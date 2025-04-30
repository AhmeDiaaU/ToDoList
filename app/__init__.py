from flask import Flask
from flask_mysqldb import MySQL
import re, hashlib

app = Flask(__name__)
app.secret_key = 'your secret key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test' # add your sql server password you set 
app.config['MYSQL_DB'] = 'todo'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_UNIX_SOCKET'] = None
# Initialize MySQL
mysql = MySQL(app)

from app import routes