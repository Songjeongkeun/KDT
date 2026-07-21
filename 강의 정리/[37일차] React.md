# [37일차] React - Context API와 React Router 정리

## 1. 이번 정리에서 다루는 내용

이번 내용은 기존에 정리한 React 기본 문법, props, state, 이벤트 처리, `useEffect`, fetch, custom Hook, `useReducer`, `useMemo`, `useCallback`과 겹치지 않는 부분만 정리한다.

주요 내용은 다음과 같다.

- Context API
- `createContext()`
- `Provider`
- `useContext()`
- 다크모드 상태 공유
- React Router
- `createBrowserRouter()`
- `RouterProvider`
- 중첩 라우팅
- `Outlet`
- `Link`
- `useNavigate()`
- `useParams()`
- 에러 페이지 처리
- CSS Module
- styled-components
- Tailwind CSS 기본 설정

---

## 2. Context API

Context API는 여러 컴포넌트가 함께 사용해야 하는 데이터를 전역처럼 공유할 수 있게 해주는 React 기능이다.

React에서는 일반적으로 부모 컴포넌트가 자식 컴포넌트에게 데이터를 전달할 때 `props`를 사용한다. 하지만 여러 단계 아래에 있는 컴포넌트까지 데이터를 전달해야 한다면, 중간 컴포넌트들이 실제로 사용하지 않는 props까지 계속 전달해야 한다.

이런 문제를 **props drilling**이라고 한다.

```jsx
function App() {
  const user = "apple"

  return <Layout user={user} />
}

function Layout({ user }) {
  return <Header user={user} />
}

function Header({ user }) {
  return <Profile user={user} />
}

function Profile({ user }) {
  return <p>{user}</p>
}
```

위 코드에서 `Layout`, `Header`는 `user`를 직접 사용하지 않지만, `Profile`까지 전달하기 위해 props를 계속 넘겨야 한다.

Context API를 사용하면 이런 데이터를 필요한 컴포넌트에서 바로 꺼내 쓸 수 있다.

---

## 3. createContext()

`createContext()`는 여러 컴포넌트가 함께 사용할 데이터 저장 공간을 만드는 함수다.

```jsx
import { createContext } from "react"

export const DarkModeContext = createContext()
```

위 코드는 `DarkModeContext`라는 Context 객체를 만든다. 이 Context는 다크모드 상태와 다크모드를 변경하는 함수를 여러 컴포넌트에서 공유하기 위한 통로 역할을 한다.

Context 자체는 데이터를 저장하는 공간이라기보다, 데이터를 공급하는 `Provider`와 데이터를 사용하는 컴포넌트를 연결하는 역할을 한다고 이해하면 좋다.

---

## 4. Provider

`Provider`는 Context에 실제 데이터를 넣어주는 역할을 한다.

```jsx
<DarkModeContext.Provider value={{ darkMode, toggleDarkMode }}>
  {children}
</DarkModeContext.Provider>
```

`value`에 넣은 값은 `Provider` 안쪽에 있는 컴포넌트들이 `useContext()`로 꺼내 사용할 수 있다.

예를 들어 다음처럼 `App`을 `DarkModeProvider`로 감싸면, `App` 내부의 모든 컴포넌트가 다크모드 상태를 사용할 수 있다.

```jsx
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import App from "./App.jsx"
import { DarkModeProvider } from "./DarkModeContext.jsx"

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <DarkModeProvider>
      <App />
    </DarkModeProvider>
  </StrictMode>
)
```

`DarkModeProvider`는 `App`을 감싸고 있기 때문에 `App`과 그 하위 컴포넌트들은 다크모드 상태에 접근할 수 있다.

---

## 5. children

`children`은 컴포넌트 태그 사이에 들어온 내용을 의미한다.

```jsx
<DarkModeProvider>
  <App />
</DarkModeProvider>
```

위 코드에서 `DarkModeProvider` 입장에서 `children`은 `<App />`이다.

따라서 `DarkModeProvider` 내부에서 다음처럼 작성하면, Provider가 감싼 컴포넌트들을 그대로 화면에 출력할 수 있다.

