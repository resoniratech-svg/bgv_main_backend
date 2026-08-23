import pymysql
from pymysql.cursors import DictCursor


def get_connection():

    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="Akanksha123",
        database="bgv_database",
        cursorclass=DictCursor
    )

    return connection