import sqlite3

conn = sqlite3.connect('site.db')
c=conn.cursor()

c.execute("""
    CREATE TABLE user(
    id  INTEGER PRIMARY KEY,
    username TEXT(20) UNIQUE NOT NULL,
    email TEXT(120) UNIQUE NOT NULL,
    image_file TEXT(20) NOT NULL DEFAULT 'default.jpg',
    password TEXT(20) NOT NULL
    )
""")


c.execute("""
    CREATE TABLE post(
    id  INTEGER PRIMARY KEY,
    title TEXT(100) NOT NULL,
    date_posted DATETIME DEFAULT TIME,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL
    )
""")
