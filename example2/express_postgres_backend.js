// Import the Express framework to create a web server
const express = require("express");

// Import CORS middleware to allow cross-origin requests (frontend on a different port)
const cors = require("cors");

// Import Pool from 'pg' to interact with PostgreSQL databases
const { Pool } = require("pg");

// Create a new Express application
const app = express();

// Enable CORS for all routes so frontend requests from other origins are allowed
app.use(cors());

// Enable parsing of JSON bodies in incoming requests
app.use(express.json());

// Create a new PostgreSQL connection pool with configuration
const pool = new Pool({
    user: "postgres",           // PostgreSQL username
    host: "localhost",          // Host where PostgreSQL is running
    database: "todo_db",        // Database name
    password: "12162004Hm_runs20", // Database password
    port: 5432                  // PostgreSQL port (default 5432)
});

// Define a GET route to fetch all todos from the database
app.get("/api/todos", async (req, res) => {
    // Execute a query to get id and task from the todos table
    const result = await pool.query("SELECT id, task FROM todos");

    // Send the query results as JSON to the client
    res.json(result.rows);
});

// Define a POST route to create a new todo
app.post("/api/todos", async (req, res) => {
    // Execute an INSERT query to add a new todo and return the generated id
    const result = await pool.query(
        "INSERT INTO todos (task) VALUES ($1) RETURNING id",
        [req.body.task]  // $1 is replaced with the task value from the request body
    );

    // Respond with the new todo's id and task in JSON format, status 201 = Created
    res.status(201).json({ id: result.rows[0].id, task: req.body.task });
});

// Define a DELETE route to remove a todo by id
app.delete("/api/todos/:id", async (req, res) => {
    // Execute a DELETE query using the id from the URL parameter
    await pool.query("DELETE FROM todos WHERE id = $1", [req.params.id]);

    // Respond with a JSON message confirming deletion
    res.json({ message: "Deleted" });
});

// Start the server and listen on port 3000; log a message when ready
app.listen(3000, () => console.log("PostgreSQL Express server running on port 3000"));