```jsx
return (
  <DarkModeContext.Provider value={{ darkMode, toggleDarkMode }}>
    {children}
  </DarkModeContext.Provider>
)
```

즉, `children`은 공통 기능을 감싸면서도 내부 컴포넌트를 그대로 유지할 때 자주 사용한다.

---

## 6. 다크모드 Context 코드

다음 코드는 다크모드 상태를 Context로 관리하는 예시다.

```jsx
import { useEffect, useState, createContext } from "react"

export const DarkModeContext = createContext()

export function DarkModeProvider({ children }) {
  const [darkMode, setDarkMode] = useState(() => {
    const savedDarkMode = localStorage.getItem("darkMode")
    return savedDarkMode === "true"
  })

  const toggleDarkMode = () => {
    setDarkMode((prevDarkMode) => !prevDarkMode)
  }

  useEffect(() => {
    localStorage.setItem("darkMode", String(darkMode))
    document.documentElement.classList.toggle("dark", darkMode)
  }, [darkMode])

  return (
    <DarkModeContext.Provider value={{ darkMode, toggleDarkMode }}>
      {children}
    </DarkModeContext.Provider>
  )
}
```

### 코드 흐름

1. `createContext()`로 다크모드 Context를 만든다.
2. `useState()`로 다크모드 상태를 관리한다.
3. 처음 렌더링될 때 `localStorage`에 저장된 다크모드 값을 읽는다.
4. `toggleDarkMode()`가 실행되면 이전 상태를 반대로 바꾼다.
5. `darkMode` 값이 바뀔 때마다 `useEffect()`가 실행된다.
6. 변경된 다크모드 값을 `localStorage`에 저장한다.
7. `<html>` 요소에 `dark` 클래스를 추가하거나 제거한다.
8. `Provider`의 `value`를 통해 `darkMode`, `toggleDarkMode`를 하위 컴포넌트에 전달한다.

---

## 7. useContext()

`useContext()`는 Context에 저장된 값을 컴포넌트에서 꺼내 사용할 때 쓰는 Hook이다.

```jsx
import { useContext } from "react"
import { DarkModeContext } from "./DarkModeContext"

function App() {
  const { darkMode, toggleDarkMode } = useContext(DarkModeContext)

  return (
    <main className="app">
      <section className="content">
        <h1>다크모드 설정</h1>
        <p>
          현재 화면 모드는{" "}
          <strong>{darkMode ? "다크모드" : "라이트모드"}</strong>입니다.
        </p>
        <button type="button" onClick={toggleDarkMode}>
          {darkMode ? "라이트모드로 변경" : "다크모드로 변경"}
        </button>
      </section>
    </main>
  )
}

export default App
```

`useContext(DarkModeContext)`를 사용하면 `Provider`의 `value`에 넣어둔 값을 가져올 수 있다.

```jsx
const { darkMode, toggleDarkMode } = useContext(DarkModeContext)
```

위 코드에서 `darkMode`는 현재 모드 상태이고, `toggleDarkMode`는 모드를 변경하는 함수다.

---

## 8. localStorage와 다크모드 유지

다크모드는 사용자가 페이지를 새로고침해도 유지되는 것이 자연스럽다. 그래서 브라우저 저장소인 `localStorage`를 사용한다.

```jsx
const [darkMode, setDarkMode] = useState(() => {
  const savedDarkMode = localStorage.getItem("darkMode")
  return savedDarkMode === "true"
})
```

위 코드는 처음 상태를 만들 때 `localStorage`에 저장된 값을 읽는다.

```jsx
useEffect(() => {
  localStorage.setItem("darkMode", String(darkMode))
  document.documentElement.classList.toggle("dark", darkMode)
}, [darkMode])
```

`darkMode`가 바뀌면 `localStorage`에 값을 다시 저장하고, `<html>` 태그에 `dark` 클래스를 붙이거나 제거한다.

```css
:root.dark .content {
  background-color: #242424;
  border-color: #444444;
}
```

