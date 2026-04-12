import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

# パス設定（これを一番最初に行う）
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

app = FastAPI()

class SearchRequest(BaseModel):
    user_input: str

# Vercel は /api/search へのリクエストを api/search.py に転送するため
# このファイル内ではパスをシンプルに保ち、どんなパスで来ても反応できるようにする
@app.post("/api/search")
@app.post("/")
async def search_spots(request: SearchRequest):
    try:
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
        return {"error": str(e), "msg": "Python execution failed"}

@app.get("/api/search")
@app.get("/")
async def health():
    return {"status": "ok", "message": "Search API is ready"}
