from flask import Flask, jsonify, request, render_template_string  # Import Flask core, JSON helpers, request data handling, and inline template rendering
from flask_cors import CORS  # Import CORS to allow cross-origin requests (important for frontend-backend communication)

app = Flask(__name__)  # Create a Flask application instance
CORS(app)  # Enable CORS for this Flask app so that requests from different origins are allowed

# Initial todo list data stored in memory
todos = [
    {"id": 1, "task": "Buy milk"},  # First todo item
    {"id": 2, "task": "Read book"}  # Second todo item
]

# Function to get the next available todo ID
def get_next_id():
    if todos:  # If there are existing todos
        return max(t["id"] for t in todos) + 1  # Return the maximum ID + 1
    return 1  # If no todos exist, start IDs at 1

# Route to get all todos (READ operation)
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)  # Return todos as JSON

# Route to add a new todo (CREATE operation)
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json  # Get JSON data from the incoming request body
    if not data or "task" not in data:  # If no data or missing 'task' key
        return jsonify({"error": "Task is required"}), 400  # Return error with HTTP 400 Bad Request
    new_todo = {"id": get_next_id(), "task": data['task']}  # Create new todo dictionary
    todos.append(new_todo)  # Add the new todo to the list
    return jsonify(new_todo), 201  # Return the new todo with HTTP 201 Created

# Route to update an existing todo (UPDATE operation)
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json  # Get JSON data from the incoming request body
    if not data or "task" not in data:  # If no data or missing 'task'
        return jsonify({"error": "Task is required"}), 400  # Return error
    for todo in todos:  # Loop through todos
        if todo["id"] == todo_id:  # If matching ID found
            todo["task"] = data['task']  # Update the task field
            return jsonify(todo)  # Return the updated todo
    return jsonify({"error": "Todo not found"}), 404  # If not found, return error

# Route to delete a todo (DELETE operation)
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos  # Declare todos as global so we can reassign it
    if not any(t["id"] == todo_id for t in todos):  # Check if todo exists
        return jsonify({"error": "Todo not found"}), 404  # If not found, return error
    todos = [t for t in todos if t["id"] != todo_id]  # Create new list without the deleted todo
    return jsonify({"message": "Deleted"}), 200  # Return success message

# Optional: Simple frontend for testing (currently unused, but could render HTML)
# render_template_string can be used to send HTML directly without a separate template file

if __name__ == '__main__':  # Run the app only if this script is executed directly
    app.run(debug=True)  # Start the Flask development server with debug mode enabled
