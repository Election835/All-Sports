import sqlite3

DATABASE_PATH = "favorites.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL UNIQUE,
            image_url TEXT,
            source TEXT,
            published_at TEXT
        )
        """
    )
    connection.commit()
    connection.close()


def save_favorite(article):
    connection = get_db_connection()
    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO favorites (title, description, url, image_url, source, published_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                article.get("title"),
                article.get("description"),
                article.get("url"),
                article.get("image_url"),
                article.get("source"),
                article.get("published_at"),
            ),
        )
        connection.commit()
    finally:
        connection.close()


def favorite_exists(url):
    connection = get_db_connection()
    result = connection.execute(
        "SELECT 1 FROM favorites WHERE url = ?",
        (url,),
    ).fetchone()
    connection.close()
    return result is not None


def get_favorites():
    connection = get_db_connection()
    favorites = connection.execute(
        "SELECT id, title, description, url, image_url, source, published_at FROM favorites ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return [dict(row) for row in favorites]


def delete_favorite(url):
    connection = get_db_connection()
    connection.execute("DELETE FROM favorites WHERE url = ?", (url,))
    connection.commit()
    connection.close()
