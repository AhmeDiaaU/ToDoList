from flask import render_template, request, redirect, url_for, session, flash
from app import app, mysql
import MySQLdb.cursors
import re
import hashlib
from datetime import datetime

@app.route('/')
def index():
    if "loggedin" in session:
        query = '''
            SELECT t.*, c.category_id, c.category_name
            FROM tasks t
            LEFT JOIN task_category tc ON t.id = tc.task_id
            LEFT JOIN category c ON tc.category_id = c.category_id
            WHERE t.archived = FALSE AND t.user_id = %s
            ORDER BY c.category_name, t.title
        '''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (session['id'],))
        tasks = cursor.fetchall()
        # Fetch non-archived tasks from the database
        cursor.execute('SELECT * FROM tasks WHERE archived = FALSE and user_id = %s', (session['id'],)) # get the archived tasks from the session user_id 
        todo_list = cursor.fetchall()
        cursor.execute('SELECT * FROM category') # get the categories from the database
        categories = cursor.fetchall()
        # Organize tasks by category
        categorized_tasks = {}
        for task in tasks:
            category_name = task['category_name'] if task['category_name'] else 'Uncategorized'
            if category_name not in categorized_tasks:
                categorized_tasks[category_name] = []
            categorized_tasks[category_name].append(task)
        return render_template('index.html', username=session['username'], todo_list=todo_list,categories=categories,categorized_tasks=categorized_tasks)
    return redirect('/login')







@app.route("/add", methods=["POST"])
def add():
    """Add a new task
    1- get form data from user
    2-validate form data
    3-insertion to db
    4- ensure its linked to the db 
    - validate it
    """
    try:
        # Get form data
        title = request.form.get("title")
        days = ",".join(request.form.getlist("days"))
        category_id = request.form.get("category_id")

        # Validate all form data at once
        if not all([title, days, category_id]):
            if not title:
                flash("Task title is required.", "error")
            if not days:
                flash("Days of the week are required.", "error")
            if not category_id:
                flash("Category is required.", "error")
            return redirect(url_for("index"))

        # Database operations
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Insert task
            cursor.execute(
                'INSERT INTO tasks(title, Days_of_week, complete, archived, user_id) VALUES (%s, %s, %s, %s, %s)',
                (title, days, False, False, session['id'])
            )
            
            # Link task to category
            task_id = cursor.lastrowid
            cursor.execute(
                'INSERT INTO task_category(task_id, category_id) VALUES(%s, %s)',
                (task_id, category_id)
            )
            print(f"Task {task_id} linked to category {category_id}")
            mysql.connection.commit()
            flash("Task added successfully.", "success")
            
        except MySQLdb.Error as db_error:
            mysql.connection.rollback()
            raise db_error

        return redirect(url_for("index"))

    except MySQLdb.Error as db_error: # handle database errors
        app.logger.error(f"Database error: {db_error}")
        flash("An error occurred while adding the task. Please try again later.", "error")
        return redirect(url_for("index"))
        
    except Exception as e: # handle any other unexpected errors like type or value errors
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for("index"))
        
    finally:
        if 'cursor' in locals(): # check if the cursor is open and close it
            cursor.close() # close the cursor






@app.route("/update/<int:todo_id>")
def update(todo_id):
    """Toggle task completion status"""
    user_id = session['id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks WHERE id = %s and user_id = %s', (todo_id,user_id ,))
    todo = cursor.fetchone()
    print(todo)
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
    return render_template("archive.html", archived_tasks=archived_tasks)

@app.route("/unarchive/<int:todo_id>")
def unarchived_task(todo_id):
    """Unarchive a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET archived = FALSE WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(url_for("view_archived"))

@app.route("/categories")
def view_categories():
    """View all categories and their tasks"""
    try:
         # Debug: Print session data
        print(f"Session data: {session}")

        # Check if the user is logged in
        if "loggedin" not in session:
            print("User not logged in. Redirecting to /login.")
            flash("You need to log in to view categories.", "error")
            return redirect('/login')

        # Validate session['id'] (ensure it's a valid integer)
        if not isinstance(session.get('id'), int):
            print(f"Invalid session ID: {session.get('id')}. Redirecting to /login.")
            flash("Invalid user session. Please log in again.", "error")
            return redirect('/login')
        
        # Create a database cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Execute the query to fetch categories and tasks
        query = '''
            SELECT c.*, 
                   GROUP_CONCAT(t.id) as task_ids,
                   GROUP_CONCAT(t.title) as task_titles,
                   GROUP_CONCAT(t.complete) as task_completes,
                   GROUP_CONCAT(t.Created_at) as task_dates,
                   GROUP_CONCAT(t.Days_of_week) as task_days
            FROM category c
            LEFT JOIN task_category tc ON c.category_id = tc.category_id
            LEFT JOIN tasks t ON tc.task_id = t.id AND t.user_id = %s
            GROUP BY c.category_id
        '''
        print(f"Executing query: {query} with user_id={session['id']}")

        cursor.execute(query, (session['id'],))

        # Fetch all categories result as list of dicts
        categories = cursor.fetchall()

        # Process the results to create a nested structure
        for category in categories:
            if category['task_ids']:
                task_ids = category['task_ids'].split(',')
                task_titles = category['task_titles'].split(',')
                task_completes = category['task_completes'].split(',')
                task_dates = category['task_dates'].split(',')
                task_days = category['task_days'].split(',')

                category['tasks'] = []
                for i in range(len(task_ids)):
                    try:
                        task = {
                            'id': int(task_ids[i]),
                            'title': task_titles[i],
                            'complete': bool(int(task_completes[i])),
                            'Created_at': datetime.strptime(task_dates[i], '%Y-%m-%d %H:%M:%S'),
                            'Days_of_week': task_days[i] if task_days[i] != 'None' else None
                        }
                        category['tasks'].append(task)
                    except (ValueError, IndexError) as e:
                        # Log the error and skip invalid task data
                        app.logger.error(f"Error processing task data: {e}")
                        continue
            else:
                category['tasks'] = []

        return render_template('categories.html', categories=categories)

    except MySQLdb.Error as db_error:
        # Handle database errors
        app.logger.error(f"Database error: {db_error}")
        flash("An error occurred while fetching data. Please try again later.", "error")
        return redirect('/')

    except Exception as e:
        # Handle any other unexpected errors
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/')

    finally:
        # Ensure the cursor is closed
        if 'cursor' in locals():
            cursor.close()

@app.route('/category/add' , methods=[ 'POST'])
def add_category():
    """
    add a new category by sending name from form to the database
    Returns:
        
    """
    try:
        if 'loggedin' not in session: # make sure user must log in to use this didnt expire
            flash("You need to log in to view categories.", "error")
            return redirect('/login')
        
        if not isinstance(session.get('id'), int): # make sure the user id is valid
            flash("Invalid user session. Please log in again.", "error")
            return redirect('/login')
        
        category_name = request.form.get('new_category') # get the name from the form
        if not category_name: # make sure the name is not empty
            flash("Category name is required.", "error")    
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM category WHERE category_name = %s', (category_name,)) # check if the category already exists
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