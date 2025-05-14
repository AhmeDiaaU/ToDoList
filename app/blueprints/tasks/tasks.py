from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql, app
import MySQLdb.cursors
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/add", methods=["POST"])
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
            return redirect(url_for("pages.index"))

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
            return redirect(url_for("pages.index"))

        return redirect(url_for("pages.index"))

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(url_for("pages.index"))

    finally:
        if 'cursor' in locals():
            cursor.close()

@tasks_bp.route("/update/<int:todo_id>")
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

@tasks_bp.route("/delete/<int:todo_id>")
def delete(todo_id):
    """Delete a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM tasks WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(request.referrer)

@tasks_bp.route("/archive/<int:todo_id>")
def archive(todo_id):
    """Archive a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET archived = TRUE WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(url_for("pages.index"))

@tasks_bp.route("/unarchive/<int:todo_id>")
def unarchive(todo_id):
    """Unarchive a task"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE tasks SET archived = FALSE WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return redirect(url_for("pages.view_archived")) 