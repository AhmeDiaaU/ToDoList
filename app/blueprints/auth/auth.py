from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql, app
import MySQLdb.cursors
import re, hashlib
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and request.form and 'date_of_birth' in request.form and 'first_name' in request.form and 'last_name' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        birthdate = request.form['date_of_birth']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        def validate_birthdate(birthdate):
            try:
                birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
                return birthdate < datetime.now().date() - timedelta(days=365 * 12)
            except ValueError:
                return False
              
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE LOWER(email) = LOWER(%s) ', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not birthdate or not first_name or not last_name:
            msg = 'Please fill out the form!'
        elif not validate_birthdate(birthdate):
            msg = 'Invalid birthdate!'
        else:
            cursor.execute('insert into user(username) values (%s)', (username,))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO accounts(password, email, user_id) VALUES (%s,%s,%s)', (password, email, user_id))
            cursor.execute('INSERT INTO user_profile(date_of_birth, first_name, last_name, user_id) values (%s,%s,%s,%s)', (birthdate, first_name, last_name, user_id))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please Fill out the Form'
    return render_template("register.html", msg=msg)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully!'
            return redirect("/")
        else:
            msg = 'Incorrect email / password!'
    return render_template('login.html', msg=msg)

@auth_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login') 