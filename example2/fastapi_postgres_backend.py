# Import FastAPI framework for building the API
from fastapi import FastAPI

# Import middleware to handle CORS (Cross-Origin Resource Sharing)
from fastapi.middleware.cors import CORSMiddleware

# Import BaseModel from Pydantic to define data schemas for requests/responses
from pydantic import BaseModel

# Import List type for type hinting
from typing import List

# Import psycopg2 to connect and interact with PostgreSQL
import psycopg2

# Create a FastAPI app instance
app = FastAPI()

# Add CORS middleware to allow frontend apps (running on different origins) to access this API
app.add_middleware(
    CORSMiddleware,                  # Middleware class
    allow_origins=["*"],              # Allow requests from any origin (* means all)
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"]               # Allow all headers
)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="todo_db",                 # Name of the database
    user="postgres",                  # Database username
    password="12162004Hm_runs20",          # Database password (replace with your actual password)
    host="localhost"                  # Database host (localhost if running locally)
)

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Define the schema for output data (used in API responses)
class TodoOut(BaseModel):
    id: int                           # ID of the todo item (integer)
    task: str                         # Task description (string)

# Define the schema for input data (used in API requests)
class TodoIn(BaseModel):
    task: str                         # Task description (string)

# Define a GET endpoint to retrieve all todos
@app.get("/api/todos", response_model=List[TodoOut])  # Returns a list of TodoOut objects
def get_todos():
    cur.execute("SELECT id, task FROM todos")         # SQL query to get all todos
    rows = cur.fetchall()                             # Fetch all rows from the query result
    return [{"id": r[0], "task": r[1]} for r in rows]  # Convert rows into list of dictionaries

# Define a POST endpoint to add a new todo
@app.post("/api/todos", response_model=TodoOut)       # Returns the created TodoOut object
def add_todo(todo: TodoIn):
    cur.execute(                                       # SQL insert query
        "INSERT INTO todos (task) VALUES (%s) RETURNING id", 
        (todo.task,)                                   # Pass task value as a tuple
    )
    todo_id = cur.fetchone()[0]                        # Get the generated ID from RETURNING
    conn.commit()                                      # Commit changes to database
    return {"id": todo_id, "task": todo.task}          # Return new todo as dictionary

# Define a DELETE endpoint to remove a todo by ID
@app.delete("/api/todos/{todo_id}")                    # Path parameter {todo_id}
def delete_todo(todo_id: int):
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))  # SQL delete query
    conn.commit()                                      # Commit changes to database
    return {"message": "Deleted"}                      # Return success message
