import os
from dotenv import load_dotenv
from tavily import TavilyClient
import requests

load_dotenv()

_tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def search_web(query: str, max_results: int = 3) -> list[dict]:
    response = _tavily_client.search(query=query, max_results=max_results)

    results = []
    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "source_type": "web",
        })
    return results


_WIKI_HEADERS = {"User-Agent": "AIResearchAgent/1.0 (educational project)"}


def search_wikipedia(query: str, max_results: int = 2) -> list[dict]:
    results = []

    search_resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": max_results,
        },
        headers=_WIKI_HEADERS,
        timeout=10,
    )
    search_resp.raise_for_status()
    titles = [item["title"] for item in search_resp.json()["query"]["search"]]

    for title in titles:
        summary_resp = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}",
            headers=_WIKI_HEADERS,
            timeout=10,
        )
        if summary_resp.status_code != 200:
            continue  

        data = summary_resp.json()
        results.append({
            "title": data.get("title", title),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            "content": data.get("extract", ""),
            "source_type": "wikipedia",
        })

    return results