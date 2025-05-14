from flask import Blueprint, request, redirect, url_for, session, flash
from app import mysql, app
import MySQLdb.cursors

categories_bp = Blueprint('categories', __name__, url_prefix='/category')

@categories_bp.route('/add', methods=['POST'])
def add_category():
    """
    add a new category by sending name from form to the database
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
        return redirect(url_for("pages.index"))
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/')

@categories_bp.route('/delete/<int:category_id>', methods=['POST'])
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
        return redirect(url_for("pages.index"))
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect('/') 