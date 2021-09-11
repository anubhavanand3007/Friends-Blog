from flask import Flask
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('site.db', check_same_thread=False)

from flaskblog import routes