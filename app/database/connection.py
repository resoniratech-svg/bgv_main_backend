import os

import pymysql
from pymysql.cursors import DictCursor


def get_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bgv_database"),
        cursorclass=DictCursor,
    )

    return connection
