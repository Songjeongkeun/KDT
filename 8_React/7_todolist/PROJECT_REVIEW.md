# [React] TodoList 프로젝트 코드 점검

React로 만든 TodoList 프로젝트를 다시 확인하고, 현재 구현된 기능과 수정하면 좋은 부분을 정리했다.

현재 프로젝트에는 다음 기능이 구현되어 있다.

- 할 일 추가
- 할 일 완료 상태 변경
- 할 일 삭제
- 전체, 진행 중, 완료 필터
- LocalStorage 저장
- Context API를 이용한 다크 모드
- CSS Module을 이용한 컴포넌트별 스타일 관리

검사 결과 프로덕션 빌드는 통과했지만 ESLint 오류가 3개 남아 있다.

```text
프로덕션 빌드: 통과
ESLint: 오류 3개
```

---

## 1. 프로젝트 구조

현재 주요 파일 구조는 다음과 같다.

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
| `App` | 필터 상태를 관리하고 전체 컴포넌트를 연결한다. |
| `Header` | 다크 모드 버튼과 필터 버튼을 보여준다. |
| `TodoList` | Todo 목록과 LocalStorage를 관리한다. |
| `Todo` | 하나의 할 일을 표시하고 완료·삭제 이벤트를 처리한다. |
| `AddTodo` | 새로운 할 일을 입력받아 목록에 추가한다. |
| `DarkModeProvider` | 다크 모드 상태와 변경 함수를 공유한다. |

---

## 2. Todo 컴포넌트

`Todo` 컴포넌트는 하나의 할 일을 화면에 표시한다.

```jsx
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

체크박스가 선택되면 상태를 `completed`로 바꾸고, 선택이 해제되면 `active`로 바꾼다.

```jsx
const status = e.target.checked ? "completed" : "active"
```

변경된 Todo 객체는 부모 컴포넌트가 전달한 `onUpdate()`로 보낸다.

```jsx
onUpdate({ ...todo, status })
```

삭제 버튼을 누르면 현재 Todo 객체를 `onDelete()`에 전달한다.

```jsx
const handleDelete = () => onDelete(todo)
```

---

## 3. TodoList 상태 관리

`TodoList` 컴포넌트는 Todo 배열을 관리한다.

```jsx
const [todos, setTodos] = useState(() => readTodosFromLocalStorage())
```

초기 렌더링 시 LocalStorage에서 기존 Todo를 읽는다. `useState()`에 함수를 전달했기 때문에 초기 렌더링에서만 해당 함수가 실행된다.

현재 추가·수정·삭제 함수는 다음과 같다.

```jsx
const handleAdd = (todo) => setTodos([...todos, todo])

const handleUpdate = (updated) =>
    setTodos(todos.map((todo) =>
        todo.id === updated.id ? updated : todo
    ))

const handleDelete = (deleted) =>
    setTodos(todos.filter((todo) => todo.id !== deleted.id))
