import sqlite3
from settings import DB_NAME


def create(db_name):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # создание таблиц + наполнение
    cursor.executescript("""
        CREATE TABLE "users" (
            `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
            `username`    TEXT,
            `created_at`    DATETIME
        );

        CREATE TABLE "chat" (
            `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
            `name`    TEXT,
            `created_at`    DATETIME
        );
        
        CREATE TABLE "messages" (
            `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
            `chat`  INTEGER,
            `author` INTEGER,
            `text` TEXT,
            `created_at`  DATETIME
        );
        
        CREATE TABLE "user_chat" (
            `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
            `chat`  INTEGER,
            `user`    INTEGER
        )
    """)

    # фиксирую коммит
    conn.commit()


def connect():
    return sqlite3.connect(DB_NAME)
