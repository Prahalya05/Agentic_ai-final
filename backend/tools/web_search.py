from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    tavily = TavilySearchResults(max_results=5)
    results = tavily.invoke({"query": query})
    return "\n".join([f"{r['title']}: {r['content']}" for r in results])
