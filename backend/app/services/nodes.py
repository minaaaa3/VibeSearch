import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .agent_state import AgentState
from datetime import datetime
import pytz

# .env ファイルを読み込む
load_dotenv()

def get_llm():
    """Geminiの初期化（安定版の 1.5-flash を使用）"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")
    
    # 503エラー（混雑）を避けるため、プレビュー版ではなく安定版の 1.5-flash を推奨
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        convert_system_message_to_human=True,
        google_api_key=api_key
    )

async def intent_analyzer(state: AgentState):
    """ユーザーの入力を解析して構造化されたクエリに変換する"""
    print(f">>> [Node: Intent Analyzer] Starting for: {state['user_input']}")
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "あなたはVibeSearchの意図解析エージェントです。ユーザーの入力から情報を抽出し、必ず以下のJSONフォーマットのみで回答してください。解説や挨拶は一切不要です。\n\n"
                "{{\n"
                "  \"location\": \"地名またはnull\",\n"
                "  \"vibe\": [\"キーワード1\", \"キーワード2\"],\n"
                "  \"usage\": \"目的またはnull\"\n"
                "}}"
            )),
            ("human", "{user_input}")
        ])
        parser = JsonOutputParser()
        chain = prompt | llm | parser
        # ainvoke を使用して非同期で実行
        intent = await chain.ainvoke({"user_input": state["user_input"]})
        print(f">>> [Node: Intent Analyzer] Success: {intent}")
    except Exception as e:
        print(f"!!! [Node: Intent Analyzer] Fallback due to error: {e}")
        intent = {"location": None, "vibe": ["落ち着く"], "usage": "お出かけ"}

    return {"intent": intent, "messages": [f"Intent analyzed: {intent}"]}

def get_current_jst_time():
    return datetime.now(pytz.timezone('Asia/Tokyo'))

MOCK_SPOTS = [
    {"name": "スターバックス リザーブ ロースタリー 東京", "vibe": ["絶景", "作業", "コーヒー"], "usage": "仕事", "address": "東京都目黒区青葉台2-19-23", "price": "1,000円〜3,000円", "open": 7, "close": 22, "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3"},
    {"name": "代官山 蔦屋書店 Anjin", "vibe": ["読書", "静か", "集中", "Wi-Fi完備"], "usage": "読書", "address": "東京都渋谷区猿楽町17-5", "price": "1,500円〜3,000円", "open": 9, "close": 22, "image": "https://images.unsplash.com/photo-1521017432531-fbd92d744264"},
    {"name": "ブルーボトルコーヒー 新宿カフェ", "vibe": ["おしゃれ", "コーヒー", "作業"], "usage": "休憩", "address": "東京都新宿区新宿4-1-6 NEWoMan新宿", "price": "700円〜1,500円", "open": 8, "close": 21, "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"},
    {"name": "BASE POINT 新宿", "vibe": ["作業", "集中", "電源あり", "Wi-Fi完備"], "usage": "仕事", "address": "東京都新宿区西新宿7-22-3", "price": "1,000円〜2,500円", "open": 10, "close": 22, "image": "https://images.unsplash.com/photo-1521017432531-fbd92d744264"},
    {"name": "青山フラワーマーケット ティーハウス", "vibe": ["癒やし", "自然", "可愛い"], "usage": "会話", "address": "東京都港区南青山5-4-41", "price": "1,500円〜2,500円", "open": 10, "close": 20, "image": "https://images.unsplash.com/photo-1490750967868-88aa35482334"},
    {"name": "bills 表参道", "vibe": ["朝食", "開放感", "テラス席"], "usage": "モーニング", "address": "東京都渋谷区神宮前4-30-3", "price": "2,000円〜4,000円", "open": 8, "close": 23, "image": "https://images.unsplash.com/photo-1528207772081-da6376180262"},
]

async def tool_executor(state: AgentState):
    intent = state.get("intent", {})
    vibes = intent.get("vibe", [])
    location = intent.get("location", "") or ""
    current_hour = get_current_jst_time().hour
    
    candidates = []
    for spot in MOCK_SPOTS:
        score = 0
        if location and (location in spot["address"] or location in spot["name"]):
            score += 10
        for v in vibes:
            if any(v in s for s in spot["vibe"] + [spot["name"]]):
                score += 3
        
        if score > 0:
            spot_copy = spot.copy()
            spot_copy.update({
                "id": spot["name"],
                "score": score,
                "image_url": spot.get("image") + "?auto=format&fit=crop&w=800&q=80",
                "status": "営業中" if spot["open"] <= current_hour < spot["close"] else "営業時間外",
                "crowd": "空いています",
                "metadata": {"price_range": spot["price"]}
            })
            candidates.append(spot_copy)
    
    if not candidates:
        for spot in MOCK_SPOTS[:4]:
            spot_copy = spot.copy()
            spot_copy.update({
                "id": spot["name"], "score": 0, "image_url": spot.get("image") + "?auto=format&fit=crop&w=800&q=80",
                "status": "営業中", "crowd": "空いています", "metadata": {"price_range": spot["price"]}
            })
            candidates.append(spot_copy)

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return {"candidates": candidates[:6], "messages": [f"Found {len(candidates)} spots"]}

async def vibe_scorer(state: AgentState):
    scored = []
    try:
        llm = get_llm()
        vibe_text = ", ".join(state.get("intent", {}).get("vibe", ["落ち着く"]))
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたはVibeSearchのコンシェルジュです。店舗の魅力を1文で説明してください。"),
            ("human", "店舗名: {spot_name}\nこだわり: {vibe}")
        ])
        chain = prompt | llm
        for spot in state.get("candidates", []):
            try:
                # 非同期で AI 呼び出し
                res = await chain.ainvoke({"vibe": vibe_text, "spot_name": spot["name"]})
                spot["vibe_summary"] = res.content
            except:
                spot["vibe_summary"] = f"{vibe_text}にぴったりの雰囲気です。"
            scored.append(spot)
    except:
        for spot in state.get("candidates", []):
            spot["vibe_summary"] = "おすすめのスポットです。"
            scored.append(spot)
    return {"final_recommendations": scored, "messages": ["Scoring completed"]}
