# [38일차] React - TodoList 프로젝트 정리

## 1. 이번 정리에서 다루는 내용

이번 내용은 37일차에 정리한 Context API, React Router, CSS Module 기본 개념과 겹치지 않는 내용을 중심으로 정리한다.

주요 내용은 다음과 같다.

- TodoList 프로젝트 구조
- 컴포넌트 역할 분리
- Todo 데이터 구조
- `uuid`를 이용한 고유 id 생성
- controlled component 입력 처리
- Todo 추가
- Todo 완료 상태 변경
- Todo 삭제
- 필터링 기능
- `localStorage`를 이용한 Todo 저장
- 배열 상태를 불변하게 변경하는 방법
- 체크박스와 `label` 연결
- `react-icons` 사용
- CSS 변수를 이용한 테마 관리

---

## 2. TodoList 프로젝트 구조

TodoList 프로젝트는 하나의 큰 컴포넌트에 모든 코드를 작성하지 않고, 역할에 따라 컴포넌트를 나누어 구성한다.

```text
src
├── App.jsx
├── App.css
├── main.jsx
├── index.css
├── context
│   └── DarkmodeContext.jsx
└── components
    ├── header
    │   ├── Header.jsx
    │   └── Header.module.css
    ├── addtodo
    │   ├── AddTodo.jsx
    │   └── AddTodo.module.css
    ├── todolist
    │   ├── TodoList.jsx
    │   └── TodoList.module.css
    └── todo
        ├── Todo.jsx
        └── Todo.module.css
```

각 컴포넌트의 역할은 다음과 같다.

| 컴포넌트 | 역할 |
|---|---|
| `App` | 전체 앱의 최상위 컴포넌트다. 필터 상태를 관리하고 주요 컴포넌트를 연결한다. |
| `Header` | 다크모드 버튼과 Todo 필터 버튼을 보여준다. |
| `TodoList` | Todo 배열 상태를 관리하고, 추가·수정·삭제·저장 기능을 처리한다. |
| `Todo` | Todo 하나를 화면에 표시하고, 완료 상태 변경과 삭제 이벤트를 처리한다. |
| `AddTodo` | 새 Todo 입력 폼을 담당한다. |
| `DarkModeProvider` | 다크모드 상태를 하위 컴포넌트에 공급한다. |

컴포넌트를 나누면 코드의 책임이 명확해진다. 예를 들어 Todo를 추가하는 코드는 `AddTodo`, Todo 배열을 실제로 관리하는 코드는 `TodoList`, Todo 하나를 표시하는 코드는 `Todo`에 둔다.

---

## 3. App 컴포넌트

`App` 컴포넌트는 전체 Todo 앱의 큰 흐름을 담당한다.

```jsx
import { useState } from "react"
import "./App.css"
import Header from "./components/header/Header"
import TodoList from "./components/todolist/TodoList"
import { DarkModeProvider } from "./context/DarkmodeContext"

const filters = ["all", "active", "completed"]

function App() {
  const [filter, setFilter] = useState(filters[0])

  return (
    <DarkModeProvider>
      <Header
        filters={filters}
        filter={filter}
        onFilterChange={setFilter}
      />
      <TodoList filter={filter} />
    </DarkModeProvider>
  )
}

export default App
```

### 코드 흐름

1. `filters` 배열에 사용할 필터 목록을 저장한다.
2. `filter` 상태에는 현재 선택된 필터를 저장한다.
3. 처음 상태는 `filters[0]`이므로 `"all"`이다.
4. `Header`에는 필터 목록, 현재 필터, 필터 변경 함수를 전달한다.
5. `TodoList`에는 현재 필터 값을 전달한다.
6. `DarkModeProvider`로 전체 컴포넌트를 감싸 다크모드 상태를 공유한다.

여기서 중요한 점은 **필터 상태를 App에서 관리한다는 것**이다. `Header`는 필터를 바꾸는 버튼을 가지고 있고, `TodoList`는 필터 값에 따라 목록을 보여줘야 한다. 두 컴포넌트가 같은 상태를 사용해야 하므로 공통 부모인 `App`에서 상태를 관리한다.

---

## 4. Todo 데이터 구조

이 프로젝트에서 Todo 하나는 객체 형태로 표현한다.

```jsx
{
  id: "고유한 id",
  text: "할 일 내용",
  status: "active"
}
```

각 속성의 의미는 다음과 같다.

