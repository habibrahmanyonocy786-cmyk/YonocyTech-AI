import asyncio
from typing import List, Dict, Any
from duckduckgo_search import DDGS

async def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Performs a web search using DuckDuckGo.

    Args:
        query (str): The search query.
        max_results (int): Number of results to return.

    Returns:
        List[Dict[str, Any]]: A list of results containing title, url, and snippet.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            return [
                {
                    "title": r.get("title", "No Title"),
                    "url": r.get("href", ""),
                    "snippet": r.get("text", "")
                }
                for r in results
            ]
    except Exception as e:
        print(f"Web search error: {e}")
        return []
