from flask import Flask, jsonify, request       # Import Flask for creating the web app, jsonify for sending JSON responses, and request for accessing incoming request data
from flask_cors import CORS                     # Import CORS to allow cross-origin requests (e.g., frontend can call backend from a different domain)
import psycopg2                                 # Import psycopg2 to connect and interact with a PostgreSQL database

app = Flask(__name__)                           # Create an instance of the Flask application
CORS(app)                                       # Enable CORS for this Flask app to allow requests from other domains (frontend apps)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="todo_db",                           # Database name to connect to
    user="postgres",                            # Database username
    password="12162004Hm_runs20",               # Database password (avoid hardcoding in real projects)
    host="localhost"                            # Host where the database is running (localhost means on the same computer)
)
cur = conn.cursor()                             # Create a cursor object to execute SQL queries

# Route to retrieve all todos (HTTP GET request)
@app.route('/api/todos', methods=['GET'])       
def get_todos():                                
    cur.execute("SELECT id, task FROM todos")   # Run SQL query to get all rows with their ID and task from the todos table
    rows = cur.fetchall()                       # Fetch all results from the executed query
    return jsonify([{"id": r[0], "task": r[1]} for r in rows])  # Convert each row into a dictionary and return as JSON

# Route to add a new todo (HTTP POST request)
@app.route('/api/todos', methods=['POST'])      
def add_todo():                                 
    data = request.json                         # Get JSON data from the request body
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id", (data['task'],))  
    # Insert new task into the todos table and return the new row's ID
    todo_id = cur.fetchone()[0]                 # Fetch the ID of the newly inserted todo
    conn.commit()                                # Commit the transaction to save changes
    return jsonify({"id": todo_id, "task": data["task"]}), 201  # Return the new todo as JSON with HTTP status 201 (Created)

# Route to delete a todo by its ID (HTTP DELETE request)
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):                            
    cur.execute("DELETE FROM todos WHERE id = %s", (id,))  # Delete the todo with the given ID
    conn.commit()                                # Commit the transaction to save changes
    return jsonify({"message": "Deleted"})       # Return a JSON message confirming deletion

# Start the Flask application
if __name__ == '__main__':                      
    app.run(port=5000, debug=True)               # Run the app on port 5000 with debug mode enabled (auto-restarts on code changes)
