from flask import render_template, request, redirect, url_for, session, flash
from app import app, mysql
import MySQLdb.cursors
import re
import hashlib
from datetime import datetime, timedelta

@app.route('/')
def index():
    if "loggedin" in session:
        query = '''
            SELECT t.*, c.category_id, c.category_name, ts.day_of_week, ts.end_time
            FROM tasks t
            LEFT JOIN category c ON t.c_id = c.category_id
            LEFT JOIN tasks_Schedule ts ON t.id = ts.task_id
            WHERE t.archived = FALSE AND t.user_id = %s
            ORDER BY c.category_name, t.title
        '''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (session['id'],))
        tasks = cursor.fetchall()
        cursor.execute('SELECT * FROM category')
        categories = cursor.fetchall()
        cursor.close()

        # Group tasks by category_id
        categories_with_tasks = []
        for category in categories:
            cat_tasks = [task for task in tasks if task['category_id'] == category['category_id']]
            for task in cat_tasks:
                if task['end_time']:
                    try:
                        task['end_time'] = datetime.strptime(str(task['end_time']), '%H:%M:%S').strftime('%I:%M %p')
                    except ValueError:
                        app.logger.error(f"Error parsing time: {task['end_time']}")
                        task['end_time'] = None
            categories_with_tasks.append({
                'category_id': category['category_id'],
                'category_name': category['category_name'],
                'tasks': cat_tasks
            })
        return render_template('index.html', email=session['email'], categories_with_tasks=categories_with_tasks , categories=categories)
    return redirect('/login')

@app.route("/add", methods=["POST"])
def add():
    days = {
        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "sun": "Sunday"
    }
    try:
        # Get form data
        title = request.form.get("title")
        days_abrv = request.form.get("days")
        category_id = request.form.get("category_id")
        created_at = datetime.now()
        end_at = request.form.get("end_time")
        repeat_task = request.form.get("r_task") == "true"
        repeat_interval = request.form.get("r_period") if repeat_task else None

        # Validate form data
        if not all([title, days_abrv, category_id, end_at]):
            flash("All fields are required.", "error")
            return redirect(url_for("index"))
        # Database operations
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Insert task
            cursor.execute(
                'INSERT INTO tasks (title, Created_at, complete, archived, user_id, c_id) VALUES (%s, %s, %s, %s, %s, %s)',
                (title, created_at, False, False, session['id'], category_id)
            )
            task_id = cursor.lastrowid

            # Insert task schedule for each day
            days_abrv = days_abrv.lower()
            day_full = days[days_abrv]
            cursor.execute(
                    'INSERT INTO tasks_Schedule (task_id, day_of_week, end_time, repeat_task, repeat_interval) '
                    'VALUES (%s, %s, %s, %s, %s)',
                    (task_id, day_full, end_at, repeat_task, repeat_interval)
             )

            mysql.connection.commit()
            flash("Task added successfully.", "success")

        except MySQLdb.Error as db_error:
            mysql.connection.rollback()
            app.logger.error(f"Database error: {db_error}")
            flash("An error occurred while adding the task. Please try again later.", "error")
            return redirect(url_for("index"))

        return redirect(url_for("index"))

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for("index"))

    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route("/update/<int:todo_id>")
def update(todo_id):
    """Toggle task completion status"""
    user_id = session['id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks WHERE id = %s and user_id = %s', (todo_id,user_id ,))
    todo = cursor.fetchone()
    if todo:
        new_status = not todo['complete']
        cursor.execute('UPDATE tasks SET complete = %s WHERE id = %s and user_id = %s', (new_status, todo_id , user_id))    
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
    for task in archived_tasks:
        if task['end_time']:
            try:
                task['end_time'] = datetime.strptime(str(task['end_time']), '%H:%M:%S').strftime('%I:%M %p')
            except ValueError:
                app.logger.error(f"Error parsing time: {task['end_time']}")
                task['end_time'] = None
    return render_template("archive.html", archived_tasks=archived_tasks)

@app.route("/unarchive/<int:todo_id>")
def unarchived_task(todo_id):
    """Unarchive a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET archived = FALSE WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(url_for("view_archived"))

@app.route('/category/add', methods=['POST'])
def add_category():
    """
    add a new category by sending name from form to the database
    Returns:
        
    """
    try:
        if 'loggedin' not in session:
            flash("You need to log in to view categories.", "error")
            return redirect('/login')
        
        if not isinstance(session.get('id'), int):
            flash("Invalid user session. Please log in again.", "error")
            return redirect('/login')
        
        category_name = request.form.get('new_category')
        if not category_name:
            flash("Category name is required.", "error")    
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category WHERE category_name = %s', (category_name,))
        if cursor.fetchone():
            flash("Category already exists.", "error")
        else:
            cursor.execute('INSERT INTO category (category_name) VALUES (%s)', (category_name,))
            mysql.connection.commit()
            flash("Category added successfully!", "success")
        mysql.connection.commit()
        return redirect(url_for("index"))
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/')

@app.route('/category/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """
    delete category by sending id to the db and delete it 
    """
    try : 
        if 'loggedin' in session : 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('DELETE FROM category WHERE category_id = %s', (category_id,))
            mysql.connection.commit()
            flash("Category deleted successfully!", "success")
        else :
            flash("You need to log in to delete categories.", "error")
        return redirect(url_for("index"))
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/')

@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')

@app.route('/login/register', methods=['GET', 'POST'])
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

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login/", methods=["POST", "GET"])
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