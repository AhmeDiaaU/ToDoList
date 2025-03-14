from flask import render_template, request, redirect, url_for
from app.models import Todo
from app import app, db

@app.route('/')
def index():
    #show to do 
    todo_list = Todo.query.filter_by(archived = False).all()
    print(todo_list)
    return render_template('index.html' , todo_list = todo_list)
@app.route("/add", methods = ["POST"])
def add():
    """
    add new item
    """
    title = request.form.get("title")
    days =request.form.get("days" , "")
    new_todo = Todo(title = title,
                    Days_of_week = days,
                    complete = False , 
                    archived = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(request.referrer)
@app.route("/update/<int:todo_id>")
def update(todo_id):  
    """
    Update new item
    """
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(request.referrer)
@app.route("/delete/<int:todo_id>")
def delete(todo_id): 
    """
    Delete new item
    """
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(request.referrer) # to redirect it to the same place
@app.route("/archive/<int:todo_id>")
def archive(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.archived = True
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/archive")
def view_archived():
    archived_tasks = Todo.query.filter_by(archived= True).all() # return the Completed Archived Task
    return render_template("archive.html" , archived_tasks = archived_tasks)
@app.route("/unarchive/<int:todo_id>")
def unarchived_task(todo_id):
    todo = Todo.query.get(todo_id)
    if todo :
        todo.archived = False
        db.session.commit()
    return redirect(url_for("view_archived"))
@app.route("/about")
def about():
    return render_template("about.html")