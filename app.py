from fastapi import FastAPI, Depends, Request, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
import models
from models import User, Todo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="!secret")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Password verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Retrieve user by username
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# Authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


# ------------------- Routes -------------------


@app.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    logged_in = "user" in req.session if hasattr(req, "session") else False
    session_user = req.session["user"] if logged_in else None

    user = None
    if session_user and isinstance(session_user, dict):
        username = session_user.get("username")
        if username:
            user = db.query(User).filter(User.username == username).first()

    todos = []
    if user:
        todos = db.query(Todo).filter(Todo.user_id == user.id).all()

    # Format dates
    for task in todos:
        task.dueDate = task.dueDate.strftime("%Y-%m-%d")

    pending_tasks = [
        task
        for task in todos
        if not task.status
        and datetime.strptime(task.dueDate, "%Y-%m-%d") >= datetime.now()
    ]
    completed_tasks = [task for task in todos if task.status]
    overdue_tasks = [
        task
        for task in todos
        if not task.status
        and datetime.strptime(task.dueDate, "%Y-%m-%d") < datetime.now()
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": req,
            "logged_in": logged_in,
            "user": {"id": user.id, "username": user.username} if user else None,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
        },
    )


@app.get("/login")
async def login(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})


@app.post("/token")
async def login_for_access_token(
    req: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid credentials"},
        )

    req.session["user"] = {"id": user.id, "username": user.username}
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/logout")
async def logout(req: Request):
    req.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/sign_up")
async def signup(req: Request):
    return templates.TemplateResponse("sign_up.html", {"request": req})


@app.post("/sign_up")
async def signup_post(
    req: Request,  # Add Request instance here
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Check if passwords match
    if password != confirm_password:
        return templates.TemplateResponse(
            "sign_up.html",
            {
                "request": req,  # Use the instance `req` here
                "error": "Passwords do not match",
                "username": username,
                "email": email,
            },
        )

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create a new user
    new_user = models.User(
        username=username, email=email, hashed_password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as e:
        db.rollback()
        return templates.TemplateResponse(
            "sign_up.html",
            {
                "request": req,  # Use the instance `req` here
                "error": "An error occurred while creating the account. Please try again.",
                "username": username,
                "email": email,
            },
        )


@app.get("/new_task")
async def get_new_task_page(req: Request):
    return templates.TemplateResponse("new_task.html", {"request": req})


@app.post("/new_task")
async def newTask(
    req: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(None),
    due_date: str = Form(...),
):
    if not title or not due_date:
        return templates.TemplateResponse(
            "new_task.html",
            {"request": req, "error": "Title and Due Date are required"},
        )

    user = req.session["user"] if "user" in req.session else None
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    new_task = models.Todo(
        title=title,
        description=description,
        status=False,
        dueDate=datetime.strptime(due_date, "%Y-%m-%d"),
        user_id=user["id"],
    )

    try:
        db.add(new_task)
        db.commit()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)}
        )


@app.post("/complete_task/{task_id}")
async def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Todo).filter(models.Todo.id == task_id).first()
    if task:
        task.status = True
        db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/delete_task/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Todo).filter(models.Todo.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/profile/{user_id}")
async def profile(
    req: Request, user_id: int, db: Session = Depends(get_db), logged_in: bool = True
):
    user = db.query(User).filter(User.id == user_id).first()

    # Get user details
    user_details = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    # Retrieve all tasks
    tasks = db.query(Todo).filter(Todo.user_id == user.id).all()

    # Count tasks based on their status
    completed_tasks = [task for task in tasks if task.status]
    pending_tasks = [
        task for task in tasks if not task.status and task.dueDate >= datetime.now()
    ]
    overdue_tasks = [
        task for task in tasks if not task.status and task.dueDate < datetime.now()
    ]

    # Prepare task counts
    completed_count = len(completed_tasks)
    pending_count = len(pending_tasks)
    overdue_count = len(overdue_tasks)

    # Calculate the percentage for each task type
    total_tasks = completed_count + pending_count + overdue_count
    completed_percentage = (completed_count / total_tasks) * 100 if total_tasks else 0
    pending_percentage = (pending_count / total_tasks) * 100 if total_tasks else 0
    overdue_percentage = (overdue_count / total_tasks) * 100 if total_tasks else 0

    # Pass data to the template
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": req,
            "user": user_details,
            "logged_in": logged_in,
            "completed_count": completed_count,
            "pending_count": pending_count,
            "overdue_count": overdue_count,
            "completed_percentage": completed_percentage,
            "pending_percentage": pending_percentage,
            "overdue_percentage": overdue_percentage,
        },
    )
