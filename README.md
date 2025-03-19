# Flask Todo Application

A feature-rich task management web application built with Flask, SQLAlchemy, and Semantic UI. This application allows users to create, manage, and organize their daily tasks with an intuitive dark-themed interface.

## Features

- Create and manage tasks
- Mark tasks as complete/incomplete
- Archive completed tasks for better organization
- Assign tasks to specific days of the week
- Track task creation dates
- View archived tasks separately
- Responsive design with dark theme
- About page with developer information

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Semantic UI
- **Template Engine**: Jinja2

## Project Structure

```
flask-todo/
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── static/
│   ├── css/
│   │   ├── about.css
│   │   ├── cards.css
│   │   ├── forms.css
│   │   └── main.css
│   └── images/
├── templates/
│   ├── about.html
│   ├── archive.html
│   ├── base.html
│   ├── index.html
│   └── partials/
│       ├── _form.html
│       └── _task.html
├── about.py
├── config.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AhmeDiaaU/FlaskTodo.git
   cd FlaskTodo
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install flask flask-sqlalchemy
   ```

4. Initialize the database:
   ```
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. Run the application:
   ```
   python run.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Adding Tasks
1. Enter a task title in the input field
2. Optionally select days of the week for the task
3. Click the "Add Task" button

### Managing Tasks
- Click the checkmark icon to mark a task as complete
- Click the archive icon to move a task to the archive
- Click the trash icon to delete a task permanently

### Viewing Archives
- Click on "Archive" in the navigation menu to view archived tasks
- Archived tasks can be unarchived or deleted

## Application Screenshots

### Active Tasks
![Active Tasks](https://github.com/AhmeDiaaU/ToDoList/blob/main/app/static/images/active-tasks.png)

### Archived Tasks
![Archived Tasks](https://github.com/AhmeDiaaU/ToDoList/blob/main/app/static/images/archived-tasks.png)

## Developer

**Ahmed Diaa**
- GitHub: [AhmeDiaaU](https://github.com/AhmeDiaaU)
- LinkedIn: [Ahmed Diaa](https://www.linkedin.com/in/ahmed-diaa-76669b2b8/)
- Email: ahmeddeya58@gmail.com

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