| 속성 | 의미 |
|---|---|
| `id` | Todo를 구분하기 위한 고유 값이다. |
| `text` | 사용자가 입력한 할 일 내용이다. |
| `status` | Todo의 진행 상태다. `"active"` 또는 `"completed"` 값을 가진다. |

Todo 배열은 다음과 같은 형태가 된다.

```jsx
[
  { id: "1", text: "React 공부하기", status: "active" },
  { id: "2", text: "Todo 앱 만들기", status: "completed" },
  { id: "3", text: "코드 정리하기", status: "active" },
]
```

Todo를 객체로 관리하면 텍스트뿐 아니라 완료 여부, 생성일, 중요도 같은 정보를 나중에 추가하기 쉽다.

---

## 5. uuid로 고유 id 만들기

Todo를 추가할 때는 각 Todo를 구분할 수 있는 고유한 id가 필요하다.

이 프로젝트에서는 `uuid` 라이브러리를 사용한다.

```bash
npm i uuid
```

사용할 때는 다음처럼 import한다.

```jsx
import { v4 as uuidv4 } from "uuid"
```

새 Todo를 만들 때 `uuidv4()`를 호출하면 고유한 문자열 id가 생성된다.

```jsx
onAdd({
  id: uuidv4(),
  text,
  status: "active",
})
```

React에서 목록을 출력할 때는 각 항목을 구분하기 위해 `key`가 필요하다.

```jsx
{filtered.map((item) => (
  <Todo key={item.id} todo={item} />
))}
```

`id`는 Todo마다 고유하므로 `key`로 사용하기 좋다.

---

## 6. AddTodo 컴포넌트

`AddTodo` 컴포넌트는 사용자가 새 Todo를 입력하고 제출하는 역할을 한다.

```jsx
import { useState } from "react"
import { v4 as uuidv4 } from "uuid"
import styles from "./AddTodo.module.css"

export default function AddTodo({ onAdd }) {
  const [text, setText] = useState("")

  const handleChange = (e) => setText(e.target.value)

  const handleSubmit = (e) => {
    e.preventDefault()

    if (text.trim().length === 0) {
      return
    }

    onAdd({ id: uuidv4(), text, status: "active" })
    setText("")
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <input
        className={styles.input}
        type="text"
        placeholder="할 일 추가"
        value={text}
        onChange={handleChange}
      />
      <button className={styles.button}>추가</button>
    </form>
  )
}
```

### controlled component

입력창의 값은 React 상태와 연결되어 있다.

```jsx
const [text, setText] = useState("")
```

```jsx
<input value={text} onChange={handleChange} />
```

사용자가 입력창에 글자를 입력하면 `onChange` 이벤트가 발생한다.

```jsx
const handleChange = (e) => setText(e.target.value)
```

이 구조에서는 입력값을 DOM이 직접 관리하는 것이 아니라 React 상태가 관리한다. 이런 입력 방식을 controlled component라고 한다.

---

## 7. form 제출 처리

폼을 제출하면 `handleSubmit` 함수가 실행된다.

```jsx
const handleSubmit = (e) => {
  e.preventDefault()

  if (text.trim().length === 0) {
    return
  }

  onAdd({ id: uuidv4(), text, status: "active" })
  setText("")
}
```

### e.preventDefault()

HTML form은 기본적으로 제출되면 페이지가 새로고침된다. React 앱에서는 새로고침 없이 상태만 변경해야 하므로 기본 동작을 막아야 한다.

```jsx
e.preventDefault()
```

### 빈 값 검사

공백만 입력된 Todo는 추가하지 않는다.

```jsx
if (text.trim().length === 0) {
  return
}
```

`trim()`은 문자열의 앞뒤 공백을 제거한다.

```jsx
"   React   ".trim() // "React"
"     ".trim()       // ""
```

### 입력창 초기화

Todo를 추가한 뒤에는 입력창을 비운다.

```jsx
setText("")
```

입력창의 `value`가 `text` 상태와 연결되어 있으므로, `text`를 빈 문자열로 바꾸면 화면의 입력창도 비워진다.

---

## 8. TodoList 컴포넌트

`TodoList` 컴포넌트는 Todo 배열 상태를 관리한다.

