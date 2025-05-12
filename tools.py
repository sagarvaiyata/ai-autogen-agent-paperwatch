import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import arxiv
from autogen_core.tools import FunctionTool
from datetime import datetime

load_dotenv()

def google_search(query: str, num_results: int = 2, max_chars: int = 500) -> list:
    """Search Google and return enriched results with snippet and page body."""
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    if not api_key or not cx:
        raise ValueError("GOOGLE_API_KEY or GOOGLE_SEARCH_ENGINE_ID not set")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cx, "q": query, "num": num_results}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        raise Exception(f"Google API error: {resp.status_code}")

    items = resp.json().get("items", [])
    def get_page_content(u: str) -> str:
        try:
            r = requests.get(u, timeout=10)
            text = BeautifulSoup(r.content, "html.parser").get_text(separator=" ", strip=True)
            words, out = text.split(), ""
            for w in words:
                if len(out) + len(w) + 1 > max_chars:
                    break
                out += " " + w
            return out.strip()
        except:
            return ""

    results = []
    for i in items:
        body = get_page_content(i["link"])
        results.append({
            "title": i["title"],
            "link": i["link"],
            "snippet": i.get("snippet", ""),
            "body": body
        })
        time.sleep(1)
    return results

def arxiv_search(query: str, max_results: int = 2) -> list:
    """Search Arxiv and return paper metadata including abstracts."""
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=max_results,
                          sort_by=arxiv.SortCriterion.Relevance)
    out = []
    for paper in client.results(search):
        out.append({
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "published": paper.published.strftime("%Y-%m-%d"),
            "abstract": paper.summary,
            "pdf_url": paper.pdf_url,
        })
    return out

def time_tool_function():
    name = "time_tool"
    description = (
        "Returns the current date in YYYY-MM-DD format. "
        "Use this to filter search queries for the most recent results."
    )

    def run(self, query: str = "") -> str:
        # ignore any query, always return today's date
        return datetime.now().strftime("%Y-%m-%d")

time_tool = FunctionTool(
    time_tool_function,
    description="Tool used to fetch news"
)

google_search_tool = FunctionTool(
    google_search,
    description="Search Google for information, returns results with snippet and body"
)
arxiv_search_tool = FunctionTool(
    arxiv_search,
    description="Search Arxiv for papers related to a given topic, including abstracts"
)
