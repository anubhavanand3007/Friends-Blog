import sqlite3

conn = sqlite3.connect('site_temp.db')
c=conn.cursor()

c.execute("DROP table user")
c.execute("DROP table post")


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

c.execute("INSERT INTO user VALUES (1,'dummy1','dummy123@example.com','default.jpg','password123')")
c.execute("INSERT INTO post VALUES (1,'dummy title','yyyy-mm-dd-hh-mm-ss','dummy content',1)")