```jsx
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

  const handleUpdate = (updated) =>
    setTodos(todos.map((t) => (t.id === updated.id ? updated : t)))

  const handleDelete = (deleted) =>
    setTodos(todos.filter((t) => t.id !== deleted.id))

  const filtered = getFilteredItems(todos, filter)

  useEffect(() => {
    localStorage.setItem("todos", JSON.stringify(todos))
  }, [todos])

  return (
    <section className={styles.container}>
      <ul className={styles.list}>
        {filtered.map((item) => (
          <Todo
            key={item.id}
            todo={item}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
          />
        ))}
      </ul>
      <AddTodo onAdd={handleAdd} />
    </section>
  )
}
```

`TodoList`는 단순히 목록을 출력하는 컴포넌트가 아니라, Todo 데이터의 중심 역할을 한다.

---

## 9. useState 초기화 함수

Todo 배열 상태는 다음처럼 만든다.

```jsx
const [todos, setTodos] = useState(() => readTodosFromLocalStorage())
```

`useState()`에 값을 바로 넣을 수도 있지만, 함수를 넣을 수도 있다.

```jsx
useState([])
```

```jsx
useState(() => readTodosFromLocalStorage())
```

함수를 전달하면 초기 렌더링 때만 실행된다. `localStorage`를 읽는 작업은 매번 렌더링될 때마다 할 필요가 없으므로 초기화 함수로 작성하는 것이 좋다.

---

## 10. localStorage에서 Todo 읽기

브라우저의 `localStorage`는 문자열만 저장할 수 있다.

따라서 Todo 배열을 저장할 때는 JSON 문자열로 바꾸고, 다시 읽을 때는 배열로 변환해야 한다.

```jsx
function readTodosFromLocalStorage() {
  const todos = localStorage.getItem("todos")
  return todos ? JSON.parse(todos) : []
}
```

### 코드 흐름

1. `localStorage.getItem("todos")`로 저장된 문자열을 읽는다.
2. 값이 있으면 `JSON.parse()`로 배열로 바꾼다.
3. 값이 없으면 빈 배열 `[]`을 반환한다.

예를 들어 `localStorage`에 다음 문자열이 저장되어 있다고 가정한다.

```json
"[{\"id\":\"1\",\"text\":\"React 공부\",\"status\":\"active\"}]"
```

`JSON.parse()`를 사용하면 JavaScript 배열로 변환된다.

```jsx
[
  { id: "1", text: "React 공부", status: "active" }
]
```

---

## 11. localStorage에 Todo 저장하기

Todo 배열이 변경될 때마다 `localStorage`에 저장한다.

```jsx
useEffect(() => {
  localStorage.setItem("todos", JSON.stringify(todos))
}, [todos])
```

`useEffect()`의 의존성 배열에 `todos`가 들어 있으므로, Todo가 추가·수정·삭제될 때마다 실행된다.

배열은 그대로 저장할 수 없기 때문에 `JSON.stringify()`로 문자열로 변환한다.

```jsx
JSON.stringify(todos)
```

### 저장 흐름

```text
Todo 추가, 수정, 삭제
        ↓
todos 상태 변경
        ↓
컴포넌트 다시 렌더링
        ↓
useEffect 실행
        ↓
localStorage에 최신 todos 저장
```

이 구조 덕분에 새로고침해도 Todo 목록이 사라지지 않는다.

---

## 12. Todo 추가

Todo를 추가하는 코드는 다음과 같다.

```jsx
const handleAdd = (todo) => setTodos([...todos, todo])
```

기존 배열을 직접 수정하지 않고, 새 배열을 만들어 상태로 전달한다.

```jsx
[...todos, todo]
```

예를 들어 기존 Todo 배열이 다음과 같다고 하자.

```jsx
const todos = [
  { id: "1", text: "React 공부", status: "active" },
]
```

새 Todo를 추가하면 다음 배열이 만들어진다.

```jsx
[
  { id: "1", text: "React 공부", status: "active" },
  { id: "2", text: "Todo 만들기", status: "active" },
]
```

React 상태에서는 기존 배열을 `push()`로 직접 수정하기보다 새 배열을 만들어 전달하는 방식이 안전하다.

```jsx
// 권장하지 않는 방식
todos.push(todo)
setTodos(todos)
```

```jsx
// 권장하는 방식
setTodos([...todos, todo])
```

---

## 13. Todo 완료 상태 변경

Todo 하나의 완료 상태는 체크박스로 변경한다.

