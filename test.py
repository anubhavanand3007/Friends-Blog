import sqlite3
from flask import session

conn = sqlite3.connect("site.db")

c = conn.cursor()
# c.execute("SELECT user.username, post.title, post.content, post.date_posted FROM post LEFT JOIN user ON user.id = post.user_id")
c.execute(f"SELECT user_id FROM post WHERE id = 2")

data = c.fetchone()[0]

print(data)