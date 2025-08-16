# Import Flask class, jsonify function (to return JSON responses), 
# and request object (to handle incoming request data)
from flask import Flask, jsonify, request

# Import CORS (Cross-Origin Resource Sharing) to allow requests from different origins (e.g., frontend on a different port)
from flask_cors import CORS

# Import MongoClient to connect to MongoDB
from pymongo import MongoClient

# Import ObjectId to handle MongoDB's unique document IDs
from bson.objectid import ObjectId


# Create a Flask application instance
app = Flask(__name__)

# Enable CORS for the Flask app so that frontend JavaScript can make requests
CORS(app)


# -------------------------
# MongoDB connection setup
# -------------------------

# Connect to MongoDB server running locally on the default port (27017)
client = MongoClient("mongodb://localhost:27017/")

# Select (or create) a database named "todo_db"
db = client["todo_db"]

# Select (or create) a collection named "todos" inside the "todo_db" database
collection = db["todos"]


# -------------------------
# Route: GET /api/todos
# -------------------------
@app.route('/api/todos', methods=['GET'])  # Define an endpoint for retrieving all todos
def get_todos():
    todos = []  # Create an empty list to store todos
    for todo in collection.find():  # Iterate over all documents in the "todos" collection
        # Append each todo with its ID converted to a string (ObjectId → str) and its task
        todos.append({"id": str(todo["_id"]), "task": todo["task"]})
    # Return the list of todos as JSON
    return jsonify(todos)


# -------------------------
# Route: POST /api/todos
# -------------------------
@app.route('/api/todos', methods=['POST'])  # Define an endpoint for adding a new todo
def add_todo():
    data = request.json  # Get JSON data from the request body
    # Insert a new document into the collection with the provided task
    result = collection.insert_one({"task": data["task"]})
    # Return the inserted todo (with its generated ID) as JSON, and set HTTP status code to 201 (Created)
    return jsonify({"id": str(result.inserted_id), "task": data["task"]}), 201


# -------------------------
# Route: DELETE /api/todos/<id>
# -------------------------
@app.route('/api/todos/<id>', methods=['DELETE'])  # Define an endpoint to delete a todo by its ID
def delete_todo(id):
    # Delete the document where _id matches the provided ObjectId
    collection.delete_one({"_id": ObjectId(id)})
    # Return a confirmation message as JSON
    return jsonify({"message": "Deleted"})


# -------------------------
# Start the Flask app
# -------------------------
if __name__ == '__main__':  # Run this only if the file is executed directly (not imported)
    # Start Flask server on port 5000 with debug mode enabled (auto-reload + error details)
    app.run(port=5000, debug=True)
