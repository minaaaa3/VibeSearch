import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.services.agent_state import AgentState

# .env ファイルを読み込む
load_dotenv()

# Geminiの初期化
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    convert_system_message_to_human=True,
    google_api_key=api_key
)

def intent_analyzer(state: AgentState):
    """ユーザーの入力を解析して構造化されたクエリに変換する"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "あなたはVibeSearchの意図解析エージェントです。ユーザーの入力から以下の情報を抽出してください。\n"
            "1. location: 具体的な地名（駅名、市区町村など）。指定がない場合は null\n"
            "2. vibe: ユーザーが求めている『雰囲気』『こだわり』『目的』を3つ以内のキーワードで抽出（必ずリスト形式。例: ['静か', '作業', '電源あり']）\n"
            "3. usage: 利用目的（例: '一人で仕事', 'デート'など）。指定がない場合は null\n"
            "出力は必ず純粋なJSON形式にしてください。マークダウンの囲み（```json）は不要です。"
        )),
        ("human", "{user_input}")
    ])

    # JSONを強制するためのパーサー
    parser = JsonOutputParser()
    chain = prompt | llm | parser

    try:
        print(f"Analyzing intent for: {state['user_input']}")
        intent = chain.invoke({"user_input": state["user_input"]})

        # vibe がリストでない、または空の場合の補正（ユーザー入力を活用）
        if not isinstance(intent.get("vibe"), list) or not intent["vibe"]:
            # ユーザー入力から2-4文字程度を抽出して使う（簡易的なフォールバック）
            intent["vibe"] = [state["user_input"][:10]]

        print(f"Successfully analyzed: {intent}")
    except Exception as e:
        print(f"!!! Error in intent_analyzer: {str(e)}")
        intent = {"location": None, "vibe": [state["user_input"][:10]], "usage": "解析失敗"}

    return {
        "intent": intent,
        "messages": [f"Intent analyzed: {intent}"]
    }
from datetime import datetime
import pytz

# 日本標準時(JST)の取得
def get_current_jst_time():
    return datetime.now(pytz.timezone('Asia/Tokyo'))

# 実在する有名店舗データ (営業時間と混雑傾向を追加)
MOCK_SPOTS = [
    {
        "name": "スターバックス リザーブ ロースタリー 東京", 
        "vibe": ["絶景", "作業", "コーヒー", "おしゃれ"], 
        "usage": "仕事・観光", 
        "address": "東京都目黒区青葉台2-19-23", 
        "price": "1,000円〜3,000円",
        "open": 7, "close": 22, # 7:00 - 22:00
        "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "代官山 蔦屋書店 Anjin", 
        "vibe": ["読書", "静か", "集中", "作業"], 
        "usage": "一人で読書", 
        "address": "東京都渋谷区猿楽町17-5", 
        "price": "1,500円〜3,000円",
        "open": 9, "close": 22,
        "image": "https://images.unsplash.com/photo-1521017432531-fbd92d744264?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "ブルーボトルコーヒー 青山カフェ", 
        "vibe": ["おしゃれ", "コーヒー", "テラス席", "モダン"], 
        "usage": "デート・会話", 
        "address": "東京都港区南青山3-13-14", 
        "price": "700円〜1,500円",
        "open": 8, "close": 19,
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "青山フラワーマーケット ティーハウス", 
        "vibe": ["癒やし", "自然", "可愛い", "デート"], 
        "usage": "友人との会話", 
        "address": "東京都港区南青山5-4-41", 
        "price": "1,500円〜2,500円",
        "open": 10, "close": 20,
        "image": "https://images.unsplash.com/photo-1490750967868-88aa35482334?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "bills 表参道", 
        "vibe": ["朝食", "パンケーキ", "テラス席", "開放感"], 
        "usage": "モーニング・デート", 
        "address": "東京都渋谷区神宮前4-30-3 東急プラザ表参道原宿7F", 
        "price": "2,000円〜4,000円",
        "open": 8, "close": 23,
        "image": "https://images.unsplash.com/photo-1528207772081-da6376180262?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "カフェ・ド・ランブル", 
        "vibe": ["レトロ", "老舗", "コーヒー", "静か"], 
        "usage": "こだわりの一杯", 
        "address": "東京都中央区銀座8-10-15", 
        "price": "1,000円〜2,000円",
        "open": 12, "close": 21,
        "image": "https://images.unsplash.com/photo-1442512595331-e89e73853f31?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Mercer Brunch Ginza Terrace", 
        "vibe": ["テラス席", "おしゃれ", "デート", "夜景"], 
        "usage": "ブランチ・記念日", 
        "address": "東京都中央区銀座1-8-19 キラリトギンザ 4F", 
        "price": "3,000円〜6,000円",
        "open": 10, "close": 23,
        "image": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Bar Benfiddich", 
        "vibe": ["隠れ家", "こだわりカクテル", "暗め", "大人"], 
        "usage": "一人飲み", 
        "address": "東京都新宿区西新宿1-13-7 大束ビル 9F", 
        "price": "3,000円〜6,000円",
        "open": 18, "close": 2, # 18:00 - 2:00
        "image": "https://images.unsplash.com/photo-1470337458703-46ad1756a187?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "パークハイアット東京 ピークラウンジ", 
        "vibe": ["絶景", "夜景", "デート", "高級"], 
        "usage": "アフタヌーンティー", 
        "address": "東京都新宿区西新宿3-7-1-2 41F", 
        "price": "5,000円〜10,000円",
        "open": 12, "close": 22,
        "image": "https://images.unsplash.com/photo-1572116469696-31de0f17cc34?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "根津美術館 NEZU CAFE", 
        "vibe": ["自然", "静か", "モダン", "和風"], 
        "usage": "一人でリラックス", 
        "address": "東京都港区南青山6-5-1", 
        "price": "1,500円〜3,000円",
        "open": 10, "close": 17,
        "image": "https://images.unsplash.com/photo-1545670723-196ed0954986?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "VIRON 渋谷店", 
        "vibe": ["パン", "活気", "おしゃれ", "フランス風"], 
        "usage": "ランチ・モーニング", 
        "address": "東京都渋谷区宇田川町33-8", 
        "price": "2,000円〜4,000円",
        "open": 8, "close": 21,
        "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "クリントン・ストリート・ベイキング・カンパニー", 
        "vibe": ["パンケーキ", "朝活", "賑やか"], 
        "usage": "ブランチ", 
        "address": "東京都港区南青山5-17-1", 
        "price": "2,000円〜3,000円",
        "open": 9, "close": 18,
        "image": "https://images.unsplash.com/photo-1506084868730-34ad5033880a?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Garden House Crafts", 
        "vibe": ["テラス席", "モーニング", "自然", "開放感"], 
        "usage": "朝活・友人", 
        "address": "東京都渋谷区代官山町13-1 LOG ROAD DAIKANYAMA", 
        "price": "1,000円〜2,500円",
        "open": 8, "close": 18,
        "image": "https://images.unsplash.com/photo-1504753793650-d4a2b783c15e?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "銀座 権八", 
        "vibe": ["和風", "活気", "映画のモデル", "賑やか"], 
        "usage": "観光・会食", 
        "address": "東京都中央区銀座1-2-3", 
        "price": "4,000円〜8,000円",
        "open": 11, "close": 23,
        "image": "https://images.unsplash.com/photo-1545300329-37318536f9cc?q=80&w=800&auto=format&fit=crop"
    },
]

def tool_executor(state: AgentState):
    """
    ユーザーの意図に基づき、MOCK_SPOTS から最適な候補を絞り込む。
    リアルタイムの営業状態と混雑状況を計算して付与します。
    """
    intent = state.get("intent", {})
    vibes = intent.get("vibe", [])
    usage = intent.get("usage", "") or ""
    location = intent.get("location", "") or ""
    
    current_time = get_current_jst_time()
    current_hour = current_time.hour
    
    candidates = []
    
    for spot in MOCK_SPOTS:
        score = 0
        
        # 1. エリア一致
        if location and location != "null" and location != "不明":
            if location in spot["address"] or location in spot["name"]:
                score += 10
        
        # 2. キーワード一致
        for v in vibes:
            if any(v in sv for sv in spot["vibe"]):
                score += 2
        
        # 3. 利用目的
        if usage and any(usage in s_usage for s_usage in [spot["usage"]] + spot["vibe"]):
            score += 3
            
        if score > 0:
            spot_copy = spot.copy()
            
            # --- 営業状態の計算 ---
            is_open = False
            # 深夜営業対応 (例: 18:00 - 2:00)
            if spot["open"] < spot["close"]:
                is_open = spot["open"] <= current_hour < spot["close"]
            else: # 深夜またぎ
                is_open = current_hour >= spot["open"] or current_hour < spot["close"]
            
            status = "営業中" if is_open else "営業時間外"
            if is_open and (current_hour == (spot["close"] - 1)):
                status = "まもなく終了"
                
            # --- 混雑状況のシミュレーション ---
            # お昼(12-13)と夕方(15-17)は混雑、それ以外は比較的空いている
            crowd = "空いています"
            if 12 <= current_hour <= 13 or 15 <= current_hour <= 18:
                crowd = "混雑しています"
            elif 11 <= current_hour <= 14 or 18 <= current_hour <= 20:
                crowd = "やや混雑"
            
            spot_copy.update({
                "id": spot["name"],
                "score": score,
                "image_url": spot.get("image"),
                "status": status,
                "crowd": crowd,
                "metadata": {
                    "price_range": spot["price"],
                    "hours": f"{spot['open']}:00 - {spot['close']}:00"
                }
            })
            candidates.append(spot_copy)
            
    candidates.sort(key=lambda x: x["score"], reverse=True)
    top_candidates = candidates[:6]
    
    return {
        "candidates": top_candidates,
        "messages": [f"Calculated real-time status for {len(top_candidates)} spots"]
    }

def vibe_scorer(state: AgentState):
    """
    検索された候補を評価し、理由を生成するノード。
    Geminiを使用して、ユーザーの意図に沿った推薦理由を生成します。
    """
    scored = []
    intent = state.get("intent", {})
    vibe_text = ", ".join(intent.get("vibe", ["落ち着く"]))
    usage = intent.get("usage", "利用")

    # 推薦理由を生成するためのプロンプト
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "あなたはVibeSearchのコンシェルジュです。店舗情報とユーザーのこだわりを元に、"
            "その店がなぜおすすめなのかを、親しみやすく魅力的な1〜2文で説明してください。\n"
            "条件：\n"
            "- 『〜というご要望』のような硬い表現は避ける\n"
            "- 具体的で自然な日本語にする\n"
            "- 店舗の特徴を活かす"
        )),
        ("human", "ユーザーのこだわり: {vibe}\n利用目的: {usage}\n店舗名: {spot_name}\n説明文を生成してください。")
    ])

    chain = prompt_template | llm

    for spot in state.get("candidates", []):
        try:
            # 各店舗に対して推薦理由を生成
            response = chain.invoke({
                "vibe": vibe_text,
                "usage": usage,
                "spot_name": spot["name"]
            })
            spot["vibe_summary"] = response.content
        except Exception as e:
            print(f"Error generating summary for {spot['name']}: {e}")
            spot["vibe_summary"] = f"{vibe_text}をお探しの方にぴったりの雰囲気です。"

        scored.append(spot)

    return {
        "final_recommendations": scored,
        "messages": ["Vibe scoring and summary generation completed by Gemini"]
    }
