from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from repository import (
    init_db,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)

app = FastAPI()

init_db()  # connects to Postgres, creates the table if missing, seeds if empty

class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    row = get_task_by_id(task_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return row

@app.post("/tasks", status_code=201)
def create_new_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required")
    return create_task(task.title)

@app.put("/tasks/{task_id}")
def update_existing_task(task_id: int, update: TaskUpdate):
    existing = get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    new_title = existing["title"]
    new_done = existing["done"]

    if update.title is not None:
        if not update.title.strip():
            raise HTTPException(status_code=400, detail="title cannot be empty")
        new_title = update.title

    if update.done is not None:
        new_done = update.done

    return update_task(task_id, new_title, new_done)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_existing_task(task_id: int):
    existing = get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    delete_task(task_id)
    return Response(status_code=204)