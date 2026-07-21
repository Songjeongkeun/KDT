import styles from "./TodoList.module.css"
import AddTodo from "../addtodo/AddTodo"
import { useEffect, useState } from "react"
import Todo from "../todo/Todo"

function readTodosFromLocalStorage() {
    const todos = localStorage.getItem("todos")
    return todos ? JSON.parse(todos) : []
}

function getFilteredItems(todos, filter) {
    if (filter === "all") {
        return todos
    }
    return todos.filter((todo) => todo.status === filter)
}

export default function TodoList({ filter }) {
    const [todos, setTodos] = useState(() => readTodosFromLocalStorage())
    const handleAdd = (todo) => setTodos([...todos, todo])
    const handleUpdate = (updated) => setTodos(todos.map((t) => (t.id === updated.id ? updated : t)))
    const handleDelete = (deleted) => setTodos(todos.filter((t) => t.id !== deleted.id))

    const filtered = getFilteredItems(todos, filter)

    useEffect(() => {
        localStorage.setItem("todos", JSON.stringify(todos))
    }, [todos])

    return (
        <section className={styles.container}>
            <ul className={styles.list}>
                {filtered.map((item) => (
                    <Todo key={item.id} todo={item} onDelete={handleDelete} onUpdate={handleUpdate} />
                ))}
            </ul>
            <AddTodo onAdd={handleAdd} />
        </section>
    )
}