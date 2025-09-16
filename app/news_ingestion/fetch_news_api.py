import requests
import os
from app.config import NEWS_API_KEY

HN_API_URL = "https://hn.algolia.com/api/v1/search_by_date"

def fetch_ai_news():
    """
    Fetch the latest AI-related news from Hacker News (sorted by date).
    """
    params = {
        "query": "artificial intelligence",  # keyword
        "tags": "story",
        "hitsPerPage": 20  # how many results you want
    }

    response = requests.get(HN_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    articles = [
        {
        "title": hit.get("story_title"),  # Use story_title
        "url": hit.get("story_url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
        "description": hit.get("comment_text"),  # Use comment_text as description
        "source": "HackerNews",
        "publishedAt": hit.get("created_at"),
        "points": hit.get("points", None),  # Safe fallback in case points doesn't exist
        "author": hit.get("author")
    }
        for hit in data.get("hits", [])
    ]

    return articles