CSS에서는 `:root.dark`를 기준으로 다크모드 스타일을 적용할 수 있다.

---

## 9. Context API를 사용할 때 좋은 경우

Context API는 모든 상태를 넣는 공간이 아니다. 여러 컴포넌트가 공통으로 사용해야 하는 값에 적합하다.

대표적인 예시는 다음과 같다.

- 로그인한 사용자 정보
- 다크모드, 라이트모드 설정
- 언어 설정
- 테마 색상
- 장바구니 개수
- 권한 정보

반대로 특정 컴포넌트 안에서만 사용하는 값이라면 일반 `useState()`가 더 단순하다.

---

## 10. React Router

React Router는 React에서 페이지 이동을 구현할 때 사용하는 라이브러리다.

일반 웹사이트에서는 페이지를 이동할 때 서버에서 새로운 HTML 문서를 다시 받아온다. 하지만 React로 만든 SPA에서는 하나의 HTML 안에서 컴포넌트를 바꿔가며 화면을 보여준다.

React Router는 URL과 컴포넌트를 연결해서 다음과 같은 구조를 만들 수 있게 해준다.

```text
/              -> Home 컴포넌트
/videos        -> Videos 컴포넌트
/videos/abc    -> VideoDetail 컴포넌트
없는 주소       -> NotFound 컴포넌트
```

---

## 11. React Router 설치

React Router를 사용하려면 `react-router-dom`을 설치한다.

```bash
npm i react-router-dom
```

설치 후 다음 기능들을 가져와 사용할 수 있다.

```jsx
import {
  createBrowserRouter,
  RouterProvider,
  Link,
  Outlet,
  useNavigate,
  useParams,
} from "react-router-dom"
```

---

## 12. createBrowserRouter()

`createBrowserRouter()`는 URL과 컴포넌트 연결 규칙을 만드는 함수다.

```jsx
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import NotFound from "./pages/NotFound"
import Root from "./pages/Root"
import Home from "./pages/Home"
import Videos from "./pages/Videos"
import VideoDetail from "./pages/VideoDetail"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      { index: true, element: <Home /> },
      { path: "videos", element: <Videos /> },
      { path: "videos/:videoId", element: <VideoDetail /> },
    ],
  },
])

function App() {
  return <RouterProvider router={router} />
}

export default App
```

### 주요 속성

| 속성 | 의미 |
|---|---|
| `path` | URL 경로를 의미한다. |
| `element` | 해당 경로에서 보여줄 컴포넌트다. |
| `children` | 중첩 라우트를 정의한다. |
| `index: true` | 부모 경로와 정확히 일치할 때 보여줄 기본 페이지다. |
| `errorElement` | 라우팅 중 오류가 발생하거나 없는 경로로 접근했을 때 보여줄 컴포넌트다. |

---

## 13. RouterProvider

`RouterProvider`는 만들어둔 라우터 설정을 React 앱에 적용하는 컴포넌트다.

```jsx
function App() {
  return <RouterProvider router={router} />
}
```

`createBrowserRouter()`로 라우팅 규칙을 만들고, `RouterProvider`에 전달하면 브라우저 주소에 따라 알맞은 컴포넌트가 렌더링된다.

---

## 14. 중첩 라우팅

중첩 라우팅은 공통 레이아웃 안에서 하위 페이지를 바꿔 보여주는 방식이다.

```jsx
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      { index: true, element: <Home /> },
      { path: "videos", element: <Videos /> },
      { path: "videos/:videoId", element: <VideoDetail /> },
    ],
  },
])
```

위 구조에서는 `/`, `/videos`, `/videos/:videoId` 모두 `Root` 컴포넌트를 먼저 렌더링한다. 그리고 `Root` 내부의 `Outlet` 위치에 하위 페이지가 들어간다.

---

## 15. Outlet

`Outlet`은 중첩 라우팅에서 자식 라우트 컴포넌트가 들어갈 자리를 의미한다.

