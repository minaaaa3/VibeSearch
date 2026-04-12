import os
import sys
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any

# Vercel の関数実行環境 (/var/task) で backend をインポート可能にする
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# backend ディレクトリ自体も念のため追加
backend_path = os.path.join(root_path, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

app = FastAPI()

class SearchRequest(BaseModel):
    user_input: str

@app.post("/api/search")
async def search_spots(request: SearchRequest):
    try:
        # リクエストを受けてからインポートすることで、起動時のインポートエラーを防ぐ
        from backend.app.services.search_agent import search_agent
        
        initial_state = {
            "user_input": request.user_input,
            "messages": [],
            "candidates": [],
            "final_recommendations": []
        }
        
        result = await search_agent.ainvoke(initial_state)
        
        messages = []
        for msg in result.get("messages", []):
            if isinstance(msg, str):
                messages.append(msg)
            elif hasattr(msg, "content"):
                messages.append(str(msg.content))
            else:
                messages.append(str(msg))

        return {
            "intent": result.get("intent"),
            "recommendations": result.get("final_recommendations"),
            "log": messages
        }
    except Exception as e:
        # エラー発生時に 500 ではなく JSON でエラーを返し、フロントエンドがクラッシュするのを防ぐ
        return {"error": str(e), "status": "failed"}

@app.get("/api/search")
async def health():
    return {"status": "ok", "api": "search endpoint"}
