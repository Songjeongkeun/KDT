# [36일차] React

## 1. React Developer Tools

React Developer Tools는 브라우저에서 React 앱의 컴포넌트 구조와 상태를 확인할 수 있는 확장 프로그램이다.

일반 개발자 도구의 `Elements` 탭은 실제 HTML DOM 구조를 보여준다. 반면 React Developer Tools의 `Components` 탭은 React 컴포넌트 기준으로 화면 구조를 보여준다.

| 구분 | Elements 탭 | Components 탭 |
| --- | --- | --- |
| 확인 대상 | 실제 HTML DOM | React 컴포넌트 |
| 주요 내용 | 태그, CSS, 실제 렌더링 구조 | props, state, hooks, component tree |
| 사용 목적 | 화면 구조와 스타일 확인 | React 데이터 흐름과 렌더링 확인 |

React Developer Tools로 확인할 수 있는 내용은 다음과 같다.

- 컴포넌트 트리
- 컴포넌트가 받은 props
- 컴포넌트 내부 state
- 사용 중인 Hooks
- Context 값
- 컴포넌트가 다시 렌더링되는 원인

React 앱을 만들 때 화면이 예상대로 바뀌지 않으면, 단순히 DOM만 보는 것보다 React Developer Tools로 컴포넌트의 props와 state를 확인하는 것이 더 효과적이다.

## 2. fetch로 JSON 데이터 불러오기

React에서는 외부 데이터나 정적 JSON 파일을 불러올 때 `fetch()`를 사용할 수 있다.

예제에서는 `public/data/products.json`과 `public/data/sale_products.json` 파일을 불러온다.

```json
[
  {
    "id": "1001",
    "name": "아이폰",
    "price": "1800000"
  },
  {
    "id": "1002",
    "name": "Z플립",
    "price": "1600000"
  }
]
```

세일 상품 파일은 같은 상품이지만 가격이 더 낮게 저장되어 있다.

```json
[
  {
    "id": "1001",
    "name": "아이폰",
    "price": "1500000"
  },
  {
    "id": "1002",
    "name": "Z플립",
    "price": "1300000"
  }
]
```

React 프로젝트에서 `public` 폴더 안의 파일은 브라우저 기준 경로로 접근할 수 있다.

```jsx
fetch('data/products.json')
```

즉, `public/data/products.json` 파일은 코드에서 `data/products.json` 경로로 요청할 수 있다.

## 3. Products 컴포넌트

상품 목록을 불러오는 기본 컴포넌트는 다음과 같은 상태를 사용한다.

```jsx
const [loading, setLoading] = useState(false)
const [checked, setChecked] = useState(false)
const [error, setError] = useState()
const [products, setProducts] = useState([])
```

각 상태의 역할은 다음과 같다.

| 상태 | 역할 |
| --- | --- |
| `loading` | 데이터를 불러오는 중인지 확인 |
| `checked` | 세일 상품만 볼지 여부 확인 |
| `error` | 데이터 요청 중 에러가 발생했는지 확인 |
| `products` | 화면에 출력할 상품 목록 저장 |

전체 코드는 다음과 같다.

```jsx
import React, { useEffect, useState } from "react"

export default function Products() {
  const [loading, setLoading] = useState(false)
  const [checked, setChecked] = useState(false)
  const [error, setError] = useState()
  const [products, setProducts] = useState([])

  const handleChange = () => setChecked((prev) => !prev)

  useEffect(() => {
    setLoading(true)
    setError(undefined)

    fetch(`data/${checked ? "sale_" : ""}products.json`)
      .then((res) => res.json())
      .then((data) => {
        console.log("네트워크에서 데이터를 잘 불러옴")
        setProducts(data)
      })
      .catch((e) => setError("에러가 발생함!"))
      .finally(() => setLoading(false))

    return () => {
      console.log("데이터 처리 완료")
    }
  }, [checked])

  if (loading) return <p>Loading 중...</p>
  if (error) return <p>{error}</p>

  return (
    <>
      <input
        id="checkbox"
        type="checkbox"
        checked={checked}
        value={checked}
        onChange={handleChange}
      />
      <label htmlFor="checkbox">세일상품보기</label>

      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <article>
              <h3>{product.name}</h3>
              <p>{product.price}</p>
            </article>
          </li>
        ))}
      </ul>
    </>
  )
}
```

