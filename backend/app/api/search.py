from fastapi import APIRouter, HTTPException
from app.services.search_agent import search_agent
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class SearchRequest(BaseModel):
    user_input: str

@router.post("/search")
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
        raise HTTPException(status_code=500, detail=str(e))
