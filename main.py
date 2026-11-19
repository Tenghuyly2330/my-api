from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Task Api")

class Task(BaseModel):
    title: str
    completed: bool = False


tasks = {
    1: {"title": "Set up Python API", "completed": True},
    2: {"title": "Test endpoints", "completed": False},
}

@app.get("/")
def home():
    return {
        "message": "Welcome to api",
        "status": "Running successfully"
    }

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "service": "Banking API"
    }


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_tasks(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task Not Found")
    return tasks[task_id]

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    new_id = max(tasks.keys(), default=0) + 1
    tasks[new_id] = task.model_dump()
    return {"id": new_id, **tasks[new_id]}

@app.delete("/tasks/{task_id}")
def delete_tasks(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted = tasks.pop(task_id)
    return {"deleted": deleted}