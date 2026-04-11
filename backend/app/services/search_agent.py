from langgraph.graph import StateGraph, END
from app.services.agent_state import AgentState
from app.services.nodes import intent_analyzer, tool_executor, vibe_scorer

def create_search_graph():
    # グラフの初期化
    workflow = StateGraph(AgentState)

    # ノードの追加
    workflow.add_node("analyze_intent", intent_analyzer)
    workflow.add_node("search_candidates", tool_executor)
    workflow.add_node("score_vibe", vibe_scorer)

    # エッジの定義（接続順序）
    workflow.set_entry_point("analyze_intent")
    workflow.add_edge("analyze_intent", "search_candidates")
    workflow.add_edge("search_candidates", "score_vibe")
    workflow.add_edge("score_vibe", END)

    # コンパイル
    return workflow.compile()

# エージェント実行用のインスタンス
search_agent = create_search_graph()
