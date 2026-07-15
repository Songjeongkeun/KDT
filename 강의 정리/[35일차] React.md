# [35일차] React

## 1. React란?

React는 사용자 인터페이스(UI)를 만들기 위한 JavaScript 라이브러리다. 화면을 하나의 큰 덩어리로 작성하지 않고, 버튼, 카드, 입력창, 리스트처럼 작은 단위의 **컴포넌트(Component)** 로 나누어 개발한다.

컴포넌트 단위로 화면을 구성하면 같은 UI를 여러 곳에서 재사용할 수 있고, 코드의 역할이 분리되어 유지보수가 쉬워진다.

React의 핵심 특징은 다음과 같다.

- 컴포넌트 기반으로 UI를 구성한다.
- 상태(state)가 바뀌면 화면을 자동으로 다시 렌더링한다.
- Virtual DOM을 이용해 변경이 필요한 부분만 효율적으로 업데이트한다.
- SPA 방식의 웹 애플리케이션을 만들기 좋다.
- `useState`, `useRef`, `useEffect` 같은 Hook을 통해 상태와 렌더링 흐름을 제어한다.

## 2. SPA

SPA(Single Page Application)는 하나의 HTML 페이지 안에서 화면 전환을 처리하는 웹 애플리케이션 방식이다.

기존 MPA(Multi Page Application)는 페이지를 이동할 때마다 서버에서 새로운 HTML 문서를 다시 받아온다. 반면 SPA는 처음 한 번 HTML, CSS, JavaScript를 받아온 뒤, 이후 화면 변경은 JavaScript가 브라우저 안에서 처리한다.

```text
MPA
페이지 이동 -> 서버에 HTML 요청 -> 새 HTML 응답 -> 전체 페이지 새로고침

SPA
처음 한 번 HTML 로드 -> JavaScript가 필요한 화면만 변경 -> 새로고침 없이 화면 전환
```

React는 SPA 구조를 만들 때 자주 사용된다. 사용자는 페이지가 이동한 것처럼 느끼지만, 실제로는 브라우저 안에서 컴포넌트가 바뀌며 화면이 다시 그려진다.

## 3. Virtual DOM

DOM(Document Object Model)은 브라우저가 HTML 문서를 객체 형태로 표현한 구조다. JavaScript로 DOM을 직접 자주 수정하면 성능 부담이 커질 수 있다.

React는 실제 DOM을 바로 수정하지 않고, 메모리 안에 가벼운 DOM 구조인 **Virtual DOM**을 먼저 만든다.

동작 흐름은 다음과 같다.

```text
상태 변경
  ↓
새로운 Virtual DOM 생성
  ↓
이전 Virtual DOM과 비교
  ↓
달라진 부분 계산
  ↓
실제 DOM에는 필요한 부분만 반영
```

이 과정을 통해 React는 화면 전체를 매번 새로 만드는 것이 아니라, 바뀐 부분만 효율적으로 업데이트한다.

## 4. Vite로 React 프로젝트 만들기

Vite는 빠른 개발 서버와 빌드 환경을 제공하는 프론트엔드 도구다. 기존 번들러보다 개발 서버 시작이 빠르고, 파일 변경 시 화면 반영 속도도 빠르다.

React 프로젝트는 다음 명령어로 만들 수 있다.

```bash
npm create vite@latest 1_react -- --template react
```

프로젝트 실행은 다음 순서로 한다.

```bash
cd 1_react
npm install
npm run dev
```

`package.json`의 주요 스크립트는 다음과 같다.

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  }
}
```

- `npm run dev`: 개발 서버 실행
- `npm run build`: 배포용 파일 생성
- `npm run preview`: 빌드 결과 미리보기
- `npm run lint`: 코드 규칙 검사

## 5. React 앱의 시작점

Vite React 프로젝트에서 화면이 시작되는 핵심 파일은 `main.jsx`다.

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

여기서 중요한 흐름은 다음과 같다.

1. `index.html` 안의 `id="root"` 요소를 찾는다.
2. `createRoot()`로 React 앱이 렌더링될 기준점을 만든다.
3. `<App />` 컴포넌트를 화면에 렌더링한다.

즉, React는 `App.jsx`를 중심으로 컴포넌트들을 조립해 화면을 만든다.

## 6. JSX

JSX는 JavaScript 안에서 HTML처럼 UI 구조를 작성할 수 있게 해주는 문법이다.

```jsx
function App() {
  return (
    <>
      <h1>React 시작하기</h1>
      <p>컴포넌트 기반으로 화면을 만든다.</p>
    </>
  )
}
```

JSX를 사용할 때 주의할 점이 있다.

- 여러 태그를 반환할 때는 하나의 부모 요소로 감싸야 한다.
- `class` 대신 `className`을 사용한다.
- JavaScript 값을 사용할 때는 `{}`를 사용한다.
- 이벤트 이름은 `onClick`, `onChange`처럼 camelCase로 작성한다.

```jsx
const name = '김사과'