```jsx
<input
  className={styles.checkbox}
  type="checkbox"
  id={id}
  checked={status === "completed"}
  onChange={handleChange}
/>
```

`checked` 값은 Todo의 `status`에 따라 결정된다.

```jsx
checked={status === "completed"}
```

체크박스를 클릭하면 `handleChange`가 실행된다.

```jsx
const handleChange = (e) => {
  const status = e.target.checked ? "completed" : "active"
  onUpdate({ ...todo, status })
}
```

### 코드 흐름

1. 체크박스가 체크되면 `e.target.checked`는 `true`다.
2. `true`이면 `status`를 `"completed"`로 만든다.
3. 체크가 해제되면 `status`를 `"active"`로 만든다.
4. 기존 Todo 객체를 복사하고, `status`만 새 값으로 덮어쓴다.
5. 변경된 Todo 객체를 부모 컴포넌트의 `onUpdate()`로 전달한다.

```jsx
onUpdate({ ...todo, status })
```

위 코드는 다음과 같은 의미다.

```jsx
{
  ...todo,
  status: status
}
```

기존 Todo의 `id`, `text`는 유지하고 `status`만 변경한다.

---

## 14. Todo 수정

Todo 배열에서 특정 Todo만 교체할 때는 `map()`을 사용한다.

```jsx
const handleUpdate = (updated) =>
  setTodos(todos.map((t) => (t.id === updated.id ? updated : t)))
```

`map()`은 배열의 각 요소를 순회하면서 새 배열을 만든다.

```jsx
todos.map((t) => (t.id === updated.id ? updated : t))
```

현재 Todo의 `id`가 수정된 Todo의 `id`와 같으면 `updated`로 교체한다. 다르면 기존 Todo를 그대로 반환한다.

예시는 다음과 같다.

```jsx
const todos = [
  { id: "1", text: "React 공부", status: "active" },
  { id: "2", text: "Todo 만들기", status: "active" },
]

const updated = {
  id: "2",
  text: "Todo 만들기",
  status: "completed",
}

const result = todos.map((todo) =>
  todo.id === updated.id ? updated : todo
)
```

결과는 다음과 같다.

```jsx
[
  { id: "1", text: "React 공부", status: "active" },
  { id: "2", text: "Todo 만들기", status: "completed" },
]
```

---

## 15. Todo 삭제

Todo를 삭제할 때는 `filter()`를 사용한다.

```jsx
const handleDelete = (deleted) =>
  setTodos(todos.filter((t) => t.id !== deleted.id))
```

`filter()`는 조건을 만족하는 요소만 모아 새 배열을 만든다.

```jsx
todos.filter((t) => t.id !== deleted.id)
```

삭제할 Todo와 id가 다른 Todo만 남긴다는 의미다.

예시는 다음과 같다.

```jsx
const todos = [
  { id: "1", text: "React 공부", status: "active" },
  { id: "2", text: "Todo 만들기", status: "completed" },
]

const deleted = {
  id: "1",
  text: "React 공부",
  status: "active",
}

const result = todos.filter((todo) => todo.id !== deleted.id)
```

결과는 다음과 같다.

```jsx
[
  { id: "2", text: "Todo 만들기", status: "completed" },
]
```

---

## 16. Todo 필터링

Todo 앱에는 세 가지 필터가 있다.

```jsx
const filters = ["all", "active", "completed"]
```

각 필터의 의미는 다음과 같다.

| 필터 | 의미 |
|---|---|
| `all` | 전체 Todo를 보여준다. |
| `active` | 아직 완료하지 않은 Todo를 보여준다. |
| `completed` | 완료한 Todo를 보여준다. |

필터링 함수는 다음과 같다.

```jsx
function getFilteredItems(todos, filter) {
  if (filter === "all") {
    return todos
  }

  return todos.filter((todo) => todo.status === filter)
}
```

`filter`가 `"all"`이면 전체 배열을 그대로 반환한다.

```jsx
if (filter === "all") {
  return todos
}
```

그 외에는 Todo의 `status`가 현재 필터와 같은 항목만 반환한다.

```jsx
return todos.filter((todo) => todo.status === filter)
```

---

## 17. Header에서 필터 버튼 만들기

`Header` 컴포넌트는 필터 목록을 받아 버튼으로 출력한다.

