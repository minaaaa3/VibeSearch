import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

# プロジェクトルートと backend フォルダをパスに追加
# これによりインポートを確実に通す
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

app = FastAPI()

class SearchRequest(BaseModel):
    user_input: str

@app.post("/api/search")
async def search_spots(request: SearchRequest):
    try:
        # 関数の外でインポートすると起動時に 500 が出やすいので、内部でインポート
        from backend.app.services.search_agent import search_agent
        
        initial_state = {
            "user_input": request.user_input,
            "messages": [],
            "candidates": [],
            "final_recommendations": []
        }
        
        # エージェントの実行
        result = await search_agent.ainvoke(initial_state)
        
        # メッセージの正規化（React Error #31 対策）
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
        # ここで 500 を返さず、JSON で具体的なエラー内容を返す（フロントエンドのクラッシュ回避）
        return {
            "error": str(e),
            "type": type(e).__name__,
            "msg": "Python execution failed"
        }

@app.get("/api/search")
async def health():
    return {"status": "ok", "api": "search"}
