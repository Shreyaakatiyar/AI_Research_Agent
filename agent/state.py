from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    query: str

    search_queries: List[str]

    sources: Annotated[List[dict], operator.add]

    iterations: int

    is_sufficient: bool

    final_answer: str
