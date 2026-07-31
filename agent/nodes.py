from agent.state import ResearchState
from agent.llm import llm
from agent.tools import search_web, search_wikipedia
from pydantic import BaseModel, Field
from typing import Optional

MAX_ITERATIONS = 3


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

class SufficiencyCheck(BaseModel):
    is_sufficient: bool = Field(
        description="True if the gathered sources contain enough information to write a good, well-rounded answer to the user's question."
    )
    reasoning: str = Field(
        description="One sentence explaining why the info is or isn't sufficient."
    )
    refined_query: Optional[str] = Field(
        default=None,
        description="If not sufficient, a NEW, more specific search query to try next (different angle than previous queries). Null if sufficient."
    )

def evaluate_sufficiency(state: ResearchState) -> dict:
    sources_text = "\n\n".join(
        f"[{s['source_type']}] {s['title']}: {s['content'][:300]}"
        for s in state["sources"]
    )

    prompt = f"""Original question: "{state['query']}"

Sources gathered so far:
{sources_text}

Evaluate whether these sources are sufficient to write a thorough, accurate answer to the original question."""

    structured_llm = llm.with_structured_output(SufficiencyCheck)
    result: SufficiencyCheck = structured_llm.invoke(prompt)

    new_iterations = state["iterations"] + 1

    is_sufficient = result.is_sufficient or new_iterations >= MAX_ITERATIONS

    update = {
        "iterations": new_iterations,
        "is_sufficient": is_sufficient,
    }

    if not is_sufficient and result.refined_query:
        update["search_queries"] = [result.refined_query]

    return update