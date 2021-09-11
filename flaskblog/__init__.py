from flask import Flask
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

conn = sqlite3.connect('site.db', check_same_thread=False)
bcrypt = Bcrypt(app)

from flaskblog import routes