```jsx
import { Outlet } from "react-router-dom"
import Navbar from "../components/Navbar"

export default function Root() {
  return (
    <div>
      <Navbar />
      <Outlet />
    </div>
  )
}
```

위 코드에서 `Navbar`는 모든 페이지에서 공통으로 보이고, `Outlet` 자리에는 URL에 따라 다른 컴포넌트가 들어온다.

```text
/              -> Navbar + Home
/videos        -> Navbar + Videos
/videos/100    -> Navbar + VideoDetail
```

이런 구조를 사용하면 공통 레이아웃을 반복해서 작성하지 않아도 된다.

---

## 16. Link

`Link`는 React Router에서 페이지를 이동할 때 사용하는 컴포넌트다.

```jsx
import { Link } from "react-router-dom"

export default function Navbar() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/videos">Videos</Link>
      </nav>
      <hr />
    </>
  )
}
```

일반 HTML에서는 페이지 이동에 `<a>` 태그를 사용한다.

```html
<a href="/videos">Videos</a>
```

하지만 React Router에서는 보통 `Link`를 사용한다.

```jsx
<Link to="/videos">Videos</Link>
```

`Link`를 사용하면 전체 페이지를 새로고침하지 않고, React 내부에서 컴포넌트만 바꿔서 화면을 전환한다.

---

## 17. useNavigate()

`useNavigate()`는 JavaScript 코드로 페이지를 이동할 때 사용하는 Hook이다.

버튼 클릭, 폼 제출, 로그인 성공 후 이동처럼 이벤트 결과에 따라 이동해야 할 때 사용한다.

```jsx
import { useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Videos() {
  const [text, setText] = useState("")
  const navigate = useNavigate()

  const handleChange = (e) => {
    setText(e.target.value)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setText("")
    navigate(`/videos/${text}`)
  }

  return (
    <div>
      Videos
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Video id: "
          value={text}
          onChange={handleChange}
        />
      </form>
    </div>
  )
}
```

위 코드에서 사용자가 입력창에 값을 입력하고 Enter를 누르면 다음 경로로 이동한다.

```text
입력값: 100
이동 경로: /videos/100
```

`navigate()`는 함수이므로 조건문이나 이벤트 함수 안에서 자유롭게 사용할 수 있다.

---

## 18. useParams()

`useParams()`는 URL에 포함된 동적 값을 꺼낼 때 사용하는 Hook이다.

라우터에서 다음처럼 `:videoId`를 사용하면 이 부분은 고정된 문자열이 아니라 변수처럼 동작한다.

```jsx
{ path: "videos/:videoId", element: <VideoDetail /> }
```

예를 들어 주소가 `/videos/100`이라면 `videoId` 값은 `"100"`이 된다.

```jsx
import { useParams } from "react-router-dom"

export default function VideoDetail() {
  const { videoId } = useParams()

  return <div>VideoDetail {videoId}</div>
}
```

실행 예시는 다음과 같다.

```text
주소: /videos/react
화면: VideoDetail react
```

`useParams()`는 게시글 상세 페이지, 상품 상세 페이지, 영상 상세 페이지처럼 특정 id를 기준으로 데이터를 보여줄 때 자주 사용한다.

---

## 19. NotFound 페이지

사용자가 존재하지 않는 주소로 접근하면 별도의 에러 페이지를 보여주는 것이 좋다.

```jsx
export default function NotFound() {
  return <div>Not Found!</div>
}
```

라우터 설정에서 `errorElement`를 지정하면 라우팅 중 오류가 발생했을 때 해당 컴포넌트를 보여줄 수 있다.

```jsx
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      { index: true, element: <Home /> },
      { path: "videos", element: <Videos /> },
      { path: "videos/:videoId", element: <VideoDetail /> },
    ],
  },
])
```

별도로 모든 잘못된 경로를 처리하고 싶다면 `*` 경로를 사용할 수도 있다.

```jsx
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      { index: true, element: <Home /> },
      { path: "videos", element: <Videos /> },
      { path: "videos/:videoId", element: <VideoDetail /> },
      { path: "*", element: <NotFound /> },
    ],
  },
])
```