```jsx
export default function Header({ filters, filter, onFilterChange }) {
  return (
    <header className={styles.header}>
      <ul className={styles.filters}>
        {filters.map((value, index) => (
          <li key={index}>
            <button
              className={`${styles.filter} ${
                filter === value && styles.selected
              }`}
              onClick={() => onFilterChange(value)}
            >
              {value}
            </button>
          </li>
        ))}
      </ul>
    </header>
  )
}
```

`filters.map()`을 사용해서 `all`, `active`, `completed`를 버튼으로 만든다.

```jsx
filters.map((value, index) => ...)
```

버튼을 클릭하면 현재 필터 값을 변경한다.

```jsx
onClick={() => onFilterChange(value)}
```

`onFilterChange`는 `App`에서 전달한 `setFilter`다.

```jsx
<Header
  filters={filters}
  filter={filter}
  onFilterChange={setFilter}
/>
```

즉, Header에서 버튼을 누르면 App의 `filter` 상태가 변경되고, 변경된 필터가 다시 `TodoList`로 전달된다.

---

## 18. 선택된 필터 스타일 처리

현재 선택된 필터에는 `selected` 클래스를 추가한다.

```jsx
className={`${styles.filter} ${filter === value && styles.selected}`}
```

`filter === value`가 참이면 `styles.selected`가 추가된다.

```jsx
filter === "active"
value === "active"
```

위 조건이 참이면 버튼은 다음 두 클래스를 함께 가진다.

```text
filter selected
```

선택된 필터는 CSS에서 밑줄이 표시된다.

```css
.filter.selected::after {
  content: "";
  display: block;
  margin-top: 0.2rem;
  border: 1px solid var(--color-text);
}
```

더 깔끔하게 작성하려면 삼항 연산자를 사용할 수 있다.

```jsx
className={
  filter === value
    ? `${styles.filter} ${styles.selected}`
    : styles.filter
}
```

이렇게 쓰면 조건이 거짓일 때 클래스 문자열에 불필요한 `false`가 들어가지 않는다.

---

## 19. Todo 컴포넌트

`Todo` 컴포넌트는 Todo 하나를 표시한다.

```jsx
import styles from "./Todo.module.css"
import { FaTrashAlt } from "react-icons/fa"

export default function Todo({ todo, onDelete, onUpdate }) {
  const { id, text, status } = todo

  const handleChange = (e) => {
    const status = e.target.checked ? "completed" : "active"
    onUpdate({ ...todo, status })
  }

  const handleDelete = () => onDelete(todo)

  return (
    <li className={styles.todo}>
      <input
        className={styles.checkbox}
        type="checkbox"
        id={id}
        checked={status === "completed"}
        onChange={handleChange}
      />
      <label htmlFor={id} className={styles.text}>
        {text}
      </label>
      <button className={styles.button} onClick={handleDelete}>
        <FaTrashAlt />
      </button>
    </li>
  )
}
```

이 컴포넌트는 Todo 배열 전체를 알 필요가 없다. 자신이 받은 Todo 하나만 화면에 보여주고, 변경이나 삭제가 필요하면 부모에게 알려준다.

이 구조를 사용하면 각 컴포넌트의 역할이 분명해진다.

```text
Todo       -> 사용자가 한 Todo를 변경했다고 알려준다.
TodoList   -> 실제 todos 배열을 수정한다.
```

---

## 20. checkbox와 label 연결

체크박스와 라벨은 `id`, `htmlFor`로 연결한다.

```jsx
<input type="checkbox" id={id} />
<label htmlFor={id}>{text}</label>
```

React에서는 HTML의 `for` 속성 대신 `htmlFor`를 사용한다.

연결해두면 사용자가 Todo 텍스트를 클릭해도 체크박스가 선택된다. 작은 차이지만 사용성이 좋아진다.

---

## 21. react-icons 사용

삭제 버튼에는 `react-icons` 라이브러리의 휴지통 아이콘을 사용한다.

설치 명령어는 다음과 같다.

```bash
npm i react-icons
```

사용할 아이콘을 import한다.

```jsx
import { FaTrashAlt } from "react-icons/fa"
```

JSX에서는 컴포넌트처럼 사용할 수 있다.

```jsx
<button className={styles.button} onClick={handleDelete}>
  <FaTrashAlt />
</button>
```

`react-icons`는 Font Awesome, Heroicons 등 여러 아이콘 묶음을 React 컴포넌트 형태로 제공한다. 별도의 이미지 파일을 준비하지 않아도 버튼이나 메뉴에 아이콘을 쉽게 넣을 수 있다.

