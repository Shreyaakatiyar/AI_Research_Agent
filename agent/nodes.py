from agent.state import ResearchState
from agent.llm import llm
from agent.tools import search_web, search_wikipedia


def _extract_text(response) -> str:
    content = response.content
    if isinstance(content, str):
        return content.strip()

    text_parts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))
        elif isinstance(block, str):
            text_parts.append(block)
    return "".join(text_parts).strip()


def analyze_query(state: ResearchState) -> dict:
    """
    Turn the user's raw question into a focused search query.
    """
    prompt = f"""You are helping prepare a research search query.

User's question: "{state["query"]}"

Rewrite this as a single, focused search engine query (no more than
10 words) that would return the most relevant results. Respond with
ONLY the search query text, nothing else — no quotes, no explanation.
"""

    response = llm.invoke(prompt)
    refined_query = _extract_text(response)

    return{
        "search_queries": [refined_query],
        "iterations": 0,
    }

def search_web_node(state: ResearchState) -> dict:
    query = state["search_queries"][-1]
    results = search_web(query)
    return {"sources": results}

def search_wikipedia_node(state: ResearchState) -> dict:
    query = state["search_queries"][-1]
    results = search_wikipedia(query)
    return {"sources": results}