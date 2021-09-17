  
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
from flaskblog import conn
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts',__name__)

@posts.route("/post/new", methods=['GET', 'POST'])
def new_post():
    if "isAuthenticated" in session:
        if session["isAuthenticated"]:
            form = PostForm()
            if form.validate_on_submit():
                c = conn.cursor()
                c.execute(f"INSERT INTO post (title, date_posted, content, user_id) VALUES ('{form.title.data}', datetime('now'), '{form.content.data}', {int(session['userID'])})")
                conn.commit()
                flash('Your Post has been created!', 'success')
                return redirect(url_for('main.home'))
        else:
            flash('Please Login again to create new post','info')
            return redirect(url_for('users.login'))
    else:
            flash('Please Login to create new post','info')
            return redirect(url_for('users.login'))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')
    

@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    updateable = False
    c = conn.cursor()
    c.execute(f"SELECT user.username, post.title, post.content, post.date_posted, user.image_file, post.id FROM post LEFT JOIN user ON user.id = post.user_id WHERE post.id = {post_id}")
    item = c.fetchone()
    post = {
        'author': item[0],
        'title': item[1],
        'content': item[2],
        'date_posted': item[3],
        'image_file': item[4],
        'id': item[5]
    }
    if "isAuthenticated" in session:
        if session["isAuthenticated"]:
            c = conn.cursor()
            c.execute(f"SELECT user_id FROM post WHERE id = {post_id}")
            if int(c.fetchone()[0]) == int(session['userID']):
                updateable = True
    return render_template('post.html', title=post['title'], post=post, updateable = updateable)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    if "isAuthenticated" in session:
        if session["isAuthenticated"]:
            c = conn.cursor()
            c.execute(f"SELECT user_id FROM post WHERE id = {post_id}")
            if int(c.fetchone()[0]) != int(session['userID']):
                abort(403)
            form = PostForm()
            if form.validate_on_submit():
                c = conn.cursor()
                c.execute(f"UPDATE post SET title = '{form.title.data}', content = '{form.content.data}' WHERE id = {post_id}")
                conn.commit()

                flash('Your Post has been Updated!', 'success')
                return redirect(url_for('posts.post', post_id=post_id))
        else:
            flash('Please Login again to update post','info')
            return redirect(url_for('users.login'))
    else:
        flash('Please Login to update post','info')
        return redirect(url_for('users.login'))
    
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'Update Post')

@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    if "isAuthenticated" in session:
        if session["isAuthenticated"]:
            c = conn.cursor()
            c.execute(f"SELECT user_id FROM post WHERE id = {post_id}")
            if int(c.fetchone()[0]) != int(session['userID']):
                abort(403)

            c = conn.cursor()
            c.execute(f"DELETE FROM post WHERE id = {post_id}")
            conn.commit()

            flash('Your Post has been Deleted!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Please Login again to delete post','info')
            return redirect(url_for('users.login'))
    else:
        flash('Please Login to delete post','info')
        return redirect(url_for('users.login'))