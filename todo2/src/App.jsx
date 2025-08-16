import { useEffect, useState } from "react";

const API_URL = "http://localhost:3000/api/todos";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState("");

  useEffect(() => {
    fetchTodos();
  }, []);

  async function fetchTodos() {
    const res = await fetch(API_URL);
    const data = await res.json();
    setTodos(data);
  }

  async function addTodo() {
    if (!task.trim()) return;
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task })
    });
    setTask("");
    fetchTodos();
  }

  async function deleteTodo(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    fetchTodos();
  }

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "20px" }}>Todo List</h1>
      <div style={{ display: "flex", marginBottom: "20px" }}>
        <input
          type="text"
          value={task}
          onChange={e => setTask(e.target.value)}
          placeholder="Enter a task"
          style={{ flexGrow: 1, padding: "10px", border: "1px solid #ccc", borderRadius: "4px 0 0 4px" }}
        />
        <button
          onClick={addTodo}
          style={{ padding: "10px 20px", border: "none", background: "blue", color: "white", borderRadius: "0 4px 4px 0", cursor: "pointer" }}
        >
          Add
        </button>
      </div>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {todos.map(todo => (
          <li key={todo.id} style={{ display: "flex", justifyContent: "space-between", padding: "10px", background: "#f5f5f5", borderRadius: "4px", marginBottom: "10px" }}>
            <span>{todo.task}</span>
            <button
              onClick={() => deleteTodo(todo.id)}
              style={{ background: "red", color: "white", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer" }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
