import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

# プロジェクトルートと backend フォルダをパスに追加
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.path.join(root_dir, 'backend') not in sys.path:
    sys.path.insert(0, os.path.join(root_dir, 'backend'))

# backend から直接 search_agent をインポート
from backend.app.services.search_agent import search_agent

# Vercel は 'app' という変数名を探します
app = FastAPI()

class SearchRequest(BaseModel):
    user_input: str

@app.post("/api/search")
async def search_spots(request: SearchRequest):
    try:
        # 初期状態の設定
        initial_state = {
            "user_input": request.user_input,
            "messages": [],
            "candidates": [],
            "final_recommendations": []
        }
        
        # エージェントの実行
        result = await search_agent.ainvoke(initial_state)
        
        # メッセージを安全に文字列化（React Error #31 回避）
        messages = []
        for msg in result.get("messages", []):
            if isinstance(msg, str):
                messages.append(msg)
            elif hasattr(msg, "content"): # BaseMessage系
                messages.append(str(msg.content))
            else:
                messages.append(str(msg))

        return {
            "intent": result.get("intent"),
            "recommendations": result.get("final_recommendations"),
            "log": messages
        }
    except Exception as e:
        # 具体的なエラーメッセージを返すことで、フロントエンドでデバッグしやすくする
        return {
            "error": str(e),
            "trace": "Error during search execution"
        }

@app.get("/api/search")
async def health_check():
    return {"status": "search endpoint is alive"}
