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

2. Create and Activate a virual environment
   ```bash
   python -m venv {virtual environment name}
   source {virtual environment name}/bin/activate   # On windows use: {virtual environment name}\Scripts\activate

3. Install the dependencies:
   ```bash
   pip install -r requirments.txt

---

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload

2. Access the app in your browser: Go to http://127.0.0.1:8000

---

## Requirments

Ensure the following are installed:

1. Python 3.9 or later
2. pip (Python package installer)

---

## Acknowledgments

- **FastAPI documentation**: https://fastapi.tiangolo.com
- **SQLAlchemy documentation**: https://docs.sqlalchemy.org
- **jinja2 documentation**: https://jinja.palletsprojects.com
