const express = require('express'); // Import Express framework
const cors = require('cors'); // Import CORS middleware for cross-origin requests
const app = express(); // Create an Express app instance

app.use(cors()); // Enable CORS so frontend can talk to backend
app.use(express.json()); // Parse incoming JSON request bodies

// In-memory todo list
let todos = [
    { id: 1, task: "Buy milk" }, // First todo
    { id: 2, task: "Read book" } // Second todo
];

// GET endpoint to return all todos
app.get('/api/todos', (req, res) => {
    res.json(todos); // Send todos as JSON
});

// POST endpoint to add a new todo
app.post('/api/todos', (req, res) => {
    const newTodo = { id: todos.length + 1, task: req.body.task }; // Create todo with new ID
    todos.push(newTodo); // Add to list
    res.status(201).json(newTodo); // Return new todo with HTTP 201 Created
});

// PUT endpoint to update an existing todo
app.put('/api/todos/:id', (req, res) => {
    const todo = todos.find(t => t.id == req.params.id); // Find todo by ID
    if (!todo) return res.status(404).json({ error: 'Todo not found' }); // If not found, return 404
    todo.task = req.body.task; // Update task description
    res.json(todo); // Return updated todo
});

// DELETE endpoint to remove a todo
app.delete('/api/todos/:id', (req, res) => {
    todos = todos.filter(t => t.id != req.params.id); // Keep all except deleted one
    res.json({ message: 'Deleted' }); // Return confirmation
});

// Start server on port 3000
app.listen(3000, () => console.log('Server running on port 3000'));
