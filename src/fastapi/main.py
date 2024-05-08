from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class Status(str, Enum):
    not_started = "Not Started"
    in_progress = "In Progress"
    done = "Done"

class TodoItem(BaseModel):
    id: int
    title: str
    status: Status = Status.not_started

app = FastAPI()
todo_db = []  # This will act as a simple database.

@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todo_db.append(todo)
    return todo

@app.get("/todos/", response_model=List[TodoItem])
def get_todos():
    return todo_db

@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo_by_id(todo_id: int):
    for todo in todo_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            return todo_db.pop(index)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/status/{status}", response_model=List[TodoItem])
def get_todos_by_status(status: Status):
    return [todo for todo in todo_db if todo.status == status]

@app.patch("/todos/{todo_id}/status", response_model=TodoItem)
def update_todo_status(todo_id: int, status: Status):
    for todo in todo_db:
        if todo.id == todo_id:
            todo.status = status
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/title/", response_model=List[TodoItem])
def get_todo_by_title(title: str = Query(..., description="The title of the todo to search for")):
    filtered_todos = [todo for todo in todo_db if todo.title.lower() == title.lower()]
    if not filtered_todos:
        raise HTTPException(status_code=404, detail="No todo found with the specified title")
    return filtered_todos

@app.delete("/todos/title/", response_model=List[TodoItem])
def delete_todo_by_title(title: str = Query(..., description="The title of the todo to delete")):
    global todo_db
    original_length = len(todo_db)
    todo_db = [todo for todo in todo_db if todo.title.lower() != title.lower()]
    if len(todo_db) == original_length:
        raise HTTPException(status_code=404, detail="No todo found with the specified title")
    return todo_db

@app.delete("/todos/status/", response_model=List[TodoItem])
def delete_todos_by_status(status: Status = Query(..., description="The status of the todos to delete")):
    global todo_db
    original_length = len(todo_db)
    todo_db = [todo for todo in todo_db if todo.status != status]
    if len(todo_db) == original_length:
        raise HTTPException(status_code=404, detail="No todos found with the specified status")
    return todo_db

@app.delete("/todos/", response_model=List[TodoItem])
def delete_all_todos():
    global todo_db
    todo_db.clear() 
    return todo_db
  