## 4. checked 값에 따라 다른 파일 요청하기

아래 코드는 `checked` 값에 따라 불러올 JSON 파일을 바꾼다.

```jsx
fetch(`data/${checked ? "sale_" : ""}products.json`)
```

동작 방식은 다음과 같다.

```text
checked === false
-> data/products.json 요청

checked === true
-> data/sale_products.json 요청
```

즉, 체크박스를 선택하지 않으면 일반 상품 목록을 불러오고, 체크박스를 선택하면 세일 상품 목록을 불러온다.

체크박스 상태를 바꾸는 함수는 다음과 같다.

```jsx
const handleChange = () => setChecked((prev) => !prev)
```

여기서 `prev`는 이전 `checked` 값이다.

```text
false -> true
true -> false
```

상태를 이전 값 기준으로 바꿀 때는 `setChecked(!checked)`보다 `setChecked((prev) => !prev)` 형태가 더 안정적이다.

## 5. 로딩과 에러 처리

데이터를 요청할 때는 성공 상황만 생각하면 안 된다.

요청이 진행 중일 수도 있고, 파일 경로가 잘못되거나 서버 문제가 생길 수도 있다. 그래서 로딩 상태와 에러 상태를 따로 관리한다.

```jsx
setLoading(true)
setError(undefined)
```

요청을 시작하기 전에 `loading`을 `true`로 만들고, 이전 에러 메시지는 초기화한다.

```jsx
.catch((e) => setError("에러가 발생함!"))
.finally(() => setLoading(false))
```

요청 중 문제가 생기면 `error`에 메시지를 저장한다. 요청이 성공하든 실패하든 마지막에는 `finally()`가 실행되어 `loading`을 `false`로 바꾼다.

화면에서는 조건부 렌더링으로 상태에 따라 다른 UI를 보여준다.

```jsx
if (loading) return <p>Loading 중...</p>
if (error) return <p>{error}</p>
```

이 구조는 다음 순서로 동작한다.

```text
1. loading이 true면 로딩 문구 출력
2. error가 있으면 에러 문구 출력
3. 둘 다 아니면 상품 목록 출력
```

## 6. 커스텀 Hook

커스텀 Hook은 여러 컴포넌트에서 반복되는 Hook 로직을 별도의 함수로 분리한 것이다.

React에서 커스텀 Hook 이름은 반드시 `use`로 시작하는 것이 관례다.

```jsx
useProducts
useInput
useFetch
```

`use`로 시작해야 React Hook 규칙을 따르는 함수라는 것을 알 수 있고, ESLint가 Hook 사용 규칙도 검사할 수 있다.

## 7. useProducts 커스텀 Hook

상품 데이터를 불러오는 로직은 컴포넌트 안에 직접 작성할 수도 있지만, 데이터 요청 로직이 길어지면 UI 코드와 데이터 처리 코드가 섞인다.

이를 분리하기 위해 `useProducts` 커스텀 Hook을 만들 수 있다.

```jsx
import React, { useState, useEffect } from "react"

export default function useProducts({ salesOnly }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState()
  const [products, setProducts] = useState([])

  useEffect(() => {
    setLoading(true)
    setError(undefined)

    fetch(`data/${salesOnly ? "sale_" : ""}products.json`)
      .then((res) => res.json())
      .then((data) => {
        console.log("네트워크에서 데이터를 잘 불러옴")
        setProducts(data)
      })
      .catch((e) => setError("에러가 발생함!"))
      .finally(() => setLoading(false))

    return () => {
      console.log("데이터 처리 완료")
    }
  }, [salesOnly])

  return [loading, error, products]
}
```

이 Hook은 `salesOnly` 값을 받아서 일반 상품 또는 세일 상품을 불러온다.

