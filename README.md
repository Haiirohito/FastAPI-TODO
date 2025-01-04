# FastAPI To-Do App

A simple To-Do application built with **FastAPI**, using **SQLAlchemy** for database management, **Jinja2** for templating, and **Passlib** for secure password handling.

---

## Features

- User authentication and session management.
- Create, read, update, and delete (CRUD) operations for to-do items.
- Interactive user interface with Jinja2 templates.
- Secure password storage using `passlib`.
- Built-in session support with Starlette middleware.

---

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database management.
- **Jinja2**: Templating engine for dynamic HTML pages.
- **Passlib**: Library for secure password hashing.
- **Starlette**: Middleware for session management.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/todo-app.git
   cd todo-app
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Apply database migrations:

bash
Copy code
python -m models
Running the Application
Start the FastAPI server:

bash
Copy code
uvicorn main:app --reload
Access the app in your browser:

Go to http://127.0.0.1:8000
Project Structure
graphql
Copy code
todo-app/
│
├── database.py             # Database connection and session setup
├── main.py                 # Main application entry point
├── models.py               # SQLAlchemy models for User and Todo
├── templates/              # HTML templates using Jinja2
├── static/                 # Static files (CSS, JS, images, etc.)
├── requirements.txt        # Python dependencies
├── README.md               # Project README
Environment Variables
Create a .env file in the project root and define the following variables:

env
Copy code
DATABASE_URL=sqlite:///./todo.db
SECRET_KEY=your_secret_key
SESSION_COOKIE_NAME=session
Requirements
Ensure the following are installed:

Python 3.9 or later
pip (Python package installer)
Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add feature').
Push to the branch (git push origin feature-branch).
Create a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
FastAPI documentation: https://fastapi.tiangolo.com
SQLAlchemy documentation: https://docs.sqlalchemy.org
Jinja2 documentation: https://jinja.palletsprojects.com
