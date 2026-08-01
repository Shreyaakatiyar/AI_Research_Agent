from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agent.state import ResearchState
from agent.nodes import (
    analyze_query,
    search_web_node,
    search_wikipedia_node,
    evaluate_sufficiency,
    summarize,
)

def route_after_evaluation(state: ResearchState):
    if state["is_sufficient"]:
        return "summarize"
    return ["search_web", "search_wikipedia"]

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("analyze_query", analyze_query)
    graph.add_node("search_web", search_web_node)
    graph.add_node("search_wikipedia", search_wikipedia_node)
    graph.add_node("evaluate_sufficiency", evaluate_sufficiency)
    graph.add_node("summarize", summarize)

    graph.add_edge(START, "analyze_query")

    graph.add_edge("analyze_query", "search_web")
    graph.add_edge("analyze_query", "search_wikipedia")

    graph.add_edge("search_web", "evaluate_sufficiency")
    graph.add_edge("search_wikipedia", "evaluate_sufficiency")

    graph.add_conditional_edges("evaluate_sufficiency", route_after_evaluation)

    graph.add_edge("summarize", END)

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)