```jsx
fetch(`data/${salesOnly ? "sale_" : ""}products.json`)
```

그리고 컴포넌트에서 사용할 수 있도록 세 가지 값을 반환한다.

```jsx
return [loading, error, products]
```

## 8. 커스텀 Hook을 사용하는 컴포넌트

커스텀 Hook을 사용하면 컴포넌트는 UI 흐름에 더 집중할 수 있다.

```jsx
import React, { useState } from "react"
import useProducts from "../hooks/useProducts"

export default function Products() {
  const [checked, setChecked] = useState(false)
  const [loading, error, products] = useProducts({ salesOnly: checked })

  const handleChange = () => setChecked((prev) => !prev)

  if (loading) return <p>Loading 중...</p>
  if (error) return <p>{error}</p>

  return (
    <>
      <input
        id="checkbox"
        type="checkbox"
        checked={checked}
        value={checked}
        onChange={handleChange}
      />
      <label htmlFor="checkbox">세일상품보기</label>

      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <article>
              <h3>{product.name}</h3>
              <p>{product.price}</p>
            </article>
          </li>
        ))}
      </ul>
    </>
  )
}
```

기존 `Products` 컴포넌트에 있던 `loading`, `error`, `products`, `fetch`, `useEffect` 로직이 `useProducts`로 이동했다.

그 결과 컴포넌트는 다음 역할만 담당한다.

- 체크박스 상태 관리
- 로딩/에러 화면 처리
- 상품 목록 출력

데이터를 가져오는 로직은 커스텀 Hook이 담당한다.

## 9. 컴포넌트 표시/숨김과 언마운트

`App.jsx`에서는 버튼을 눌러 상품 목록 컴포넌트를 보이거나 숨긴다.

```jsx
import React, { useState } from "react"
import Products from "./components/ProductHook"

function App() {
  const [showProducts, setShowProducts] = useState(true)

  return (
    <>
      <div>
        {showProducts && <Products />}
        <button onClick={() => setShowProducts((show) => !show)}>
          제품 보기
        </button>
      </div>
    </>
  )
}

export default App
```

여기서 핵심은 다음 코드다.

```jsx
{showProducts && <Products />}
```

`showProducts`가 `true`이면 `Products` 컴포넌트가 화면에 나타난다. `false`이면 화면에서 사라진다.

```text
showProducts === true
-> Products mount

showProducts === false
-> Products unmount
```

컴포넌트가 사라질 때 `useEffect`의 cleanup 함수가 실행된다.

```jsx
return () => {
  console.log("데이터 처리 완료")
}
```

## 10. useReducer

`useReducer`는 상태 변경 종류가 여러 개일 때 상태 변경 규칙을 하나의 함수로 관리하는 Hook이다.

`useState`는 간단한 상태를 관리할 때 편하다. 하지만 상태 구조가 복잡하거나, 상태를 바꾸는 방식이 여러 개라면 `useReducer`를 사용하는 편이 더 명확할 수 있다.

기본 형태는 다음과 같다.

```jsx
const [state, dispatch] = useReducer(reducer, initialState)
```

각 요소의 의미는 다음과 같다.

| 요소 | 의미 |
| --- | --- |
| `state` | 현재 상태 |
| `dispatch` | 상태 변경 요청을 보내는 함수 |
| `reducer` | 상태를 어떤 방식으로 바꿀지 정의한 함수 |
| `initialState` | 처음 사용할 초기 상태 |

전체 흐름은 다음과 같다.

```text
사용자 이벤트 발생
  ↓
dispatch 실행
  ↓
action 객체 전달
  ↓
reducer 실행
  ↓
새로운 state 반환
  ↓
React가 상태 저장
  ↓
컴포넌트 리렌더링
```

## 11. useReducer 예제

멘토 목록을 관리한다고 가정하면 상태 변경 종류는 여러 개가 될 수 있다.

- 멘토 추가
- 멘토 이름 수정
- 멘토 삭제

이런 경우 상태 변경 로직을 reducer 함수 안에 모을 수 있다.

