import sqlite3

conn = sqlite3.connect("site.db")

c = conn.cursor()
# c.execute("SELECT user.username, post.title, post.content, post.date_posted FROM post LEFT JOIN user ON user.id = post.user_id")
c.execute(f"SELECT user.username, post.title, post.content, post.date_posted, user.image_file FROM post LEFT JOIN user ON user.id = post.user_id WHERE post.id = 1")

data = c.fetchall()

print(data)