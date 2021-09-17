from typing import Mapping
from flask import render_template, request, Blueprint
from flaskblog import conn

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    c = conn.cursor()
    c.execute("SELECT user.username, post.title, post.content, post.date_posted, user.image_file, post.id FROM post LEFT JOIN user ON user.id = post.user_id")
    items = c.fetchall()
    posts = []
    for item in items:
        post = {
            'author': item[0],
            'title': item[1],
            'content': item[2],
            'date_posted': item[3],
            'image_file': item[4],
            'id': item[5]
        }
        posts.append(post)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/user_posts/<author>", methods=['GET', 'POST'])
def user_posts(author):
    c = conn.cursor()
    c.execute(f"SELECT user.username, post.title, post.content, post.date_posted, user.image_file, post.id FROM post LEFT JOIN user ON user.id = post.user_id WHERE user.username = '{author}'")

    items = c.fetchall()
    posts = []
    for item in items:
        post = {
            'author': item[0],
            'title': item[1],
            'content': item[2],
            'date_posted': item[3],
            'image_file': item[4],
            'id': item[5]
        }
        posts.append(post)
    return render_template('user_posts.html', posts = posts, author = author)