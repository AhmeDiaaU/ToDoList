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

# Import and register blueprints
from app.blueprints.tasks import tasks_bp
from app.blueprints.categories import categories_bp
from app.blueprints.auth import auth_bp
from app.blueprints.pages import pages_bp

app.register_blueprint(tasks_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(pages_bp)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return "404 Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error", 500

@app.errorhandler(403)
def forbidden_error(error):
    return "403 Forbidden", 403