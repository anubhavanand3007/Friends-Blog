
from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flaskblog import bcrypt, conn
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.users.utils import save_picture

users = Blueprint('users',__name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    fielderror = {}
    form = RegistrationForm()
    c = conn.cursor()
    
    c.execute(f"SELECT id FROM user WHERE email = '{form.email.data}'")
    isEmail = c.fetchone()
    c.execute(f"SELECT id FROM user WHERE username = '{form.username.data}'")
    isUsername = c.fetchone()

    if isEmail:
        fielderror['email'] = 'This Email is already taken.'
    if isUsername:
        fielderror['username'] = 'This Usernanme is already taken.'

    if form.validate_on_submit() and not isUsername and not isEmail:

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        c = conn.cursor()
        c.execute(f"INSERT INTO user(username, email, password) VALUES ('{form.username.data}','{form.email.data}','{hashed_password}')")

        conn.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, fielderror = fielderror)


@users.route("/login", methods=['GET', 'POST'])
def login():
    #login data
    form = LoginForm()
    
    #is entered value valid?
    if form.validate_on_submit():

        #cursor for database connection
        c = conn.cursor()
        c.execute(f"SELECT password FROM user WHERE email = '{form.email.data}'")
        password = c.fetchone()
        #authentication
        if password == None:
            flash('Login Unsuccessfull, Given username does not exist', 'danger')
        elif bcrypt.check_password_hash(password[0],form.password.data):

            #creating session storage
            c.execute(f"SELECT id FROM user WHERE email = '{form.email.data}'")
            session.permanent = False
            session['userID'] = f"{c.fetchone()[0]}"
            session["isAuthenticated"] = True
            
            flash(f'Login Successfull, Welcome   to flaskblog', 'success')
            return redirect(url_for('main.home'))
            
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop("userID", None)
    session["isAuthenticated"] = False

    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
def account():
    if "isAuthenticated" in session:

        #REAL ACCOUNT PAGE
        if session["isAuthenticated"]:
            fielderror = {}
            form = UpdateAccountForm()
            
            c = conn.cursor()
            c.execute(f"SELECT * FROM user WHERE id = '{session['userID']}'")
            data = c.fetchone()
            current_user = {
                'id': data[0],
                'username': data[1],
                'email':data[2],
                'image_file': data[3]
            }
            form.username.data = current_user['username']
            form.email.data = current_user['email']
            image_file = url_for('static', filename = 'profile_pics/' + current_user['image_file'])

            c = conn.cursor()
            c.execute(f"SELECT user.username, post.title, post.content, post.date_posted, user.image_file, post.id FROM post LEFT JOIN user ON user.id = post.user_id WHERE user.username = '{current_user['username']}'")

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
            c = conn.cursor()
   
            c.execute(f"SELECT id FROM user WHERE email = '{form.email.data}' AND email <> '{current_user['email']}'")       
            isEmail = c.fetchone()
            c.execute(f"SELECT id FROM user WHERE username = '{form.username.data}' AND username <> '{current_user['username']}'")
            isUsername = c.fetchone()

            if isEmail:
                fielderror['email'] = 'This Email is already taken.'
            if isUsername:
                fielderror['username'] = 'This Usernanme is already taken.'

            if form.validate_on_submit() and not isUsername and not isEmail:
                c = conn.cursor()

                if form.picture.data:
                    picture_file = save_picture(form.picture.data)
                    c.execute(f"UPDATE user SET image_file = '{picture_file}' WHERE id = {int(session['userID'])}")
                if form.username.data:
                    c.execute(f"UPDATE user SET username = '{form.username.data}' WHERE id = {int(current_user['id'])}")     
                if form.email.data:
                    c.execute(f"UPDATE user SET email = '{form.email.data}' WHERE id = {int(current_user['id'])}")
                conn.commit()
                flash(f'Account Updated to {form.username.data}!', 'success')
                return redirect(url_for('users.account'))
            

        else:
            flash('Please Login to access Account Page','info')
            return redirect(url_for('users.login'))
    else:
        flash('Please Login to access Account Page','info')
        return redirect(url_for('users.login'))

    return render_template('account.html',title='Account',current_user = current_user,image_file = image_file, form=form, fielderror= fielderror, posts = posts)