---

## 22. props로 이벤트 함수 전달하기

이 프로젝트에서는 자식 컴포넌트가 직접 부모 상태를 수정하지 않는다. 대신 부모가 함수를 props로 전달하고, 자식은 그 함수를 호출한다.

예를 들어 `TodoList`는 `Todo`에게 수정 함수와 삭제 함수를 전달한다.

```jsx
<Todo
  key={item.id}
  todo={item}
  onDelete={handleDelete}
  onUpdate={handleUpdate}
/>
```

`Todo`는 사용자가 체크박스를 클릭하면 `onUpdate()`를 호출한다.

```jsx
onUpdate({ ...todo, status })
```

삭제 버튼을 클릭하면 `onDelete()`를 호출한다.

```jsx
const handleDelete = () => onDelete(todo)
```

이 구조를 그림으로 보면 다음과 같다.

```text
TodoList
  ├─ todos 상태를 가지고 있다.
  ├─ handleUpdate 함수를 만든다.
  ├─ handleDelete 함수를 만든다.
  ↓
Todo
  ├─ onUpdate를 호출한다.
  └─ onDelete를 호출한다.
```

상태는 부모가 가지고 있고, 이벤트는 자식이 발생시킨다. React에서 자주 사용하는 데이터 흐름이다.

---

## 23. 배열 상태를 불변하게 다루기

React에서 배열 상태를 변경할 때는 기존 배열을 직접 수정하지 않는 것이 중요하다.

### 추가

```jsx
setTodos([...todos, todo])
```

기존 배열을 복사하고 새 Todo를 뒤에 붙인다.

### 수정

```jsx
setTodos(todos.map((t) => (t.id === updated.id ? updated : t)))
```

수정할 항목만 새 객체로 교체하고 나머지는 그대로 둔다.

### 삭제

```jsx
setTodos(todos.filter((t) => t.id !== deleted.id))
```

삭제할 항목을 제외한 새 배열을 만든다.

이 세 가지 패턴은 React에서 리스트 상태를 다룰 때 매우 자주 사용한다.

| 기능 | 사용하는 배열 메서드 |
|---|---|
| 추가 | spread syntax `...` |
| 수정 | `map()` |
| 삭제 | `filter()` |
| 조회·출력 | `map()` |
| 조건 검색 | `filter()` |

---

## 24. CSS 변수로 테마 관리하기

이 프로젝트는 CSS 변수로 색상을 관리한다.

```css
:root {
  --color-bg-dark: #f5f5f5;
  --color-bg: #fdfffd;
  --color-grey: #d1d1d1;
  --color-text: #22243b;
  --color-accent: #f16e03;
  --color-white: white;
  --color-scrollbar: #aaa7a7;
}
```

다크모드일 때는 `html.dark`에서 변수 값을 바꾼다.

```css
html.dark {
  --color-bg-dark: #1a1c35;
  --color-bg: #22243b;
  --color-grey: #4e4e4e;
  --color-text: #fdfffd;
}
```

컴포넌트 CSS에서는 직접 색상 값을 쓰지 않고 변수를 사용한다.

```css
.header {
  background-color: var(--color-bg-dark);
  border-bottom: 1px solid var(--color-grey);
}

.todo {
  color: var(--color-text);
}
```

이렇게 하면 다크모드로 전환할 때 각 컴포넌트 CSS를 일일이 수정하지 않아도 된다. 루트의 변수 값만 바뀌면 전체 색상이 함께 바뀐다.

---

## 25. 시스템 다크모드 감지

다크모드는 사용자가 직접 선택할 수도 있고, 운영체제의 기본 설정을 따라갈 수도 있다.

```jsx
window.matchMedia("(prefers-color-scheme: dark)").matches
```

위 코드는 사용자의 시스템 설정이 다크모드인지 확인한다.

다크모드 초기값을 정할 때는 다음 흐름을 사용할 수 있다.

```text
localStorage에 theme 값이 dark인가?
        ↓
맞으면 다크모드

localStorage에 theme 값이 없는가?
        ↓
시스템 설정이 다크모드인지 확인
        ↓
맞으면 다크모드
```

예시 코드는 다음과 같다.

```jsx
function getInitialDarkMode() {
  return (
    localStorage.theme === "dark" ||
    (
      !("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    )
  )
}
```