```jsx
import { useReducer } from "react"

const initialState = {
  name: "김사과",
  title: "프로젝트 매니저",
  mentors: []
}

function reducer(state, action) {
  switch (action.type) {
    case "ADD":
      return {
        ...state,
        mentors: [
          ...state.mentors,
          {
            name: action.name,
            title: action.title
          }
        ]
      }

    case "UPDATE":
      return {
        ...state,
        mentors: state.mentors.map((mentor) =>
          mentor.name === action.prev
            ? { ...mentor, name: action.next }
            : mentor
        )
      }

    case "DELETE":
      return {
        ...state,
        mentors: state.mentors.filter((mentor) => mentor.name !== action.name)
      }

    default:
      return state
  }
}

function App() {
  const [state, dispatch] = useReducer(reducer, initialState)

  const handleAdd = () => {
    const name = prompt("멘토의 이름을 입력하세요")
    const title = prompt("멘토의 직함을 입력하세요")

    dispatch({
      type: "ADD",
      name,
      title
    })
  }

  return (
    <div>
      <h1>{state.name} {state.title}</h1>
      <button onClick={handleAdd}>멘토 추가하기</button>
    </div>
  )
}
```

`dispatch()`에는 상태를 직접 바꾸는 코드가 들어가지 않는다. 대신 어떤 작업을 할지 나타내는 `action` 객체를 전달한다.

```jsx
dispatch({
  type: "ADD",
  name,
  title
})
```

실제 상태 변경은 `reducer` 함수가 담당한다.

## 12. useState와 useReducer 차이

| 구분 | useState | useReducer |
| --- | --- | --- |
| 사용 상황 | 단순한 상태 관리 | 복잡한 상태 관리 |
| 상태 변경 방식 | setter 함수로 직접 변경 | dispatch로 action 전달 |
| 로직 위치 | 컴포넌트 내부에 흩어질 수 있음 | reducer 함수에 모을 수 있음 |
| 예시 | input 값, checkbox 값 | 추가/수정/삭제가 있는 객체·배열 상태 |

간단한 값 하나를 바꾸는 정도라면 `useState`가 더 쉽다.

```jsx
const [checked, setChecked] = useState(false)
```

하지만 상태 변경 방식이 여러 개라면 `useReducer`가 더 읽기 쉬울 수 있다.

```jsx
dispatch({ type: "ADD", name, title })
dispatch({ type: "UPDATE", prev, next })
dispatch({ type: "DELETE", name })
```

## 13. useCallback

`useCallback`은 함수 자체를 기억하는 Hook이다.

React 함수형 컴포넌트는 렌더링될 때마다 함수 전체가 다시 실행된다. 따라서 컴포넌트 내부에서 선언한 함수도 렌더링될 때마다 새로 만들어진다.

```jsx
function App() {
  const handleAdd = () => {
    console.log("추가")
  }
}
```

`App`이 다시 렌더링되면 새로운 `handleAdd` 함수 객체가 만들어진다.

```text
이전 handleAdd !== 새로운 handleAdd
```

이 자체가 항상 문제는 아니다. 하지만 자식 컴포넌트에 함수를 props로 전달하고, 자식 컴포넌트가 `memo`로 최적화되어 있다면 함수 참조가 매번 바뀌는 것이 불필요한 렌더링을 만들 수 있다.

이때 `useCallback`을 사용할 수 있다.

```jsx
const handleAdd = useCallback(() => {
  const name = prompt("멘토의 이름을 입력하세요")
  const title = prompt("멘토의 직함을 입력하세요")
}, [])
```

의존성 배열 `[]` 안의 값이 바뀌지 않으면 React는 이전에 만든 함수를 재사용한다.

## 14. useCallback 예제

예제 코드에서는 버튼 클릭 함수들을 `useCallback`으로 감싸고 있다.

