from flask import render_template, flash, url_for, redirect
from flaskblog import app, conn, bcrypt
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