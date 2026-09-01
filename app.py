import sqlite3

from flask import Flask, redirect, render_template, request, url_for

from database import delete_favorite, get_favorites, init_db, save_favorite
from news_api import fetch_news

app = Flask(__name__)

# Sport display names and navigation labels
SPORT_LABELS = {
    "all": "All",
    "nfl": "NFL",
    "nba": "NBA",
    "mlb": "MLB",
    "nhl": "NHL",
    "soccer": "Soccer",
}

# Specific, professional-only sport queries to prevent mixing
SPORT_QUERIES = {
    "all": "sports news",
    "nfl": "NFL professional football",  # Explicitly exclude college
    "nba": "NBA professional basketball",  # Explicitly exclude college/WNBA
    "mlb": "MLB professional baseball",  # Explicitly exclude college
    "nhl": "NHL professional ice hockey",  # Explicitly exclude college/minor leagues
    "soccer": "soccer Premier League Champions League MLS",  # International/professional focus
}

# Team names mapped to their full name and sport for better search queries
TEAM_MAPPING = {
    # NBA Teams
    "lakers": ("Los Angeles Lakers", "NBA"),
    "celtics": ("Boston Celtics", "NBA"),
    "warriors": ("Golden State Warriors", "NBA"),
    "heat": ("Miami Heat", "NBA"),
    "nets": ("Brooklyn Nets", "NBA"),
    "hawks": ("Atlanta Hawks", "NBA"),
    "bucks": ("Milwaukee Bucks", "NBA"),
    "76ers": ("Philadelphia 76ers", "NBA"),
    "suns": ("Phoenix Suns", "NBA"),
    "mavericks": ("Dallas Mavericks", "NBA"),
    # NFL Teams
    "patriots": ("New England Patriots", "NFL"),
    "cowboys": ("Dallas Cowboys", "NFL"),
    "chiefs": ("Kansas City Chiefs", "NFL"),
    "falcons": ("Atlanta Falcons", "NFL"),
    "ravens": ("Baltimore Ravens", "NFL"),
    "bills": ("Buffalo Bills", "NFL"),
    "broncos": ("Denver Broncos", "NFL"),
    "lions": ("Detroit Lions", "NFL"),
    "packers": ("Green Bay Packers", "NFL"),
    "colts": ("Indianapolis Colts", "NFL"),
    # MLB Teams
    "yankees": ("New York Yankees", "MLB"),
    "redsox": ("Boston Red Sox", "MLB"),
    "dodgers": ("Los Angeles Dodgers", "MLB"),
    "giants": ("San Francisco Giants", "MLB"),
    "braves": ("Atlanta Braves", "MLB"),
    "cubs": ("Chicago Cubs", "MLB"),
    "white sox": ("Chicago White Sox", "MLB"),
    "twins": ("Minnesota Twins", "MLB"),
    # Soccer Teams
    "manchester united": ("Manchester United", "Soccer"),
    "manchester city": ("Manchester City", "Soccer"),
    "arsenal": ("Arsenal", "Soccer"),
    "liverpool": ("Liverpool", "Soccer"),
    "chelsea": ("Chelsea", "Soccer"),
}


def find_best_query(search_term):
    """
    Convert a user search into the best query for the news API.
    If the search matches a known team, include the sport in the query.
    Otherwise, return the search term as-is.
    
    This ensures team searches return team-specific content.
    """
    if not search_term:
        return None
    
    search_lower = search_term.lower().strip()
    
    # Check if the search matches a known team
    if search_lower in TEAM_MAPPING:
        full_name, sport = TEAM_MAPPING[search_lower]
        # Add sport context to make search more specific
        # e.g., "Atlanta Falcons NFL" instead of just "Atlanta Falcons"
        return f"{full_name} {sport}"
    
    # If not a known team, return the search term as-is
    return search_term


