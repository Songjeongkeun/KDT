import TodoList from "@/components/TodoList";

export default function TodoPage() {
  return (
    <div className="flex flex-1 items-start justify-center bg-zinc-50 px-4 py-12 dark:bg-black">
      <main className="w-full max-w-lg">
        <header className="mb-8">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            Todo
          </h1>
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            할 일을 추가하고 완료 체크, 삭제할 수 있습니다.
          </p>
        </header>
        <TodoList />
      </main>
    </div>
  );
}
