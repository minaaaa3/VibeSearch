import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

# Vercel の実行環境 (/var/task) でルートディレクトリを特定
# api/search.py から見て親ディレクトリがプロジェクトルート
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# backend フォルダもパッケージとして認識させる
backend_dir = os.path.join(base_dir, 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

app = FastAPI()

class SearchRequest(BaseModel):
    user_input: str

@app.post("/api/search")
@app.post("/")
async def search_spots(request: SearchRequest):
    try:
        # 起動時ではなく、リクエスト時にインポートすることで ModuleNotFoundError で 500 になるのを防ぐ
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
        # ここで 500 エラーを発生させず、エラー詳細を JSON で返す（フロントエンドのクラッシュ防止）
        return {
            "error": str(e),
            "trace": "Check if backend directory exists and GOOGLE_API_KEY is set",
            "sys_path": sys.path
        }

@app.get("/api/search")
@app.get("/")
async def health():
    return {"status": "ok", "msg": "VibeSearch API is active"}