function App() {
  return <h1>{name}님 안녕하세요</h1>
}
```

## 7. 컴포넌트

컴포넌트는 React에서 화면을 구성하는 독립적인 UI 조각이다.

예를 들어 프로필 이미지를 보여주는 `Avatar` 컴포넌트는 다음과 같이 만들 수 있다.

```jsx
export default function Avatar({ image, isNew }) {
  return (
    <div className="avatar">
      <img className="photo" src={image} alt="사진" />
      {isNew && <span className="new">New</span>}
    </div>
  )
}
```

`Avatar` 컴포넌트는 `image`, `isNew` 값을 외부에서 전달받는다. 이렇게 부모 컴포넌트가 자식 컴포넌트에게 전달하는 값을 **props**라고 한다.

## 8. Props

Props는 부모 컴포넌트에서 자식 컴포넌트로 전달하는 데이터다.

```jsx
<Avatar image="profile.png" isNew={true} />
```

자식 컴포넌트에서는 구조 분해 할당으로 값을 받을 수 있다.

```jsx
function Avatar({ image, isNew }) {
  return (
    <div>
      <img src={image} alt="프로필" />
      {isNew && <span>New</span>}
    </div>
  )
}
```

Props는 읽기 전용 데이터다. 자식 컴포넌트가 props를 직접 수정하는 방식으로 사용하지 않는다.

## 9. 조건부 렌더링

React에서는 조건에 따라 특정 UI를 보여주거나 숨길 수 있다.

```jsx
{isNew && <span className="new">New</span>}
```

위 코드는 `isNew`가 `true`일 때만 `<span>`을 렌더링한다.

```text
isNew === true  -> New 표시
isNew === false -> 아무것도 표시하지 않음
```

이 방식은 배지, 경고 메시지, 로그인 상태 표시처럼 조건에 따라 화면 일부를 다르게 보여줄 때 유용하다.

## 10. 컴포넌트 조합

작은 컴포넌트는 더 큰 컴포넌트 안에서 조합할 수 있다.

```jsx
import Avatar from './Avatar'

export default function Profile({ image, name, title, isNew }) {
  return (
    <div className="profile">
      <Avatar image={image} isNew={isNew} />
      <h2>{name}</h2>
      <p>{title}</p>
    </div>
  )
}
```

`Profile` 컴포넌트는 내부에서 `Avatar` 컴포넌트를 사용한다. 이렇게 컴포넌트를 조합하면 UI 구조를 더 작은 단위로 나눌 수 있다.

사용 예시는 다음과 같다.

```jsx
<Profile
  image="https://example.com/profile.png"
  name="김사과"
  title="AI 개발자"
  isNew={false}
/>
```

## 11. useState

`useState`는 컴포넌트 안에서 값을 기억하고, 그 값이 바뀌면 화면을 다시 렌더링하는 Hook이다.

기본 형태는 다음과 같다.

```jsx
const [state, setState] = useState(초기값)
```

입력값을 상태로 관리하는 예시는 다음과 같다.

```jsx
import { useState } from 'react'

