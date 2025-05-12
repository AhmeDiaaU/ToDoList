# ToDoList Project

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge&logo=github&logoColor=white) ![HTML](https://img.shields.io/badge/HTML-39.9%25-orange.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-31.2%25-blue.svg?style=for-the-badge&logo=css3&logoColor=white) ![Python](https://img.shields.io/badge/Python-27.6%25-yellow.svg?style=for-the-badge&logo=python&logoColor=white) ![Mako](https://img.shields.io/badge/Mako-1.3%25-green.svg?style=for-the-badge&logo=mako&logoColor=white)

The **ToDoList** project is a web-based application designed to help users manage their daily tasks efficiently. Built with Flask (Python), HTML, CSS, and Mako templates, it provides a responsive, user-friendly interface for task management, with data stored in a MySQL database.

![ToDoList App Screenshot]([https://github.com/AhmeDiaaU/ToDoList/blob/v2/app/static/images/Screenshot%202025-03-20%20095911.png?raw=true](https://github.com/AhmeDiaaU/ToDoList/blob/main/images/Screenshot%20from%202025-05-12%2005-50-12.png))

## 🚀 Features

- Add new tasks with categories and days of the week
- Update task completion status (mark as complete/incomplete)
- Delete tasks
- Archive and unarchive tasks
- Categorize tasks and view them by category
- User authentication (register, login, logout)
- Responsive design with a dark red-black theme

## 🛠️ How It Works

- **Add Task:** Users can add a task via a modal, specifying the title, days of the week, and category.
- **Update Task Status:** Toggle a task's completion status with a button.
- **Delete Task:** Remove a task permanently from the list.
- **Archive Task:** Move a task to the archive; unarchive it later if needed.
- **Categorize Tasks:** Assign tasks to categories and view them grouped by category.
- **User Authentication:** Register and log in to manage personal tasks securely.
- **Responsive UI:** The app adapts to different screen sizes with a consistent dark theme.

## 📜 Commands

| Command          | Description                     | Example                          |
|------------------|---------------------------------|----------------------------------|
| `Add Task`       | Add a new task via modal        | `Add Task: "Finish report" (Mon, Wed), Category: Work` |
| `Toggle Status`  | Mark a task as complete/incomplete | `Toggle Status: Finish report`   |
| `Delete Task`    | Remove a task                   | `Delete Task: Finish report`     |
| `Archive Task`   | Archive a task                  | `Archive Task: Finish report`    |
| `Unarchive Task` | Restore an archived task        | `Unarchive Task: Finish report`  |
| `Add Category`   | Add a new category              | `Add Category: Personal`         |
| `View Categories`| View tasks grouped by category  | `View Categories`                |

## 💻 Code Highlights

### Key Routes

| Route/Method          | Description                              |
|-----------------------|------------------------------------------|
| `/add`                | Adds a new task to the database          |
| `/update/<int:todo_id>` | Toggles a task's completion status       |
| `/delete/<int:todo_id>` | Deletes a task by its ID                 |
| `/archive/<int:todo_id>`| Archives a task by its ID                |
| `/unarchive/<int:todo_id>` | Unarchives a task by its ID           |
| `/category/add`       | Adds a new category                      |
| `/categories`         | Displays tasks grouped by category       |
| `/login/register`     | Registers a new user                     |
| `/login/`             | Handles user login                       |
| `/login/logout`       | Logs out the current user                |
| `/dashboard`       | Dashboard tracking production                |

## 📂 Project Structure

- **Flask Application (`app/`):**
  - `routes.py`: Defines all routes and logic for task management, user authentication, and category handling.
  - `app.py`: Initializes the Flask app and MySQL connection.
- **Templates (`templates/`):**
  - `base.html`: Base template with navigation and layout.
  - `index.html`: Displays active tasks grouped by category.
  - `archive.html`: Shows archived tasks.
  - `categories.html`: Displays tasks by category.
  - `about.html`: About page with project details.
  - `login.html` & `register.html`: User authentication pages.
  - `partials/_task.html`: Reusable task card component.
  - `dashboard.html`: Tracking progress
- **Static Files (`static/`):**
  - `css/`: Stylesheets (`main.css`, `cards.css`, `forms.css`, `about.css` , `dashboard.css` ,`info.css` :) for the dark blue-black theme.
  - `images/`: Profile image for the about page.
- **Database:** MySQL database with tables for tasks, categories, task-category relationships, and user accounts.

## 📚 Future Enhancements

- **Due Dates:** Add functionality to set and track due dates for tasks.[x]
- **Task Prioritization:** Allow users to assign priority levels to tasks.
- **Notifications:** Implement email or in-app reminders for upcoming tasks.
- **Task Search:** Add a search feature to find tasks by title or category.
- **Task Sorting:** Enable sorting tasks by creation date, status, or category.[x]
- **User Profiles:** Allow users to update their profile information.

## 📧 Contact

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ahmed-diaa-76669b2b8/)  
[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AhmeDiaaU)

---

**Ahmed Diaa**  
**Faculty of Computers and Artificial Intelligence**  
**Assiut National University**