```jsx
import React, { useCallback } from "react"

function App() {
  const handleAdd = useCallback(() => {
    const name = prompt("멘토의 이름을 입력하세요")
    const title = prompt("멘토의 직함을 입력하세요")
  })

  const handleUpdate = useCallback(() => {
    const prev = prompt("변경 이전의 멘토 이름을 입력하세요")
    const title = prompt("변경 이후의 멘토 이름을 입력하세요")
  })

  const handleDelete = useCallback(() => {
    const name = prompt("삭제할 멘토 이름을 입력하세요")
  })

  return (
    <>
      <div>
        <h1>김사과 프로젝트 매니저</h1>
        <p>김사과의 멘토는: </p>
        <Button text="멘토 추가하기" onClick={handleAdd} />
        <Button text="멘토 이름 바꾸기" onClick={handleUpdate} />
        <Button text="멘토 삭제하기" onClick={handleDelete} />
      </div>
    </>
  )
}
```

위 코드의 의도는 버튼 컴포넌트에 전달되는 함수 참조를 기억해서, 불필요한 렌더링을 줄이는 것이다.

실무에서는 `useCallback`을 무조건 사용하는 것이 아니라, 다음 상황에서 주로 사용한다.

- 함수를 자식 컴포넌트에 props로 전달한다.
- 자식 컴포넌트가 `memo`로 최적화되어 있다.
- 함수 참조가 바뀌어서 불필요한 렌더링이 발생한다.

## 15. memo

`memo`는 컴포넌트의 props가 바뀌지 않았다면 이전 렌더링 결과를 재사용하게 해주는 최적화 함수다.

```jsx
import { memo } from "react"

const Button = memo(({ text, onClick }) => {
  console.log("Button", text, "렌더링 되었음!")

  return (
    <button onClick={onClick}>
      {text}
    </button>
  )
})
```

`memo`를 사용하면 부모 컴포넌트가 다시 렌더링되어도, `Button`이 받은 props가 이전과 같다면 `Button`은 다시 렌더링되지 않을 수 있다.

하지만 props로 전달되는 함수가 매번 새로 만들어지면 React는 props가 바뀌었다고 판단할 수 있다.

```text
이전 onClick 함수 !== 새로운 onClick 함수
```

그래서 `memo`와 `useCallback`은 함께 사용되는 경우가 많다.

```jsx
const handleAdd = useCallback(() => {
  console.log("추가")
}, [])

<Button text="멘토 추가하기" onClick={handleAdd} />
```

## 16. useMemo

`useMemo`는 계산된 결과값을 기억하는 Hook이다.

`useCallback`이 함수를 기억한다면, `useMemo`는 함수 실행 결과인 값을 기억한다.

기본 형태는 다음과 같다.

```jsx
const memoizedValue = useMemo(() => {
  return 계산결과
}, [의존성])
```

의존성 배열의 값이 바뀌지 않으면 이전에 계산한 값을 재사용한다.

## 17. useMemo 예제

예제에서는 계산 비용이 큰 함수가 있다고 가정한다.

```jsx
function calculator() {
  for (let i = 0; i < 10000; i++) {
    console.log("😝")
  }
  return 10000
}
```

이 함수가 렌더링될 때마다 실행되면 콘솔 출력이 반복되고 성능에도 부담이 될 수 있다.

`Button` 컴포넌트에서는 `useMemo`로 계산 결과를 기억한다.

```jsx
const Button = memo(({ text, onClick }) => {
  console.log("Button", text, "렌더링 되었음!")

  const result = useMemo(() => calculator(), [])

  return (
    <button
      onClick={onClick}
      style={{
        backgroundColor: "deepskyblue",
        color: "white",
        borderRadius: "20px",
        margin: "0.4rem",
        padding: "20px"
      }}
    >
      {`${text} ${result}`}
    </button>
  )
})
```

```jsx
const result = useMemo(() => calculator(), [])
```

의존성 배열이 비어 있기 때문에 `calculator()`는 처음 렌더링될 때만 실행되고, 이후에는 이전 계산 결과를 재사용한다.

## 18. useCallback과 useMemo 차이

두 Hook은 모두 렌더링 최적화와 관련이 있다. 하지만 기억하는 대상이 다르다.