37일차에서는 Context의 기본 구조를 다뤘다면, 이번 Todo 앱에서는 다크모드 값을 CSS 변수와 연결해서 실제 UI 테마를 바꾸는 흐름까지 확인할 수 있다.

---

## 26. 화면 구성 흐름

Todo 앱의 전체 동작 흐름은 다음과 같다.

```text
App
 ├─ filter 상태 관리
 ├─ DarkModeProvider로 감싸기
 │
 ├─ Header
 │   ├─ 다크모드 버튼
 │   └─ all / active / completed 필터 버튼
 │
 └─ TodoList
     ├─ todos 상태 관리
     ├─ localStorage 저장
     ├─ 필터링된 Todo 목록 출력
     │
     ├─ Todo
     │   ├─ 체크박스로 완료 상태 변경
     │   └─ 삭제 버튼
     │
     └─ AddTodo
         └─ 새 Todo 입력 및 추가
```

상태 흐름은 다음과 같다.

```text
사용자 입력
   ↓
AddTodo에서 새 Todo 생성
   ↓
TodoList의 handleAdd 호출
   ↓
todos 상태 변경
   ↓
화면 다시 렌더링
   ↓
useEffect로 localStorage 저장
```

체크박스 변경 흐름은 다음과 같다.

```text
사용자가 Todo 체크
   ↓
Todo의 handleChange 실행
   ↓
status를 completed 또는 active로 변경
   ↓
TodoList의 handleUpdate 호출
   ↓
map()으로 해당 Todo만 교체
   ↓
화면 다시 렌더링
```

삭제 흐름은 다음과 같다.

```text
사용자가 삭제 버튼 클릭
   ↓
Todo의 handleDelete 실행
   ↓
TodoList의 handleDelete 호출
   ↓
filter()로 해당 Todo 제외
   ↓
화면 다시 렌더링
```

---

## 27. 접근성을 고려한 개선 포인트

아이콘만 들어 있는 버튼은 화면으로 보면 의미를 알 수 있지만, 스크린 리더는 버튼의 목적을 알기 어렵다.

삭제 버튼에는 `aria-label`을 추가할 수 있다.

```jsx
<button
  className={styles.button}
  onClick={handleDelete}
  aria-label={`${text} 삭제`}
>
  <FaTrashAlt />
</button>
```

다크모드 버튼도 현재 상태에 따라 설명을 넣을 수 있다.

```jsx
<button
  className={styles.toggle}
  onClick={toggleDarkMode}
  aria-label={darkMode ? "라이트모드로 변경" : "다크모드로 변경"}
>
  {!darkMode && <HiMoon />}
  {darkMode && <HiSun />}
</button>
```

선택된 필터 버튼에는 `aria-pressed`를 사용할 수 있다.

```jsx
<button
  aria-pressed={filter === value}
  onClick={() => onFilterChange(value)}
>
  {value}
</button>
```

작은 Todo 앱이라도 이런 속성을 넣어두면 키보드 사용자와 스크린 리더 사용자에게 더 친절한 UI가 된다.

---

## 28. 핵심 정리

TodoList 프로젝트는 React에서 자주 사용하는 상태 관리 패턴을 종합적으로 연습하기 좋은 예제다.

`App`은 필터 상태를 관리하고, `Header`는 필터 변경 이벤트를 발생시킨다. `TodoList`는 Todo 배열 상태를 관리하며, `AddTodo`는 새 Todo를 생성하고, `Todo`는 하나의 Todo를 표시하면서 완료 상태 변경과 삭제 이벤트를 처리한다.

Todo 배열은 직접 수정하지 않고 `spread syntax`, `map()`, `filter()`를 사용해 새 배열로 변경한다. 이 방식은 React가 상태 변경을 올바르게 감지하고 화면을 다시 렌더링하게 만든다.

또한 `localStorage`를 사용해 새로고침 후에도 Todo 목록이 유지되도록 만들고, `uuid`로 각 Todo의 고유 id를 생성한다. `react-icons`를 활용하면 이미지 파일 없이도 아이콘 UI를 쉽게 구성할 수 있다.

이번 프로젝트의 핵심은 단순히 Todo 앱을 만드는 것이 아니라, **상태를 어디에 둘지**, **자식 컴포넌트가 부모 상태를 어떻게 변경 요청할지**, **배열 데이터를 어떻게 안전하게 수정할지**를 이해하는 데 있다.

