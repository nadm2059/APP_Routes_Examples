# Import the FastAPI class to create a web application
from fastapi import FastAPI  

# Import CORS middleware to allow cross-origin requests from the frontend
from fastapi.middleware.cors import CORSMiddleware  

# Import BaseModel from Pydantic for defining request/response data structures
from pydantic import BaseModel  

# Import List type hint for specifying lists in function return types
from typing import List  

# Import MongoClient to connect to MongoDB
from pymongo import MongoClient  

# Import ObjectId to work with MongoDB document IDs
from bson.objectid import ObjectId  


# Create a new FastAPI application instance
app = FastAPI()  

# Add CORS middleware to allow requests from any origin, any method, and any header
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)  


# Create a MongoDB client and connect to the local MongoDB server
client = MongoClient("mongodb://localhost:27017/")  

# Select (or create if not exists) the database named "todo_db"
db = client["todo_db"]  

# Select (or create if not exists) the collection named "todos"
collection = db["todos"]  


# Define the response model for a Todo item (output format)
class TodoOut(BaseModel):
    id: str   # The unique ID of the todo (as a string)
    task: str # The text description of the todo task


# Define the request model for creating a Todo item (input format)
class TodoIn(BaseModel):
    task: str # The text description of the todo task


# Route: GET /api/todos → Returns a list of all todos
@app.get("/api/todos", response_model=List[TodoOut])
def get_todos():
    todos = []  # Initialize an empty list to store todos
    for todo in collection.find():  # Iterate over all documents in the "todos" collection
        # Append each todo as a dictionary with string ID and task text
        todos.append({"id": str(todo["_id"]), "task": todo["task"]})
    return todos  # Return the list of todos


# Route: POST /api/todos → Adds a new todo to the database
@app.post("/api/todos", response_model=TodoOut)
def add_todo(todo: TodoIn):
    # Insert the new todo into MongoDB and store the result
    result = collection.insert_one({"task": todo.task})
    # Return the inserted todo with its generated ID
    return {"id": str(result.inserted_id), "task": todo.task}


# Route: DELETE /api/todos/{todo_id} → Deletes a todo by its ID
@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str):
    # Convert the string ID to an ObjectId and delete the document
    collection.delete_one({"_id": ObjectId(todo_id)})
    # Return a success message
    return {"message": "Deleted"}
