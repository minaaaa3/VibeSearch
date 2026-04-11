from typing import TypedDict, List, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    # ユーザーの生の入力
    user_input: str
    # Intent Analyzerが抽出した条件
    intent: Dict[str, Any]
    # 検索されたスポット候補
    candidates: List[Dict[str, Any]]
    # 最終的な推薦結果
    final_recommendations: List[Dict[str, Any]]
    # フィードバックループ用（前回の対話履歴など）
    messages: Annotated[List[str], operator.add]