`*`는 위에 정의된 경로와 일치하지 않는 나머지 모든 경로를 의미한다.

---

## 20. CSS Module

CSS Module은 CSS 클래스 이름이 다른 컴포넌트와 충돌하지 않도록 컴포넌트 단위로 스타일을 관리하는 방식이다.

일반 CSS 파일을 import하면 클래스 이름이 전역으로 적용된다.

```css
.button {
  background-color: deepskyblue;
}
```

```jsx
import "../App.css"

export default function Home() {
  return <button className="button">버튼</button>
}
```

전역 CSS는 여러 파일에서 같은 `.button` 이름을 사용하면 스타일이 충돌할 수 있다.

CSS Module은 파일명을 다음처럼 작성한다.

```text
Home.module.css
```

```css
.button {
  background-color: deeppink;
}
```

컴포넌트에서는 객체처럼 import해서 사용한다.

```jsx
import styles from "./Home.module.css"
import "../App.css"

export default function Home() {
  return (
    <div>
      Home
      <button className={styles.button}>버튼1</button>
      <button className="button">버튼2</button>
    </div>
  )
}
```

### 차이점

```jsx
<button className={styles.button}>버튼1</button>
```

위 코드는 CSS Module 스타일을 사용한다. 클래스 이름이 자동으로 고유하게 바뀌기 때문에 다른 컴포넌트의 `.button`과 충돌하지 않는다.

```jsx
<button className="button">버튼2</button>
```

위 코드는 전역 CSS를 사용한다. 같은 클래스 이름이 여러 곳에 있으면 영향을 받을 수 있다.

---

## 21. styled-components

styled-components는 JavaScript 파일 안에서 컴포넌트 형태로 CSS를 작성할 수 있게 해주는 라이브러리다.

설치 명령어는 다음과 같다.

```bash
npm i styled-components
```

사용 예시는 다음과 같다.

```jsx
import styled, { css } from "styled-components"

const Container = styled.div`
  display: flex;
`

const Button = styled.button`
  background: black;
  border-radius: 3px;
  border: 3px solid deeppink;
  color: white;
  margin: 0 1em;
  padding: 0.25em 1em;

  ${(props) =>
    props.primary &&
    css`
      background: deepskyblue;
      color: ivory;
    `}
`

export default function Videos() {
  return (
    <Container>
      <Button>기본버튼</Button>
      <Button primary>Primary 버튼</Button>
    </Container>
  )
}
```

`styled.button`은 스타일이 적용된 버튼 컴포넌트를 만든다.

```jsx
const Button = styled.button`
  background: black;
`
```

이후 JSX에서는 일반 컴포넌트처럼 사용할 수 있다.

```jsx
<Button>기본버튼</Button>
```

또한 props를 이용해서 조건부 스타일을 적용할 수 있다.

```jsx
<Button primary>Primary 버튼</Button>
```

`primary` 값이 있으면 다음 CSS가 추가된다.

```jsx
${(props) =>
  props.primary &&
  css`
    background: deepskyblue;
    color: ivory;
  `}
```

styled-components는 컴포넌트와 스타일을 함께 관리하고 싶을 때 유용하다.

---

## 22. Tailwind CSS

Tailwind CSS는 미리 정의된 유틸리티 클래스를 조합해서 빠르게 스타일을 작성하는 CSS 프레임워크다.

예를 들어 다음 코드는 큰 글씨, 파란 배경, 둥근 모서리, 좌우 여백을 클래스 이름만으로 적용한다.

```jsx
<h1 className="text-8xl">메뉴</h1>
<button className="bg-blue-500 rounded-xl px-2">버튼</button>
```

### Vite 프로젝트에 Tailwind 설치

```bash
npm i tailwindcss @tailwindcss/vite
```

`vite.config.js`에 Tailwind 플러그인을 추가한다.

```jsx
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

`index.css`에는 다음 코드를 추가한다.

```css
@import "tailwindcss";
```

이후 JSX에서 Tailwind 클래스를 사용할 수 있다.

```jsx
<button className="bg-blue-500 rounded-xl px-2">
  버튼