function InputUser() {
  const [inputs, setInputs] = useState({
    userid: '',
    password: ''
  })

  const { userid, password } = inputs

  const onChange = (e) => {
    const { value, name } = e.target

    setInputs({
      ...inputs,
      [name]: value
    })
  }

  const onReset = () => {
    setInputs({
      userid: '',
      password: ''
    })
  }

  return (
    <div>
      <input
        name="userid"
        placeholder="아이디를 입력하세요"
        value={userid}
        onChange={onChange}
      />
      <input
        type="password"
        name="password"
        placeholder="비밀번호를 입력하세요"
        value={password}
        onChange={onChange}
      />
      <button onClick={onReset}>초기화</button>
      <div>
        <b>값: {userid}({password})</b>
      </div>
    </div>
  )
}
```

### 객체 상태를 업데이트하는 이유

`inputs`는 객체 형태의 상태다.

```jsx
{
  userid: '',
  password: ''
}
```

객체 상태를 바꿀 때는 기존 객체를 직접 수정하지 않고, 새로운 객체를 만들어 전달한다.

```jsx
setInputs({
  ...inputs,
  [name]: value
})
```

여기서 `...inputs`는 기존 값을 복사한다. `[name]: value`는 현재 입력 중인 input의 `name` 값을 key로 사용해 해당 값만 바꾼다.

예를 들어 `name="userid"`인 input에 `apple`을 입력하면 다음처럼 동작한다.

```jsx
setInputs({
  userid: 'apple',
  password: ''
})
```

## 12. 배열 렌더링

여러 개의 데이터를 화면에 출력할 때는 배열과 `map()`을 사용한다.

```jsx
const users = [
  {
    id: 1,
    userid: 'apple',
    name: '김사과',
    email: 'apple@apple.com'
  },
  {
    id: 2,
    userid: 'banana',
    name: '반하나',
    email: 'banana@banana.com'
  },
  {
    id: 3,
    userid: 'orange',
    name: '오렌지',
    email: 'orange@orange.com'
  }
]
```

반복되는 사용자 UI는 `User` 컴포넌트로 분리할 수 있다.

```jsx
function User({ user }) {
  return (
    <div>
      <b>{user.userid}</b> <span>({user.name})</span>
    </div>
  )
}
```

그리고 `map()`으로 배열을 컴포넌트 목록으로 변환한다.

```jsx
function UserList() {
  return (
    <div>
      {users.map((user) => (
        <User user={user} key={user.id} />
      ))}
    </div>
  )
}
```

### key

React에서 배열을 렌더링할 때는 각 항목에 `key`를 지정해야 한다.

```jsx
<User user={user} key={user.id} />
```

`key`는 React가 어떤 항목이 추가, 변경, 삭제되었는지 구분하는 기준이다. 일반적으로 데이터가 가진 고유한 `id`를 사용한다.

## 13. useRef

`useRef`는 컴포넌트 안에서 값을 기억하는 상자 역할을 한다.

```jsx
const nextId = useRef(5)
```

`useRef`의 값은 `current`로 접근한다.

```jsx
console.log(nextId.current)
```

`useRef`의 중요한 특징은 다음과 같다.

- 값을 변경해도 화면이 다시 렌더링되지 않는다.
- 컴포넌트가 다시 렌더링되어도 값이 유지된다.
- DOM 요소를 직접 참조할 때도 사용할 수 있다.

사용자 id를 증가시키는 예시는 다음과 같다.

```jsx
const nextId = useRef(5)

const onCreate = () => {
  const user = {
    id: nextId.current,
    userid,
    name,
    email
  }

  setUsers([...users, user])
  nextId.current += 1
}
```

여기서 `nextId.current`는 새 사용자에게 부여할 id를 기억한다. id 값은 화면에 직접 표시되는 상태가 아니므로 `useState`보다 `useRef`가 적합하다.

## 14. 사용자 추가하기

`2_array` 예제에서는 입력값을 받아 사용자 배열에 새 데이터를 추가한다.

```jsx
const [inputs, setInputs] = useState({
  userid: '',
  name: '',
  email: ''
})

const { userid, name, email } = inputs
```

입력 컴포넌트는 부모로부터 값과 이벤트 함수를 props로 전달받는다.

```jsx
function CreateUser({ userid, name, email, onChange, onCreate }) {
  return (
    <div>
      <input
        name="userid"
        placeholder="아이디를 입력하세요"
        value={userid}
        onChange={onChange}
      />
      <input
        name="name"
        placeholder="이름을 입력하세요"
        value={name}
        onChange={onChange}
      />
      <input
        name="email"
        placeholder="이메일을 입력하세요"
        value={email}
        onChange={onChange}
      />
      <button onClick={onCreate}>등록</button>
    </div>
  )
}
```

새 사용자 추가 함수는 다음과 같다.

```jsx
const onCreate = () => {
  const user = {
    id: nextId.current,
    userid,
    name,
    email
  }

  setUsers([...users, user])

  setInputs({
    userid: '',
    name: '',
    email: ''
  })

  nextId.current += 1
}
```

핵심은 `setUsers([...users, user])`다. 기존 배열을 직접 수정하지 않고, 기존 배열을 복사한 뒤 새 사용자를 뒤에 추가한 새로운 배열을 만든다.

## 15. 사용자 삭제하기

사용자 삭제는 `filter()`를 사용한다.

```jsx
const onRemove = (id) => {
  setUsers(users.filter((user) => user.id !== id))
}
```

`filter()`는 조건을 만족하는 요소만 모아 새로운 배열을 만든다.

```text
삭제할 id: 2

