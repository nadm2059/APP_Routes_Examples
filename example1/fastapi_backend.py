from fastapi import FastAPI  # Import FastAPI framework
from pydantic import BaseModel  # Import BaseModel for defining data schemas
from typing import List  # Import List type hint for defining lists of objects
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware to allow cross-origin requests

app = FastAPI()  # Create a FastAPI application instance

# Add middleware to handle Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,  # Use CORS middleware
    allow_origins=["*"],  # Allow requests from all domains ("*" means no restrictions)
    allow_credentials=True,  # Allow cookies and authentication credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all HTTP headers
)

# Pydantic model for a Todo item (full representation with ID)
class Todo(BaseModel):
    id: int  # ID of the todo item
    task: str  # Description of the task

# Pydantic model for creating a new Todo (without ID, since server generates it)
class TodoCreate(BaseModel):
    task: str  # Task description

# Initial in-memory list of todos
todos = [
    Todo(id=1, task="Buy milk"),  # First todo item
    Todo(id=2, task="Read book")  # Second todo item
]

# GET endpoint to return all todos
@app.get("/api/todos", response_model=List[Todo])  # Returns a list of Todo objects
def get_todos():
    return todos  # Return the in-memory todos list

# POST endpoint to add a new todo
@app.post("/api/todos", response_model=Todo)  # Returns the newly created Todo object
def add_todo(todo: TodoCreate):  # Accepts TodoCreate object as request body
    new_todo = Todo(id=len(todos) + 1, task=todo.task)  # Assign new ID and set task
    todos.append(new_todo)  # Add the new todo to the list
    return new_todo  # Return the created todo

# PUT endpoint to update an existing todo
@app.put("/api/todos/{todo_id}", response_model=Todo)  # Returns the updated Todo object
def update_todo(todo_id: int, todo: TodoCreate):  # Takes todo_id from URL and new data from request body
    for t in todos:  # Loop through todos
        if t.id == todo_id:  # If matching ID found
            t.task = todo.task  # Update the task description
            return t  # Return the updated todo
    return {"error": "Todo not found"}  # Return error if todo does not exist

# DELETE endpoint to remove a todo
@app.delete("/api/todos/{todo_id}")  # No specific response model; returns a message
def delete_todo(todo_id: int):  # Takes todo_id from URL
    global todos  # Declare todos as global to modify it
    todos = [t for t in todos if t.id != todo_id]  # Keep all todos except the one with matching ID
    return {"message": "Deleted"}  # Return confirmation message
