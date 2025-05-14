from flask import Blueprint, render_template, redirect, session, flash
from app import mysql, app
import MySQLdb.cursors
from datetime import datetime

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
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
        return render_template('index.html', email=session['email'], categories_with_tasks=categories_with_tasks, categories=categories)
    return redirect('/login')

@pages_bp.route("/archive")
def view_archived():
    """View archived tasks"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks WHERE archived = TRUE')
    archived_tasks = cursor.fetchall()
    return render_template("archive.html", archived_tasks=archived_tasks)

@pages_bp.route("/about")
def about():
    return render_template("about.html")

@pages_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if "loggedin" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # total tasks
        cursor.execute('SELECT COUNT(*) as active_tasks_count FROM tasks where user_id = %s AND complete = FALSE AND archived = FALSE' , (session['id'],))
        active_tasks_count = cursor.fetchall()
        active_tasks_count = active_tasks_count[0]['active_tasks_count'] if active_tasks_count else 0

        # completed tasks last month
        cursor.execute('SELECT COUNT(*) as completed_tasks_count From tasks where user_id = %s AND complete = True AND Created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)',(session['id'],))
        completed_tasks_last_month = cursor.fetchall()
        completed_tasks_last_month = completed_tasks_last_month[0]['completed_tasks_count'] if completed_tasks_last_month else 0

        # tasks completed last week 
        cursor.execute('''
            SELECT DATE(Created_at) as task_date, COUNT(*) as task_count 
            FROM tasks 
            WHERE user_id = %s AND Created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) AND complete = True 
            GROUP BY DATE(Created_at)
            ORDER BY task_date
        ''', (session['id'],))
        completed_tasks_last_week = cursor.fetchall()
        number_of_completed_tasks_last_week = completed_tasks_last_week[0]['task_count'] if completed_tasks_last_week else 0

        # completed tasks today 
        cursor.execute(
        '''
            SELECT DATE(Created_at) as task_date , COUNT(*) as task_count 
            FROM tasks 
            where user_id =%s AND Created_at >= DATE_SUB(NOW() , INTERVAL 1 DAY) AND complete = True 
            GROUP BY DATE(Created_at)
            ORDER BY task_date
          ''' ,(session['id'],))
        completed_tasks_last_day = cursor.fetchall()
        number_of_completed_tasks_last_day = completed_tasks_last_day[0]['task_count'] if completed_tasks_last_day else 0 

        # username
        cursor.execute('SELECT username FROM user where id = %s',(session['id'],))
        username = cursor.fetchall()
        username = username[0]['username'] if username else None

        return render_template('dashboard.html',
                            username=username,
                            email=session['email'],
                            active_tasks_count=active_tasks_count,
                            number_of_completed_tasks_last_day=number_of_completed_tasks_last_day,
                            completed_tasks_last_week=completed_tasks_last_week,
                            completed_tasks_last_month=completed_tasks_last_month,
                            completed_tasks_last_day=completed_tasks_last_day,
                            number_of_completed_tasks_last_week=number_of_completed_tasks_last_week)
    return redirect('/login') 