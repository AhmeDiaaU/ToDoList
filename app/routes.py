from flask import render_template, request, redirect, url_for, session, flash
from app import app, mysql
import MySQLdb.cursors
import re
import hashlib

@app.route('/')
def index():
    if "loggedin" in session:
        # Fetch non-archived tasks from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tasks WHERE archived = FALSE')
        todo_list = cursor.fetchall()
        return render_template('index.html', username=session['username'], todo_list=todo_list)
    return redirect('/login')

@app.route("/add", methods=["POST"])
def add():
    """Add a new task"""
    title = request.form.get("title")
    days = request.form.get("days", "")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO tasks (title, Days_of_week, complete, archived) VALUES (%s, %s, %s, %s)',
        (title, days, False, False)
    )
    mysql.connection.commit()
    return redirect(request.referrer)

@app.route("/update/<int:todo_id>")
def update(todo_id):
    """Toggle task completion status"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks WHERE id = %s', (todo_id,))
    todo = cursor.fetchone()
    if todo:
        new_status = not todo['complete']
        cursor.execute('UPDATE tasks SET complete = %s WHERE id = %s', (new_status, todo_id))
        mysql.connection.commit()
    return redirect(request.referrer)

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    """Delete a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM tasks WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(request.referrer)

@app.route("/archive/<int:todo_id>")
def archive(todo_id):
    """Archive a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET archived = TRUE WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(url_for("index"))

@app.route("/archive")
def view_archived():
    """View archived tasks"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks WHERE archived = TRUE')
    archived_tasks = cursor.fetchall()
    return render_template("archive.html", archived_tasks=archived_tasks)

@app.route("/unarchive/<int:todo_id>")
def unarchived_task(todo_id):
    """Unarchive a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET archived = FALSE WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(url_for("view_archived"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        print(f"Username: {username}, Password: {password}")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return redirect("/")
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')

@app.route('/login/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #must be hashed before entering the database
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE LOWER(username) = LOWER(%s) ', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): #handle double input 
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username): # handel username input
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL,%s,%s,%s)',(username , password , email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method== 'POST':
        msg='Please Fill out the Form'
    return render_template("register.html" , msg=msg)