```

### 코드 흐름

1. `AddTodo`가 새로운 Todo 객체를 만든다.
2. `handleAdd()`가 기존 배열 뒤에 새 Todo를 추가한다.
3. 체크박스가 변경되면 `handleUpdate()`가 같은 `id`를 가진 Todo를 교체한다.
4. 삭제 버튼을 누르면 `handleDelete()`가 같은 `id`를 가진 Todo를 제외한다.
5. `todos`가 변경되면 화면이 다시 렌더링된다.

---

## 4. LocalStorage

LocalStorage를 사용하면 페이지를 새로고침해도 Todo 목록을 유지할 수 있다.

Todo 목록이 변경될 때마다 다음 Effect가 실행된다.

```jsx
useEffect(() => {
    localStorage.setItem("todos", JSON.stringify(todos))
}, [todos])
```

배열은 LocalStorage에 직접 저장할 수 없기 때문에 `JSON.stringify()`로 문자열로 변환한다.

저장된 값을 읽을 때는 `JSON.parse()`로 다시 배열로 변환한다.

```jsx
function readTodosFromLocalStorage() {
    const todos = localStorage.getItem("todos")
    return todos ? JSON.parse(todos) : []
}
```

### 코드 흐름

1. 처음 렌더링될 때 LocalStorage의 `todos` 값을 읽는다.
2. 문자열을 JavaScript 배열로 변환한다.
3. 변환된 배열을 `todos`의 초기 상태로 사용한다.
4. Todo가 추가·수정·삭제되면 `todos` 상태가 변경된다.
5. `useEffect()`가 변경된 배열을 다시 LocalStorage에 저장한다.

---

## 6. Todo 필터링

필터 값은 `all`, `active`, `completed` 세 가지다.

```jsx
const filters = ["all", "active", "completed"]
```

`all`이면 전체 배열을 반환하고, 나머지 필터에서는 상태가 일치하는 Todo만 반환한다.

```jsx
function getFilteredItems(todos, filter) {
    if (filter === "all") {
        return todos
    }

    return todos.filter((todo) => todo.status === filter)
}
```

필터링된 배열은 `map()`을 이용해 `Todo` 컴포넌트로 변환한다.

```jsx
{filtered.map((item) => (
    <Todo
        key={item.id}
        todo={item}
        onDelete={handleDelete}
        onUpdate={handleUpdate}
    />
))}
```

Todo의 `id`는 UUID이므로 React 목록의 `key`로 사용하기 적합하다.

---

## 7. Header의 조건부 클래스

현재 선택된 필터에는 `selected` 클래스를 추가한다.

```jsx
className={`${styles.filter} ${filter === value && styles.selected}`}
```

하지만 조건이 거짓이면 클래스 문자열 안에 `false`가 들어간다.

```html
<button class="filter false">
```

화면이 바로 깨지는 문제는 아니지만 불필요한 클래스가 생긴다. 삼항 연산자로 처리하면 더 명확하다.

```jsx
className={
    filter === value
        ? `${styles.filter} ${styles.selected}`
        : styles.filter
}
```

필터 값은 `all`, `active`, `completed`처럼 고유하므로 배열의 index보다 값 자체를 `key`로 사용할 수 있다.

```jsx
{filters.map((value) => (
    <li key={value}>
```

---

## 8. AddTodo 입력 처리

`AddTodo`는 controlled component 방식으로 입력값을 관리한다.

```jsx
const [text, setText] = useState("")

const handleChange = (e) => {
    setText(e.target.value)
}
```

입력창의 `value`는 React 상태와 연결되어 있다.

```jsx
<input
    type="text"
    value={text}
    onChange={handleChange}
/>
```

폼을 제출하면 빈 문자열인지 검사한 후 새 Todo를 만든다.

```jsx
if (text.trim().length === 0) {
    return
}

onAdd({
    id: uuidv4(),
    text,
    status: "active",
})
```

현재 코드는 공백 여부만 검사하고 실제 저장에는 원래 문자열을 사용한다. 앞뒤 공백을 제거한 값을 저장하는 편이 자연스럽다.

```jsx
const trimmedText = text.trim()

if (!trimmedText) {
    return
}

onAdd({
    id: uuidv4(),
    text: trimmedText,
    status: "active",
})
```

---

## 9. Context API와 다크 모드

다크 모드 상태는 `Header`와 스타일 시스템에서 공통으로 사용되므로 Context API에 적합하다.

현재 Provider는 다음 값을 하위 컴포넌트에 전달한다.

```jsx
<DarkModeContext.Provider value={{ darkMode, toggleDarkMode }}>
    {children}
</DarkModeContext.Provider>
```

`Header`에서는 커스텀 Hook으로 값을 꺼낸다.

```jsx
const { darkMode, toggleDarkMode } = useDarkMode()
```

### 미디어 쿼리 문자열

현재 시스템 다크 모드를 확인하는 문자열에는 괄호가 빠져 있다.

```jsx
window.matchMedia("prefers-color-scheme: dark").matches
```

다음처럼 작성해야 한다.

```jsx
window.matchMedia("(prefers-color-scheme: dark)").matches
```

### 초기 상태 설정

현재 코드는 컴포넌트가 렌더링된 후 Effect 안에서 상태를 다시 설정한다.

```jsx
useEffect(() => {
    const isDark = /* 다크 모드 계산 */
    setDarkMode(isDark)
    updateDarkMode(isDark)
}, [])
```

이 부분 때문에 다음 ESLint 오류가 발생한다.

```text
react-hooks/set-state-in-effect
```

초기 다크 모드는 `useState()`의 초기화 함수에서 읽을 수 있다.

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

const [darkMode, setDarkMode] = useState(getInitialDarkMode)
```

상태가 변경될 때 LocalStorage와 `<html>`의 클래스를 동기화한다.

```jsx
useEffect(() => {
    updateDarkMode(darkMode)
}, [darkMode])
```

토글 함수에서는 이전 상태를 반대로 변경한다.

```jsx
const toggleDarkMode = () => {
    setDarkMode((previousDarkMode) => !previousDarkMode)
}
```

### 코드 흐름

1. 처음 렌더링될 때 LocalStorage 또는 시스템 설정에서 다크 모드를 읽는다.
2. 읽은 값을 `darkMode`의 초기 상태로 사용한다.
3. 다크 모드 버튼을 누르면 이전 상태를 반대로 변경한다.
4. `darkMode`가 바뀌면 Effect가 실행된다.
5. 변경된 값을 LocalStorage에 저장한다.
6. `<html>` 요소에 `dark` 클래스를 추가하거나 제거한다.
7. CSS 변수의 색상이 변경된다.

---

## 10. Context 파일과 Fast Refresh

현재 `DarkmodeContext.jsx`는 Provider 컴포넌트와 커스텀 Hook을 함께 export한다.

```jsx
export function DarkModeProvider() {}
export const useDarkMode = () => {}
```

이 구조 때문에 다음 ESLint 오류가 발생한다.

```text
react-refresh/only-export-components
```

Fast Refresh 규칙은 컴포넌트 파일에서 컴포넌트가 아닌 값을 함께 export하지 않도록 권장한다.

역할별로 나누면 다음과 같은 구조가 된다.

```text
context
├── DarkModeContext.js
├── DarkModeProvider.jsx
└── useDarkMode.js
```

| 파일 | 역할 |
|---|---|
| `DarkModeContext.js` | Context 객체를 만든다. |
| `DarkModeProvider.jsx` | 다크 모드 상태를 관리하고 공급한다. |
| `useDarkMode.js` | Context 값을 꺼내는 Hook을 제공한다. |

작은 학습 프로젝트에서는 하나의 파일에 둘 수도 있지만, 현재 ESLint 설정을 유지하려면 파일을 분리하는 것이 가장 명확하다.

---

## 11. CSS Module과 전역 CSS

CSS Module은 클래스 이름이 다른 컴포넌트와 충돌하지 않도록 컴포넌트 단위로 스타일을 관리한다.

```jsx
import styles from "./Todo.module.css"
```

```jsx
<li className={styles.todo}>
```

빌드 과정에서 `.todo` 같은 클래스 이름은 고유한 이름으로 변환된다.

반면 `index.css`와 `App.css`는 전역 스타일이다. 현재 두 파일 모두 `body`, `button`, 색상과 관련된 설정을 가지고 있다.

```text
index.css → Vite 기본 전역 스타일
App.css   → TodoList 전용 전역 스타일과 색상 변수
```

전역 `button` 스타일은 모든 버튼에 영향을 준다.

```css
button {
    padding: 0.6em 1.2em;
    background-color: #1a1a1a;
}
```

컴포넌트에서 예상하지 못한 크기나 색상이 적용될 수 있으므로, Vite 기본 스타일 중 사용하지 않는 부분을 정리하고 앱 공통 스타일의 위치를 하나로 통일하는 것이 좋다.

### 사용되지 않는 `.icon` 클래스

`Todo.module.css`에는 다음 클래스가 있다.

```css
.icon {
    width: 26px;
    height: 26px;
    background-color: var(--color-grey);
    border-radius: 100%;
}
```

하지만 현재 `Todo.jsx`에는 `styles.icon`을 사용하는 요소가 없다. 원형 배경을 사용할 계획이라면 JSX와 연결하고, 사용하지 않는다면 남겨두지 않는 편이 좋다.

---

## 12. 접근성

아이콘만 표시되는 버튼은 화면만 봐서는 용도를 알 수 있지만, 스크린 리더는 버튼의 의미를 알기 어렵다.

다크 모드 버튼에는 현재 상태에 맞는 이름을 제공할 수 있다.

```jsx
<button
    type="button"
    aria-label={darkMode ? "라이트 모드로 전환" : "다크 모드로 전환"}
    onClick={toggleDarkMode}
>
```

삭제 버튼에는 삭제할 Todo의 이름을 포함할 수 있다.

```jsx
<button
    type="button"
    aria-label={`${text} 삭제`}
    onClick={handleDelete}
>
```

선택된 필터 버튼에는 `aria-pressed`를 적용할 수 있다.

```jsx
<button
    type="button"
    aria-pressed={filter === value}
>
```

폼의 추가 버튼에는 제출 버튼이라는 의미를 명확하게 표시한다.

```jsx
<button type="submit">추가</button>
```

---

## 13. 사용자 경험 개선

현재 핵심 CRUD 기능은 구현되어 있다. 다음 항목을 추가하면 사용자가 상태를 더 쉽게 이해할 수 있다.

### 완료된 Todo 표시

완료된 Todo의 텍스트에 취소선을 적용할 수 있다.

```jsx
<label
    htmlFor={id}
    className={`${styles.text} ${
        status === "completed" ? styles.completed : ""
    }`}
>
    {text}
</label>
```

```css
.completed {
    text-decoration: line-through;
    opacity: 0.6;
}
```

### 빈 목록 안내

필터 결과가 없을 때 빈 공간 대신 안내 문구를 표시할 수 있다.

```jsx
{filtered.length === 0 && (
    <p>등록된 할 일이 없습니다.</p>
)}
```

### HTML 언어와 제목

한국어 앱이므로 `index.html`을 다음처럼 설정하는 것이 좋다.

```html
<html lang="ko">
<title>할 일 목록</title>
```

---

## 14. 불필요한 Fragment

현재 `App`은 Fragment 안에 `DarkModeProvider` 하나만 렌더링한다.

```jsx
return (
    <>
        <DarkModeProvider>
            <Header />
            <TodoList />
        </DarkModeProvider>
    </>
)
```

Fragment는 여러 요소를 하나로 묶을 때 사용한다. 현재는 최상위 요소가 하나이므로 생략할 수 있다.

```jsx
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
```

---

## 15. 수정 권장 순서

현재 프로젝트는 빌드가 통과하므로 기능을 한 번에 모두 바꾸기보다 오류부터 순서대로 처리하는 것이 좋다.

```text
1. Todo.jsx의 사용하지 않는 useState import 제거
2. TodoList import 경로의 대소문자 통일
3. matchMedia 미디어 쿼리 괄호 수정
4. 다크 모드 초기 상태를 useState 초기화 함수로 이동
5. Context와 커스텀 Hook 파일 분리
6. npm run lint로 ESLint 오류 해결 확인
7. Todo.jsx가 Git에 포함됐는지 확인
8. Todo 상태 업데이트를 함수형 방식으로 변경
9. LocalStorage 예외 처리 추가
10. Header의 조건부 클래스와 key 수정
11. 접근성 속성 추가
12. 전역 CSS와 사용하지 않는 스타일 정리
13. 완료 상태와 빈 목록 UI 보완
14. README와 index.html 정리
```

수정 후 다음 명령으로 검사한다.

```bash
npm run lint
npm run build
```

---

## 16. 핵심 정리

현재 TodoList 프로젝트는 Todo의 추가, 완료 상태 변경, 삭제, 필터링, LocalStorage 저장, 다크 모드까지 핵심 기능이 구현되어 있다.

`TodoList`는 Todo 배열을 관리하고, `Todo`는 하나의 항목을 표시한다. `AddTodo`는 새로운 Todo를 만들고, `Header`는 필터와 다크 모드를 제어한다.

상태를 이전 값에 기반해 변경할 때는 함수형 업데이트를 사용하면 더 안전하다.

```jsx
setTodos((previousTodos) => [...previousTodos, newTodo])
```

LocalStorage의 데이터는 외부에서 변경되거나 손상될 수 있으므로 `JSON.parse()`를 사용할 때 예외 처리를 추가하는 것이 좋다.

다크 모드의 초기값은 Effect에서 다시 설정하기보다 `useState()`의 초기화 함수에서 읽으면 불필요한 렌더링을 줄일 수 있다.

Context API는 여러 컴포넌트가 함께 사용하는 다크 모드 같은 상태에 적합하다. Context 객체, Provider 컴포넌트, 커스텀 Hook을 역할별로 분리하면 Fast Refresh와 유지보수 측면에서 더 안정적이다.

CSS Module은 컴포넌트의 클래스 충돌을 막아주지만, 전역 `button` 스타일처럼 태그 선택자로 작성한 CSS는 모든 컴포넌트에 영향을 준다. 전역 스타일과 컴포넌트 스타일의 역할을 명확히 나누는 것이 중요하다.

현재 프로덕션 빌드는 통과한다. 남아 있는 ESLint 오류 3개와 파일명의 대소문자, Git 미추적 파일을 먼저 해결한 후 코드 품질과 사용자 경험 개선을 진행하는 순서가 적절하다.
