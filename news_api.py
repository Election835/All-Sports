import os

import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_news(query="sports", max_results=10):
    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        raise ValueError("Missing GNEWS_API_KEY. Add your key to the .env file.")

    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": api_key,
        "q": query,
        "language": "en",
        "size": max_results,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout as exc:
        raise TimeoutError("Request timed out while loading the latest news.") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            "We're having trouble loading the latest news. Please try again later."
        ) from exc
    except ValueError as exc:
        raise RuntimeError("Invalid API response from the news provider.") from exc

    if data.get("status") == "error":
        raise RuntimeError("We're having trouble loading the latest news. Please try again later.")

    articles = data.get("results", [])
    cleaned_articles = []

    for article in articles:
        creator = article.get("creator") or []
        source_name = creator[0] if isinstance(creator, list) and creator else article.get("source_id") or "Unknown source"

        cleaned_articles.append(
            {
                "title": article.get("title") or "Untitled article",
                "description": article.get("description") or "No summary available.",
                "url": article.get("link") or article.get("url") or "#",
                "image_url": article.get("image_url") or "",
                "source": source_name,
                "published_at": article.get("pubDate") or "Unknown date",
            }
        )

    return cleaned_articles
