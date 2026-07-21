import styles from "./Todo.module.css"
import { FaTrashAlt } from "react-icons/fa"
import { useState } from "react"

export default function Todo({ todo, onDelete, onUpdate }) {
    const { id, text, status } = todo
    const handleChange = (e) => {
        const status = e.target.checked ? "completed" : "active"
        onUpdate({ ...todo, status })

    }
    const handleDelete = () => onDelete(todo)

    return (
        <li className={styles.todo}>
            <input className={styles.checkbox} type="checkbox" id={id} checked={status === "completed"} onChange={handleChange} />
            <label htmlFor={id} className={styles.text}>{text}</label>
            <button className={styles.button} onClick={handleDelete}>
                <FaTrashAlt />
            </button>

        </li>
    )
}

