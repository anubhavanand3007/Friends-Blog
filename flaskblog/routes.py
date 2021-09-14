from flask import Flask, render_template, url_for, flash, redirect, session
from wtforms.validators import ValidationError
from flaskblog import app, bcrypt, conn
from flaskblog import forms
from flaskblog.forms import RegistrationForm, LoginForm


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, fielderror = fielderror)


@app.route("/login", methods=['GET', 'POST'])
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
            return redirect(url_for('home'))
            
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop("userID", None)
    session["isAuthenticated"] = False

    return redirect(url_for('home'))

@app.route("/account")
def account():
    if "isAuthenticated" in session:
        if session["isAuthenticated"]:
            c = conn.cursor()
            c.execute(f"SELECT * FROM user WHERE id = '{session['userID']}'")
            data = c.fetchone()
            current_user = {
                'username': data[1],
                'email':data[2],
                'image_file': data[3]
            }
            image_file = url_for('static', filename = 'profile_pics/' + current_user['image_file'])
        else:
            flash('Please Login to access Account Page','info')
            return redirect(url_for('login'))
    else:
        flash('Please Login to access Account Page','info')
        return redirect(url_for('login'))

    return render_template('account.html',title='Account',current_user = current_user,image_file = image_file)