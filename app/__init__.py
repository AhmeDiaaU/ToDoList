from flask import Flask
from flask_mysqldb import MySQL
import re, hashlib

app = Flask(__name__)
app.secret_key = 'your secret key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'todo'

# Initialize MySQL
mysql = MySQL(app)

from app import routes