기존 users:
1 apple
2 banana
3 orange

filter 결과:
1 apple
3 orange
```

React 상태 배열을 수정할 때는 원본 배열을 직접 바꾸지 않고, 새로운 배열을 만들어 `setUsers()`에 전달해야 한다.

## 16. 사용자 선택 토글하기

사용자 이름을 클릭했을 때 선택 상태를 바꾸는 코드는 다음과 같다.

```jsx
const onToggle = (id) => {
  setUsers(
    users.map((user) =>
      user.id === id
        ? { ...user, select: !user.select }
        : user
    )
  )
}
```

동작 방식은 다음과 같다.

1. `map()`으로 전체 사용자 배열을 순회한다.
2. 클릭한 사용자 id와 같은 사용자를 찾는다.
3. 해당 사용자만 `select` 값을 반대로 바꾼 새 객체로 만든다.
4. 나머지 사용자는 그대로 반환한다.

선택 여부에 따라 스타일도 바꿀 수 있다.

```jsx
<b
  style={{
    cursor: 'pointer',
    color: user.select ? 'deeppink' : 'black'
  }}
  onClick={() => onToggle(user.id)}
>
  {user.userid}
</b>
```

`user.select`가 `true`이면 글자색이 `deeppink`가 되고, `false`이면 `black`이 된다.

## 17. 이벤트 핸들러

React에서 이벤트는 JSX 속성으로 연결한다.

```jsx
<button onClick={onCreate}>등록</button>
```

인자를 전달해야 할 때는 화살표 함수로 감싼다.

```jsx
<button onClick={() => onRemove(user.id)}>삭제</button>
```

아래처럼 바로 실행하면 안 된다.

```jsx
<button onClick={onRemove(user.id)}>삭제</button>
```

위 코드는 버튼을 클릭했을 때 실행되는 것이 아니라, 렌더링되는 순간 함수가 바로 실행될 수 있다.

## 18. useEffect

`useEffect`는 컴포넌트가 렌더링된 이후에 실행할 작업을 등록하는 Hook이다. 외부 시스템과의 동기화, 콘솔 확인, API 요청, 이벤트 등록, 타이머 설정 등에 사용된다.

기본 형태는 다음과 같다.

```jsx
useEffect(() => {
  실행할 작업

  return () => {
    정리 작업
  }
}, [의존성])
```

예제에서는 사용자 데이터가 설정되거나 바뀔 때 콘솔을 출력한다.

```jsx
import { useEffect } from 'react'

function User({ user, onRemove, onToggle }) {
  useEffect(() => {
    console.log('user 설정: ', user)

    return () => {
      console.log('user 바뀌기 전: ', user)
    }
  }, [user])

  console.log('User 컴포넌트 실행!')

  return (
    <div>
      <b
        style={{
          cursor: 'pointer',
          color: user.select ? 'deeppink' : 'black'
        }}
        onClick={() => onToggle(user.id)}
      >
        {user.userid}
      </b>
      <span>({user.name} / {user.email})</span>
      <button onClick={() => onRemove(user.id)}>삭제</button>
    </div>
  )
}
```

### useEffect 실행 흐름

```text
1. 컴포넌트 함수 실행
2. JSX 생성
3. 화면 렌더링
4. useEffect 실행
5. 의존성 배열의 값이 바뀌면 cleanup 실행
6. 새로운 useEffect 실행
7. 컴포넌트가 사라질 때 cleanup 실행
```

예를 들어 `user` 값이 A에서 B로 바뀌면 다음처럼 동작한다.

```text
초기 렌더링: user 설정: A
user 변경: user 바뀌기 전: A
user 변경: user 설정: B
컴포넌트 제거: user 바뀌기 전: B
```

의존성 배열 `[user]`는 `user` 값이 바뀔 때만 effect를 다시 실행하겠다는 의미다.

## 19. 상태 불변성

React에서 배열이나 객체 상태를 수정할 때는 기존 값을 직접 바꾸지 않는다. 대신 새로운 배열이나 객체를 만들어 상태를 업데이트한다.

좋은 예시는 다음과 같다.

```jsx
setUsers([...users, user])
```

```jsx
setUsers(users.filter((user) => user.id !== id))
```

```jsx
setUsers(
  users.map((user) =>
    user.id === id ? { ...user, select: !user.select } : user
  )
)
```

피해야 할 예시는 다음과 같다.

```jsx
users.push(user)
setUsers(users)
```

```jsx
users[0].select = true
setUsers(users)
```

기존 배열이나 객체를 직접 수정하면 React가 상태 변경을 제대로 감지하지 못하거나, 예측하기 어려운 렌더링 문제가 생길 수 있다.

## 20. CSS 적용

React에서는 일반 CSS 파일을 import해서 사용할 수 있다.

```jsx
import './App.css'
```

컴포넌트에서는 `className`으로 CSS 클래스를 적용한다.

```jsx
<div className="profile">
  <img className="photo" src={image} alt="사진" />
