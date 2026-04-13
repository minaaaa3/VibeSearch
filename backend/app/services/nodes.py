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
    """Geminiの初期化（エラーハンドリング付き）"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        convert_system_message_to_human=True,
        google_api_key=api_key
    )

def intent_analyzer(state: AgentState):
    """ユーザーの入力を解析して構造化されたクエリに変換する"""
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "あなたはVibeSearchの意図解析エージェントです。ユーザーの入力から情報を抽出し、必ず以下のJSONフォーマットのみで回答してください。解説や挨拶は一切不要です。\n\n"
                "{\n"
                "  \"location\": \"地名またはnull\",\n"
                "  \"vibe\": [\"キーワード1\", \"キーワード2\"],\n"
                "  \"usage\": \"目的またはnull\"\n"
                "}"
            )),
            ("human", "{user_input}")
        ])
        parser = JsonOutputParser()
        chain = prompt | llm | parser
        intent = chain.invoke({"user_input": state["user_input"]})
    except Exception as e:
        print(f"!!! Intent Analyzer Fallback: {e}")
        intent = {"location": None, "vibe": [state["user_input"][:10]], "usage": "解析失敗"}

    return {"intent": intent, "messages": [f"Intent analyzed: {intent}"]}

def get_current_jst_time():
    return datetime.now(pytz.timezone('Asia/Tokyo'))

MOCK_SPOTS = [
    {"name": "スターバックス リザーブ ロースタリー 東京", "vibe": ["絶景", "作業", "コーヒー", "おしゃれ"], "usage": "仕事", "address": "東京都目黒区青葉台2-19-23", "price": "1,000円〜", "open": 7, "close": 22, "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3"},
    {"name": "代官山 蔦屋書店 Anjin", "vibe": ["読書", "静か", "集中", "Wi-Fi完備"], "usage": "一人で読書", "address": "東京都渋谷区猿楽町17-5", "price": "1,500円〜", "open": 9, "close": 22, "image": "https://images.unsplash.com/photo-1521017432531-fbd92d744264"},
    {"name": "ブルーボトルコーヒー 新宿カフェ", "vibe": ["おしゃれ", "コーヒー", "作業"], "usage": "休憩", "address": "東京都新宿区新宿4-1-6 NEWoMan新宿", "price": "700円〜", "open": 8, "close": 21, "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"},
    {"name": "BASE POINT 新宿", "vibe": ["作業", "集中", "電源あり", "Wi-Fi完備"], "usage": "仕事・勉強", "address": "東京都新宿区西新宿7-22-3", "price": "1,000円〜", "open": 10, "close": 22, "image": "https://images.unsplash.com/photo-1521017432531-fbd92d744264"},
    {"name": "青山フラワーマーケット ティーハウス", "vibe": ["癒やし", "自然", "可愛い"], "usage": "会話", "address": "東京都港区南青山5-4-41", "price": "1,500円〜", "open": 10, "close": 20, "image": "https://images.unsplash.com/photo-1490750967868-88aa35482334"},
    {"name": "bills 表参道", "vibe": ["朝食", "開放感", "おしゃれ"], "usage": "モーニング", "address": "東京都渋谷区神宮前4-30-3", "price": "2,000円〜", "open": 8, "close": 23, "image": "https://images.unsplash.com/photo-1528207772081-da6376180262"},
    {"name": "カフェ・ド・ランブル", "vibe": ["レトロ", "老舗", "コーヒー"], "usage": "こだわり", "address": "東京都中央区銀座8-10-15", "price": "1,000円〜", "open": 12, "close": 21, "image": "https://images.unsplash.com/photo-1442512595331-e89e73853f31"},
    {"name": "Garden House Crafts", "vibe": ["テラス席", "自然", "Wi-Fi完備"], "usage": "朝活", "address": "東京都渋谷区代官山町13-1", "price": "1,000円〜", "open": 8, "close": 18, "image": "https://images.unsplash.com/photo-1504753793650-d4a2b783c15e"},
]

def tool_executor(state: AgentState):
    intent = state.get("intent", {})
    vibes = intent.get("vibe", [])
    location = intent.get("location", "") or ""
    # "null" 文字列や "不明" などを除外
    if location in ["null", "None", "不明", "どこでも"]:
        location = ""
    
    current_hour = get_current_jst_time().hour
    candidates = []
    
    for spot in MOCK_SPOTS:
        score = 0
        
        # 1. エリア一致 (部分一致を強力に)
        if location:
            # 「新宿」が「東京都新宿区...」に含まれるか、またはその逆
            if location in spot["address"] or spot["address"] in location or location in spot["name"]:
                score += 10
        
        # 2. キーワード一致
        for v in vibes:
            if v and any(v in sv for sv in spot["vibe"] + [spot["name"]]):
                score += 3
        
        # 3. 利用目的の一致
        usage = intent.get("usage", "")
        if usage and usage in spot["usage"]:
            score += 2
        
        # ヒットした店舗を追加
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
    
    # 1件もヒットしない場合、または地名指定がない場合は、全店舗から人気順/ランダムに選出
    if not candidates:
        for spot in MOCK_SPOTS[:4]: # 最初の4件をデフォルトで出す
            spot_copy = spot.copy()
            spot_copy.update({
                "id": spot["name"],
                "score": 0,
                "image_url": spot.get("image") + "?auto=format&fit=crop&w=800&q=80",
                "status": "営業中" if spot["open"] <= current_hour < spot["close"] else "営業時間外",
                "crowd": "空いています",
                "metadata": {"price_range": spot["price"]}
            })
            candidates.append(spot_copy)

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return {"candidates": candidates[:6], "messages": [f"Found {len(candidates)} spots"]}

def vibe_scorer(state: AgentState):
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
                res = chain.invoke({"vibe": vibe_text, "spot_name": spot["name"]})
                spot["vibe_summary"] = res.content
            except:
                spot["vibe_summary"] = f"{vibe_text}にぴったりの雰囲気です。"
            scored.append(spot)
    except:
        for spot in state.get("candidates", []):
            spot["vibe_summary"] = "おすすめのスポットです。"
            scored.append(spot)
    return {"final_recommendations": scored, "messages": ["Scoring completed"]}