</button>
```

---

## 23. 스타일링 방식 비교

React에서는 여러 방식으로 스타일을 적용할 수 있다.

| 방식 | 특징 |
|---|---|
| 일반 CSS | 전역 스타일로 적용된다. 간단하지만 클래스 이름 충돌 가능성이 있다. |
| CSS Module | 컴포넌트 단위로 클래스 이름을 분리할 수 있다. |
| styled-components | JavaScript 안에서 스타일 컴포넌트를 만들 수 있다. props 기반 조건부 스타일에 좋다. |
| Tailwind CSS | 유틸리티 클래스를 조합해서 빠르게 스타일을 작성한다. |

작은 프로젝트에서는 일반 CSS만으로도 충분하다. 컴포넌트가 많아지고 스타일 충돌을 피하고 싶다면 CSS Module이 좋다. 컴포넌트와 스타일을 강하게 묶고 싶다면 styled-components를 사용할 수 있다. 빠르게 UI를 구성하고 싶다면 Tailwind CSS가 편리하다.

---

## 24. 전체 라우팅 흐름 예시

다음은 이번 구조를 기준으로 한 페이지 이동 흐름이다.

```text
사용자가 / 접속
        ↓
RouterProvider가 router 설정 확인
        ↓
path "/"에 해당하는 Root 렌더링
        ↓
Root 안에서 Navbar 출력
        ↓
Outlet 위치에 index route인 Home 렌더링
```

`/videos`로 이동하면 다음 흐름이 된다.

```text
사용자가 /videos 접속
        ↓
Root 렌더링
        ↓
Navbar 출력
        ↓
Outlet 위치에 Videos 렌더링
```

`/videos/react`로 이동하면 다음 흐름이 된다.

```text
사용자가 /videos/react 접속
        ↓
Root 렌더링
        ↓
Navbar 출력
        ↓
Outlet 위치에 VideoDetail 렌더링
        ↓
useParams()로 videoId 값 추출
        ↓
화면에 VideoDetail react 출력
```

---

## 25. Context와 Router를 함께 사용할 때

Context와 Router는 서로 다른 역할을 한다.

| 구분 | 역할 |
|---|---|
| Context API | 여러 컴포넌트가 공유할 상태를 관리한다. |
| React Router | URL에 따라 보여줄 컴포넌트를 결정한다. |

예를 들어 다크모드 상태는 페이지가 바뀌어도 유지되어야 한다. 이런 값은 Context에 넣어두면 좋다.

```jsx
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <DarkModeProvider>
      <App />
    </DarkModeProvider>
  </StrictMode>
)
```

그리고 `App` 안에서는 Router를 사용해 페이지를 나눌 수 있다.

```jsx
function App() {
  return <RouterProvider router={router} />
}
```

이렇게 구성하면 어떤 페이지로 이동하더라도 다크모드 상태를 공통으로 사용할 수 있다.

---

## 26. 핵심 정리

Context API는 여러 컴포넌트가 함께 사용하는 값을 props 없이 공유할 수 있게 해준다. `createContext()`로 Context를 만들고, `Provider`로 값을 공급하며, `useContext()`로 값을 꺼내 사용한다.

React Router는 React 앱에서 URL과 컴포넌트를 연결한다. `createBrowserRouter()`로 라우팅 규칙을 만들고, `RouterProvider`로 앱에 적용한다. 중첩 라우팅에서는 `Outlet`이 자식 페이지가 들어갈 위치가 된다.

`Link`는 새로고침 없는 페이지 이동에 사용하고, `useNavigate()`는 코드로 이동할 때 사용한다. `useParams()`는 `/videos/:videoId`처럼 URL 안에 들어 있는 동적 값을 가져올 때 사용한다.

스타일링은 일반 CSS, CSS Module, styled-components, Tailwind CSS 등 여러 방식이 있으며, 프로젝트 규모와 목적에 따라 선택하면 된다.

