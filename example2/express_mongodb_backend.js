// Import the Express framework to create a web server
const express = require("express");

// Import CORS middleware to allow cross-origin requests (frontend on a different port)
const cors = require("cors");

// Import MongoClient and ObjectId from the mongodb package
// MongoClient allows connecting to MongoDB, ObjectId is used to handle MongoDB document IDs
const { MongoClient, ObjectId } = require("mongodb");

// Create a new Express application
const app = express();

// Enable CORS for all routes so frontend requests from other origins are allowed
app.use(cors());

// Enable parsing of JSON bodies in incoming requests
app.use(express.json());

// MongoDB connection URL
const url = "mongodb://localhost:27017";

// Create a new MongoClient instance to connect to MongoDB
const client = new MongoClient(url);

// Variable to hold the collection reference
let collection;

// Immediately Invoked Async Function to connect to MongoDB
(async () => {
    // Connect to the MongoDB server
    await client.connect();

    // Select the database "todo_db" and the "todos" collection
    collection = client.db("todo_db").collection("todos");
})();

// Define a GET route to fetch all todos from the MongoDB collection
app.get("/api/todos", async (req, res) => {
    // Retrieve all documents from the collection as an array
    const todos = await collection.find().toArray();

    // Map the MongoDB _id field to "id" for frontend usage and send as JSON
    res.json(todos.map(t => ({ id: t._id, task: t.task })));
});

// Define a POST route to create a new todo
app.post("/api/todos", async (req, res) => {
    // Insert a new document with the task from the request body
    const result = await collection.insertOne({ task: req.body.task });

    // Respond with the new todo's ID and task, status 201 = Created
    res.status(201).json({ id: result.insertedId, task: req.body.task });
});

// Define a DELETE route to remove a todo by ID
app.delete("/api/todos/:id", async (req, res) => {
    // Delete the document matching the ObjectId from the URL parameter
    await collection.deleteOne({ _id: new ObjectId(req.params.id) });

    // Respond with a JSON message confirming deletion
    res.json({ message: "Deleted" });
});

// Start the server and listen on port 3000; log a message when ready
app.listen(3000, () => console.log("MongoDB Express server running on port 3000"));