| 구분 | useCallback | useMemo |
| --- | --- | --- |
| 기억하는 것 | 함수 자체 | 계산된 결과값 |
| 반환값 | 함수 | 값 |
| 주 사용 목적 | 자식 컴포넌트에 전달하는 함수 참조 유지 | 무거운 계산 결과 재사용 |
| 자주 함께 쓰는 것 | `memo` | 비용이 큰 계산 함수 |

예를 들어 다음 코드는 함수를 기억한다.

```jsx
const handleAdd = useCallback(() => {
  console.log("추가")
}, [])
```

반면 다음 코드는 계산 결과를 기억한다.

```jsx
const result = useMemo(() => calculator(), [])
```

## 19. 최적화 Hook을 사용할 때 주의할 점

`useCallback`, `useMemo`, `memo`는 성능 최적화를 위한 도구다. 하지만 무조건 많이 사용한다고 좋은 것은 아니다.

오히려 단순한 컴포넌트에 과도하게 사용하면 코드가 복잡해지고, 의존성 배열 관리가 어려워질 수 있다.

사용하면 좋은 경우는 다음과 같다.

- 자식 컴포넌트가 자주 불필요하게 렌더링된다.
- 자식 컴포넌트가 `memo`로 감싸져 있다.
- props로 전달되는 함수 참조를 유지해야 한다.
- 계산 비용이 큰 함수가 렌더링마다 실행된다.
- 리스트나 복잡한 UI에서 렌더링 비용이 커진다.

굳이 사용하지 않아도 되는 경우는 다음과 같다.

- 컴포넌트가 작고 렌더링 비용이 거의 없다.
- 계산이 가볍다.
- props 변경 여부를 최적화할 필요가 없다.
- 코드 가독성이 더 중요하다.

즉, 최적화 Hook은 문제가 보일 때 적용하는 것이 좋다.

## 20. 오늘 코드 흐름 정리

이번 예제는 크게 두 흐름으로 나눌 수 있다.

첫 번째 흐름은 상품 데이터를 불러오는 예제다.

```text
App
└── ProductHook
    ├── checked 상태 관리
    ├── useProducts 호출
    ├── loading / error 처리
    └── products 출력

useProducts
├── loading 상태 관리
├── error 상태 관리
├── products 상태 관리
├── salesOnly 값에 따라 JSON 파일 요청
└── [loading, error, products] 반환
```

두 번째 흐름은 렌더링 최적화 예제다.

```text
App
├── handleAdd    -> useCallback
├── handleUpdate -> useCallback
├── handleDelete -> useCallback
└── Button       -> memo
                   └── calculator 결과 -> useMemo
```

이 구조를 통해 React에서 데이터 요청 로직을 분리하는 방법과, 컴포넌트 렌더링을 최적화하는 기본 방법을 확인할 수 있다.

## 21. 정리

이번 내용의 핵심은 다음과 같다.

1. React Developer Tools를 사용하면 컴포넌트의 props, state, hooks를 확인할 수 있다.
2. `fetch()`를 사용해 JSON 데이터를 불러올 수 있다.
3. 데이터 요청 시 `loading`, `error`, `data` 상태를 나누어 관리하면 화면 처리가 명확해진다.
4. 체크박스 상태에 따라 일반 상품과 세일 상품 데이터를 다르게 요청할 수 있다.
5. 반복되는 데이터 요청 로직은 커스텀 Hook으로 분리할 수 있다.
6. 커스텀 Hook 이름은 `use`로 시작하는 것이 관례다.
7. `useReducer`는 상태 변경 방식이 여러 개일 때 로직을 한곳에 모아 관리하기 좋다.
8. `useCallback`은 함수 참조를 기억한다.
9. `memo`는 props가 바뀌지 않은 컴포넌트의 불필요한 렌더링을 줄인다.
10. `useMemo`는 계산된 결과값을 기억한다.

기존 React 기초가 화면 구성과 상태 관리의 출발점이었다면, 이번 내용은 데이터 요청 로직을 분리하고 렌더링 성능을 관리하는 쪽으로 한 단계 확장된 내용이다.