</div>
```

예제의 프로필 스타일은 다음과 같다.

```css
.profile {
  width: 300px;
  text-align: center;
  padding: 1rem;
  background-color: #ebebeb;
  border-radius: 20px;
  box-shadow: 7px 5px 23px -9px rgba(0, 0, 0, 0.75);
  margin-bottom: 1rem;
}

.photo {
  width: 200px;
  height: 200px;
  border-radius: 100%;
}

.avatar {
  position: relative;
  width: 200px;
  height: 200px;
  margin: auto;
}

.new {
  position: absolute;
  left: 70%;
  top: 10%;
  background-color: deepskyblue;
  padding: 0.2rem 0.5rem;
  border-radius: 0.5rem;
  text-transform: uppercase;
  font-weight: bold;
}
```

## 21. 전체 예제 흐름

`2_array` 프로젝트의 전체 구조는 다음과 같다.

```text
App
├── CreateUser
│   ├── userid input
│   ├── name input
│   ├── email input
│   └── 등록 button
└── UserList
    └── User
        ├── 사용자 정보 출력
        ├── 선택 토글
        └── 삭제 button
```

부모 컴포넌트인 `App`은 사용자 배열과 입력 상태를 관리한다.

```jsx
const [inputs, setInputs] = useState({
  userid: '',
  name: '',
  email: ''
})

const [users, setUsers] = useState([
  {
    id: 1,
    userid: 'apple',
    name: '김사과',
    email: 'apple@apple.com',
    select: true
  }
])
```

`CreateUser`는 입력과 등록 버튼을 담당한다.

```jsx
<CreateUser
  userid={userid}
  name={name}
  email={email}
  onChange={onChange}
  onCreate={onCreate}
/>
```

`UserList`는 사용자 목록 출력을 담당한다.

```jsx
<UserList
  users={users}
  onRemove={onRemove}
  onToggle={onToggle}
/>
```

이 구조에서 데이터는 부모인 `App`이 가지고 있고, 자식 컴포넌트는 props로 필요한 값과 함수를 전달받아 사용한다.

## 22. 정리

React를 사용할 때 중요한 흐름은 다음과 같다.

1. 화면을 컴포넌트 단위로 나눈다.
2. 부모 컴포넌트에서 데이터를 관리한다.
3. 자식 컴포넌트에는 props로 값을 전달한다.
4. 값이 바뀌어야 하는 데이터는 `useState`로 관리한다.
5. 렌더링과 관계없는 값은 `useRef`로 관리할 수 있다.
6. 반복되는 UI는 배열과 `map()`으로 렌더링한다.
7. 배열을 렌더링할 때는 고유한 `key`를 지정한다.
8. 배열이나 객체 상태는 직접 수정하지 않고 새 값으로 업데이트한다.
9. 렌더링 이후의 부가 작업은 `useEffect`로 처리한다.

이번 예제의 핵심은 단순히 화면을 출력하는 것에서 끝나지 않고, 사용자의 입력을 상태로 관리하고, 배열 데이터를 추가·삭제·수정하며, 컴포넌트 간에 데이터를 주고받는 React의 기본 흐름을 익히는 것이다.