def filter_relevant_articles(articles, search_term, original_search):
    """
    Filter articles to prefer those that mention the searched team.
    
    Args:
        articles: List of articles from the API
        search_term: The term we searched for (may be full team name)
        original_search: The original user input
    
    Returns:
        Tuple of (filtered_articles, fallback_message)
        fallback_message is None if we found team-specific results,
        or a message if we're showing broader results
    """
    if not articles or not search_term:
        return articles, None
    
    # Extract key words from the search term to match against articles
    search_words = search_term.lower().split()
    
    # Score each article based on how many search words appear in title/description
    relevant_articles = []
    for article in articles:
        title_lower = article.get("title", "").lower()
        desc_lower = article.get("description", "").lower()
        combined = title_lower + " " + desc_lower
        
        # Count how many search words appear in the article
        match_count = sum(1 for word in search_words if word in combined)
        
        if match_count > 0:
            relevant_articles.append((article, match_count))
    
    # If we found relevant articles, sort by relevance and return them
    if relevant_articles:
        relevant_articles.sort(key=lambda x: x[1], reverse=True)
        sorted_articles = [article for article, _ in relevant_articles]
        return sorted_articles, None
    
    # If no team-specific articles found, show a fallback message
    if original_search in TEAM_MAPPING:
        full_name, sport = TEAM_MAPPING[original_search.lower()]
        fallback_msg = f"No specific {full_name} news found. Showing related {sport} news."
        return articles, fallback_msg
    
    return articles, None

init_db()


@app.route("/")
def home():
    selected_sport = request.args.get("sport", "all")
    search_query = request.args.get("q", "").strip()

    # Validate sport selection
    if selected_sport not in SPORT_QUERIES:
        selected_sport = "all"
    
    # Determine what to search for
    if search_query:
        # User entered a search - use our improved query logic with sport context
        query_to_fetch = find_best_query(search_query)
    else:
        # No search - use the specific sport query to avoid mixing
        query_to_fetch = SPORT_QUERIES[selected_sport]

    try:
        articles = fetch_news(query_to_fetch)
        message = None
        
        # If user searched for a team, filter results and show fallback message if needed
        if search_query:
            articles, fallback_msg = filter_relevant_articles(articles, query_to_fetch, search_query)
            if fallback_msg:
                message = fallback_msg
            elif not articles:
                message = "No articles found for your search."
        elif not articles:
            message = "No articles found for this category."
            
    except (ValueError, RuntimeError, TimeoutError) as exc:
        articles = []
        message = str(exc)

    return render_template(
        "index.html",
        articles=articles,
        message=message,
        selected_sport=selected_sport,
        search_query=search_query,
        sport_labels=SPORT_LABELS,
    )


@app.route("/save", methods=["POST"])
def save_article():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    url = request.form.get("url", "").strip()
    image_url = request.form.get("image_url", "").strip()
    source = request.form.get("source", "").strip()
    published_at = request.form.get("published_at", "").strip()

    if not url:
        return redirect(url_for("home"))

    article = {
        "title": title,
        "description": description,
        "url": url,
        "image_url": image_url,
        "source": source,
        "published_at": published_at,
    }

    try:
        save_favorite(article)
    except sqlite3.Error:
        pass

    return redirect(url_for("home"))


@app.route("/favorites")
def favorites():
    try:
        favorites = get_favorites()
    except sqlite3.Error:
        favorites = []

    return render_template("favorites.html", favorites=favorites)


@app.route("/remove", methods=["POST"])
def remove_favorite():
    url = request.form.get("url", "").strip()
    if url:
        try:
            delete_favorite(url)
        except sqlite3.Error:
            pass
    return redirect(url_for("favorites"))


@app.route("/article")
def article_detail():
    article_url = request.args.get("url", "").strip()

    if not article_url:
        return redirect(url_for("home"))

    article = {
        "title": request.args.get("title", "Article"),
        "description": request.args.get("description", "No summary available."),
        "url": article_url,
        "image_url": request.args.get("image_url", ""),
        "source": request.args.get("source", "Unknown source"),
        "published_at": request.args.get("published_at", "Unknown date"),
    }

    return render_template("article.html", article=article)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
