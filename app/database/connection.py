import os
import pymysql
from pymysql.cursors import DictCursor
from urllib.parse import urlparse


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        url_str = database_url
        if url_str.startswith("mysql+pymysql://"):
            url_str = url_str.replace("mysql+pymysql://", "http://")
        elif url_str.startswith("mysql://"):
            url_str = url_str.replace("mysql://", "http://")
        
        parsed = urlparse(url_str)
        return pymysql.connect(
            host=parsed.hostname or "127.0.0.1",
            port=parsed.port or 3306,
            user=parsed.username or "root",
            password=parsed.password or "",
            database=parsed.path.lstrip("/") or "bgv_database",
            cursorclass=DictCursor
        )

    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Akanksha123"),
        database=os.getenv("DB_NAME", "bgv_database"),
        cursorclass=DictCursor
    )