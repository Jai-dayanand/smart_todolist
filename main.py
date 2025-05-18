from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add")
def add_task(title: str = Form(...), db: Session = Depends(get_db)):
    new_task = models.Todo(title=title)
    db.add(new_task)
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Todo).get(task_id)
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/toggle/{task_id}")
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Todo).get(task_id)
    if task:
        task.completed = not task.completed
        db.commit()
    return RedirectResponse("/", status_code=303)
