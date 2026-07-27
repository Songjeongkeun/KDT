"use client";

import type { Todo } from "@/types/todo";

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function TodoItem({ todo, onToggle, onDelete }: TodoItemProps) {
  return (
    <li className="flex items-center gap-3 rounded-lg border border-zinc-200 bg-white px-4 py-3 shadow-sm transition-colors hover:border-zinc-300 dark:border-zinc-700 dark:bg-zinc-900 dark:hover:border-zinc-600">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        className="h-4 w-4 shrink-0 cursor-pointer rounded border-zinc-300 text-zinc-900 focus:ring-zinc-500 dark:border-zinc-600 dark:bg-zinc-800"
        aria-label={`${todo.text} 완료 여부`}
      />
      <span
        className={`flex-1 text-sm ${
          todo.completed
            ? "text-zinc-400 line-through dark:text-zinc-500"
            : "text-zinc-900 dark:text-zinc-100"
        }`}
      >
        {todo.text}
      </span>
      <button
        type="button"
        onClick={() => onDelete(todo.id)}
        className="shrink-0 rounded-md px-2 py-1 text-xs font-medium text-red-600 transition-colors hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-950/30"
        aria-label={`${todo.text} 삭제`}
      >
        삭제
      </button>
    </li>
  );
}
