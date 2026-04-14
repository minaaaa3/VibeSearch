from fastapi import APIRouter, HTTPException
from ..services.search_agent import search_agent
from pydantic import BaseModel
from typing import List, Dict, Any
import traceback

router = APIRouter()

class SearchRequest(BaseModel):
    user_input: str

@router.post("/search")
async def search_spots(request: SearchRequest):
    print(f"\n>>> [Backend] Received search request: {request.user_input}")
    try:
        # 初期状態
        initial_state = {
            "user_input": request.user_input,
            "messages": [],
            "candidates": [],
            "final_recommendations": []
        }
        
        print(">>> [Backend] Starting search_agent.ainvoke...")
        # エージェントの実行
        result = await search_agent.ainvoke(initial_state)
        print(">>> [Backend] search_agent execution completed.")
        
        # メッセージを安全に文字列化
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
        print(f"!!! [Backend] Error in search_spots: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
