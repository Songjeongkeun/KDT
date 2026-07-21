# React + Express + MongoDB CRUD 수업 복습 노트

> 작성 기준: 현재 `8_CRUDProject` 코드  
> 핵심 주제: React에서 입력받은 상품 정보를 Express API로 보내고 MongoDB에 저장·조회·수정·삭제하기

---

## 1. 오늘 만든 프로젝트 한눈에 보기

이 프로젝트는 상품의 **등록(Create), 조회(Read), 수정(Update), 삭제(Delete)** 기능을 구현한 풀스택 CRUD 애플리케이션이다.

```text
사용자
  ↓ 입력·버튼 클릭
React 프런트엔드 (localhost:5173)
  ↓ HTTP 요청: fetch()
Express 백엔드 (127.0.0.1:5001)
  ↓ Mongoose 메서드
MongoDB
```

각 기술의 역할은 다음과 같다.

| 기술 | 역할 |
|---|---|
| React | 화면 표시, 입력값과 상품 목록 상태 관리 |
| Vite | React 개발 서버 실행 및 빌드 |
| Fetch API | 프런트엔드에서 백엔드로 HTTP 요청 전송 |
| Express | API 주소와 요청 처리 로직 구성 |
| Mongoose | JavaScript 코드로 MongoDB 조작 |
| MongoDB | 상품 데이터를 실제로 저장 |
| CORS | 서로 다른 출처의 프런트엔드 요청 허용 |
| dotenv | `.env`의 환경변수 사용 |

---

## 2. CRUD와 HTTP 요청 연결하기

CRUD는 데이터 처리의 가장 기본적인 네 가지 기능이다.

| 기능 | 의미 | HTTP 메서드 | API 주소 | Mongoose 메서드 |
|---|---|---|---|---|
| Create | 상품 등록 | `POST` | `/api/products` | `Product.create()` |
| Read | 전체 조회 | `GET` | `/api/products` | `Product.find()` |
| Read | 하나 조회 | `GET` | `/api/products/:id` | `Product.findById()` |
| Update | 상품 수정 | `PUT` | `/api/products/:id` | `Product.findByIdAndUpdate()` |
| Delete | 상품 삭제 | `DELETE` | `/api/products/:id` | `Product.findByIdAndDelete()` |

`/:id`는 실제 글자가 아니라 상품마다 MongoDB가 부여한 `_id`가 들어가는 자리다.

```text
/api/products/6690abcdef1234567890abcd
              └──── 상품의 _id ────┘
```

---

## 3. 백엔드 구조 이해하기

```text
backend/
├── server.js            서버 설정 및 실행
├── models/
│   └── Product.js       상품 데이터의 형태 정의
└── routes/
    └── products.js      상품 CRUD API 정의
```

### 3-1. `server.js`: 서버의 시작점

주요 처리 순서는 다음과 같다.

```js
dotenv.config()
const app = express()

app.use(cors(/* 설정 */))
app.use(express.json())
app.use("/api/products", productRouter)

await mongoose.connect(MONGODB_URI)
app.listen(PORT)
```

#### `dotenv.config()`

`.env`에 저장된 값을 `process.env`로 읽을 수 있게 한다.

```js
const PORT = process.env.PORT || 5001
const MONGODB_URI = process.env.MONGODB_URI
```

- 환경변수에 `PORT`가 있으면 그 값을 사용한다.
- 값이 없으면 `5001`을 기본값으로 사용한다.
- 데이터베이스 주소처럼 외부에 공개하면 안 되는 값은 `.env`로 분리한다.

#### `express.json()`

클라이언트가 보낸 JSON 요청 본문을 `req.body`로 읽을 수 있게 한다.

```js
app.use(express.json())
```

이 코드가 없으면 다음 요청의 `name`, `price`를 정상적으로 꺼내기 어렵다.

```json
{
  "name": "키보드",
  "price": 50000
}
```

#### 라우터 연결

```js
app.use("/api/products", productRouter)
```

라우터 내부의 `/` 앞에 `/api/products`가 붙는다.

```text
router.get("/")       → GET /api/products
router.get("/:id")   → GET /api/products/:id
router.post("/")      → POST /api/products
```

#### MongoDB 연결 후 서버 실행

```js
await mongoose.connect(MONGODB_URI)
app.listen(PORT)
```

DB 연결이 성공한 다음 HTTP 서버를 시작한다. `await`를 사용하려면 해당 코드를 감싼 함수에 `async`가 필요하다.

```js
const startServer = async () => {
  // 여기에서 await 사용 가능
}
```

---

### 3-2. `Product.js`: 상품 스키마와 모델

스키마(schema)는 MongoDB에 저장할 데이터의 규칙을 정의한다.

```js
const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true
    },
    price: {
      type: Number,
      required: true,
      min: 0
    }
  },
  { timestamps: true }
)
```

| 옵션 | 의미 |
|---|---|
| `type` | 저장할 값의 자료형 |
| `required` | 반드시 입력해야 하는 값인지 검사 |
| `trim` | 문자열 앞뒤 공백 제거 |
| `min: 0` | 가격이 0보다 작은지 검사 |
| `timestamps: true` | `createdAt`, `updatedAt` 자동 생성 |

모델(model)은 이 규칙을 사용해 실제 DB 작업을 수행하는 객체다.

```js
const Product = mongoose.model("Product", productSchema)
```

이후 `Product.find()`, `Product.create()` 같은 메서드를 사용할 수 있다.

---

### 3-3. `products.js`: REST API 구현

#### 전체 상품 조회

```js
const products = await Product.find().sort({ createdAt: -1 })
res.status(200).json(products)
```

- `find()`는 모든 상품을 조회한다.
- `sort({ createdAt: -1 })`는 최신 상품부터 정렬한다.
- `json()`은 데이터를 JSON 형식으로 응답한다.

#### 상품 등록

```js
const { name, price } = req.body
const product = await Product.create({ name, price })
res.status(201).json(product)
```

- 구조 분해 할당으로 요청 본문에서 값을 꺼낸다.
- 새 데이터가 생성되면 `201 Created`로 응답한다.

#### 상품 수정

```js
const updatedProduct = await Product.findByIdAndUpdate(
  id,
  { name, price },
  { new: true, runValidators: true }
)
```

| 옵션 | 의미 |
|---|---|
| `new: true` | 수정 전 데이터가 아니라 수정된 최신 데이터 반환 |
| `runValidators: true` | 수정할 때도 스키마 유효성 검사 실행 |

#### 상품 삭제

```js
const deletedProduct = await Product.findByIdAndDelete(id)
```

`id`에 해당하는 상품을 찾아 삭제하고, 삭제된 데이터를 반환한다. 존재하지 않으면 `null`을 반환한다.

#### MongoDB ID 검사

```js
if (!mongoose.isValidObjectId(id)) {
  return res.status(400).json({
    message: "올바르지 않은 상품 ID입니다."
  })
}
```

잘못된 형식의 ID를 DB에 바로 전달하지 않고 먼저 차단한다. 여기서 `return`은 응답을 보낸 뒤 아래 코드가 계속 실행되는 것을 막는다.

---

## 4. HTTP 상태 코드 정리

| 상태 코드 | 뜻 | 이 프로젝트의 사용 예시 |
|---|---|---|
| `200 OK` | 요청 성공 | 조회·수정·삭제 성공 |
| `201 Created` | 생성 성공 | 상품 등록 성공 |
| `400 Bad Request` | 잘못된 요청 | 입력 누락, 잘못된 ID, 유효성 검사 실패 |
| `404 Not Found` | 데이터를 찾지 못함 | 해당 ID의 상품이 없음 |
| `500 Internal Server Error` | 서버 내부 오류 | DB 조회·삭제 중 예상하지 못한 오류 |

프런트엔드에서는 `response.ok`로 성공 여부를 확인한다.

```js
if (!response.ok) {
  throw new Error(data.message || "요청 처리에 실패했습니다.")
}
```

---

## 5. 프런트엔드 구조 이해하기

핵심 코드는 `frontend/src/App.jsx`에 있다.

### 5-1. 상태(state) 설계

```js
const [products, setProducts] = useState([])
const [name, setName] = useState("")
const [price, setPrice] = useState("")
const [editingId, setEditingId] = useState(null)
const [loading, setLoading] = useState(false)
const [error, setError] = useState("")
```

| 상태 | 저장하는 값 |
|---|---|
| `products` | 서버에서 받은 상품 배열 |
| `name` | 상품명 입력값 |
| `price` | 가격 입력값 |
| `editingId` | 현재 수정 중인 상품 ID, 수정 중이 아니면 `null` |
| `loading` | 목록을 불러오는 중인지 표시 |
| `error` | 사용자에게 보여줄 오류 메시지 |

상태가 바뀌면 React가 필요한 화면을 다시 렌더링한다.

---

### 5-2. 제어 컴포넌트

입력 요소의 화면 값과 React 상태를 연결하는 방식이다.

```jsx
<input
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

흐름은 다음과 같다.

```text
사용자가 입력
→ onChange 실행
→ setName()으로 상태 변경
→ 변경된 name이 value에 반영
```

React가 입력값의 기준(source of truth)이 된다.

---

### 5-3. 첫 렌더링 시 상품 조회

```js
useEffect(() => {
  fetchProducts()
}, [])
```

빈 의존성 배열 `[]`을 사용하면 컴포넌트가 화면에 처음 나타날 때 상품 목록을 요청한다.

개발 환경에서 `<StrictMode>`를 사용하면 부작용을 점검하기 위해 `useEffect`가 두 번 실행되는 것처럼 보일 수 있다. 배포 빌드에서는 같은 방식으로 중복 실행되지 않는다.

---

### 5-4. `fetch()`로 API 요청하기

#### GET 요청

```js
const response = await fetch(API_URL)
const data = await response.json()
setProducts(data)
```

GET은 기본 메서드라 별도 옵션이 필요 없다.

#### POST 또는 PUT 요청

```js
const response = await fetch(url, {
  method,
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    name: name.trim(),
    price: Number(price)
  })
})
```

- `Content-Type`으로 JSON 데이터임을 알린다.
- `JSON.stringify()`는 JavaScript 객체를 JSON 문자열로 바꾼다.
- 입력 요소의 값은 기본적으로 문자열이므로 가격은 `Number(price)`로 숫자로 변환한다.

#### DELETE 요청

```js
await fetch(`${API_URL}/${id}`, {
  method: "DELETE"
})
```

삭제할 상품의 ID를 URL에 넣어 요청한다.

---

### 5-5. 하나의 폼으로 등록과 수정 처리

`editingId`가 있는지를 기준으로 요청을 바꾼다.

```js
const isEditing = editingId !== null
const url = isEditing ? `${API_URL}/${editingId}` : API_URL
const method = isEditing ? "PUT" : "POST"
```

```text
editingId === null  → 등록 모드 → POST /api/products
editingId !== null  → 수정 모드 → PUT /api/products/:id
```

삼항 연산자의 구조는 다음과 같다.

```js
조건 ? 참일 때 값 : 거짓일 때 값
```

---

### 5-6. 조건부 렌더링

현재 상태에 따라 서로 다른 화면을 보여준다.

```jsx
{loading ? (
  <p>상품 목록을 불러오는 중입니다.</p>
) : products.length === 0 ? (
  <p>등록된 상품이 없습니다.</p>
) : (
  <ul>{/* 상품 목록 */}</ul>
)}
```

판단 순서:

1. 로딩 중이면 로딩 메시지 표시
2. 로딩이 끝났고 배열이 비었으면 빈 목록 메시지 표시
3. 상품이 있으면 목록 표시

`&&`를 사용하면 조건이 참일 때만 요소를 표시할 수 있다.

```jsx
{error && <p>{error}</p>}
{editingId && <button>수정 취소</button>}
```

---

### 5-7. 배열 렌더링과 `key`

```jsx
{products.map((product) => (
  <li key={product._id}>
    {product.name}
  </li>
))}
```

`map()`은 상품 배열을 JSX 배열로 변환한다. `key`는 React가 각각의 항목을 구분하는 고유 식별자다.

- 반복되는 최상위 요소에 지정한다.
- MongoDB의 `_id`처럼 변하지 않는 고유 값을 사용한다.
- 배열 순서가 바뀔 수 있다면 `index`를 `key`로 쓰지 않는 것이 좋다.

---

## 6. 비동기 처리와 오류 처리

서버와 DB 요청은 결과가 바로 나오지 않으므로 `async/await`를 사용한다.

```js
const fetchProducts = async () => {
  try {
    const response = await fetch(API_URL)
  } catch (error) {
    setError(error.message)
  } finally {
    setLoading(false)
  }
}
```

| 구문 | 역할 |
|---|---|
| `async` | 함수 내부에서 `await`를 사용할 수 있게 함 |
| `await` | Promise 작업이 끝날 때까지 기다린 뒤 결과 사용 |
| `try` | 정상적으로 실행할 코드 |
| `catch` | 실행 중 오류가 발생했을 때 처리 |
| `finally` | 성공·실패와 관계없이 마지막에 실행 |

주의할 점:

```js
// 오류: async가 없는데 await를 사용함
router.delete("/:id", (req, res) => {
  const product = await Product.findByIdAndDelete(id)
})

// 올바른 형태
router.delete("/:id", async (req, res) => {
  const product = await Product.findByIdAndDelete(id)
})
```

`SyntaxError: Unexpected reserved word`는 이런 상황에서 발생할 수 있다.

---

## 7. CORS가 필요한 이유

프런트엔드와 백엔드는 포트가 다르므로 브라우저에서 서로 다른 출처(origin)로 판단한다.

```text
프런트엔드: http://localhost:5173
백엔드:     http://127.0.0.1:5001
```

백엔드에서 허용할 출처와 메서드를 설정한다.

```js
cors({
  origin: "http://localhost:5173",
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type"]
})
```

`localhost`와 `127.0.0.1`은 같은 컴퓨터를 가리키지만 브라우저의 origin 문자열은 서로 다르다. 프런트 페이지는 CORS 설정과 동일하게 `http://localhost:5173`으로 여는 것이 안전하다.

---

## 8. 등록부터 화면 갱신까지의 전체 흐름

```text
1. 사용자가 상품명과 가격 입력
2. form의 submit 이벤트 발생
3. e.preventDefault()로 새로고침 방지
4. fetch()가 POST 요청 전송
5. express.json()이 JSON 본문 해석
6. products 라우터가 req.body에서 값 추출
7. Product.create()가 MongoDB에 데이터 저장
8. 서버가 201과 생성된 상품을 응답
9. 프런트엔드가 폼 상태 초기화
10. fetchProducts()로 최신 목록 다시 조회
11. setProducts()로 상태 변경
12. React가 변경된 상품 목록 렌더링
```

수정과 삭제도 핵심 구조는 같다. **사용자 이벤트 → HTTP 요청 → DB 처리 → HTTP 응답 → 상태 변경 → 화면 재렌더링** 흐름을 기억하면 된다.

---

## 9. 현재 코드에서 수정해야 할 부분

아래 내용은 개념 설명이 아니라 현재 프로젝트 파일을 기준으로 확인한 실제 수정 포인트다.

### 9-1. 가격 입력의 속성 오타

현재 `App.jsx`:

```jsx
<input type="nubmer" vlaue={price} />
```

수정:

```jsx
<input type="number" value={price} />
```

- `nubmer` → `number`
- `vlaue` → `value`

이 오타 때문에 숫자 입력 기능과 제어 컴포넌트 연결이 정상 작동하지 않는다.

### 9-2. 수정할 상품 ID 설정 오류

현재 `handleEdit()`:

```js
setEditingId(product.editingId)
```

MongoDB 상품의 ID 필드는 `_id`이므로 다음과 같아야 한다.

```js
setEditingId(product._id)
```

현재 상태에서는 수정 버튼을 눌러도 `editingId`가 올바르게 설정되지 않아 PUT 요청으로 전환되지 않는다.

### 9-3. Mongoose 스키마 옵션 오타

현재 `Product.js`:

```js
requried: [true, "가격은 필수입니다."]
```

수정:

```js
required: [true, "가격은 필수입니다."]
```

오타가 있으면 Mongoose가 해당 옵션을 필수 검사로 인식하지 않는다.

### 9-4. 불필요한 Mongoose named import

현재 `server.js`:

```js
import mongoose, { mongo } from "mongoose"
```

`mongo`를 사용하지 않으므로 다음처럼 정리할 수 있다.

```js
import mongoose from "mongoose"
```

### 9-5. 삭제 버튼 CSS 클래스 미적용

CSS에는 `.delete-button`이 있지만 JSX의 삭제 버튼에는 해당 클래스가 없다.

```jsx
<button
  type="button"
  className="delete-button"
  onClick={() => handleDelete(product._id)}
>
  삭제
</button>
```

---

## 10. 자주 만나는 오류와 해석법

### `The tag <mian> is unrecognized`

HTML 태그 `main`을 `mian`으로 잘못 입력한 경우다.

```jsx
<main>...</main>
```

소문자로 시작하는 JSX 태그는 HTML 태그로 해석되고, 대문자로 시작하면 React 컴포넌트로 해석된다.

### `Each child in a list should have a unique key prop`

`map()`으로 만든 요소에 고유한 `key`가 없다는 경고다.

```jsx
<li key={product._id}>...</li>
```

### `SyntaxError: Unexpected reserved word`

현재 수업 코드에서는 `async`가 없는 함수 안에서 `await`를 사용했을 때 발생했다.

### 403 오류

macOS에서 5000번 포트를 시스템의 `ControlCenter`가 사용하면 Express 서버 대신 그 프로세스에 접속해 403이 나타날 수 있다. 이 프로젝트는 백엔드 포트를 5001로 사용하면 충돌을 피할 수 있다.

### `Failed to fetch` 또는 CORS 오류

다음 항목을 순서대로 확인한다.

1. 백엔드 서버가 실행 중인가?
2. API 포트가 프런트엔드의 `API_URL`과 같은가?
3. MongoDB 연결이 성공했는가?
4. 프런트엔드를 CORS에서 허용한 주소로 열었는가?
5. 요청 URL과 HTTP 메서드가 라우터 정의와 같은가?

---

## 11. 프로젝트 실행 방법

터미널을 두 개 사용한다.

### 터미널 1: 백엔드

```bash
cd backend
npm install
npm run dev
```

확인할 로그:

```text
MongoDB 연결 성공
서버 실행 중...
```

### 터미널 2: 프런트엔드

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 Vite가 알려 준 주소로 접속한다. 현재 CORS 설정 기준 권장 주소는 다음과 같다.

```text
http://localhost:5173
```

---

## 12. 복습용 핵심 질문

아래 질문에 코드 없이 답할 수 있으면 오늘의 핵심 흐름을 이해한 것이다.

- CRUD의 네 가지 기능과 대응하는 HTTP 메서드는 무엇인가?
- `express.json()`은 왜 필요한가?
- `req.body`와 `req.params`의 차이는 무엇인가?
- React에서 `useState`가 바뀌면 화면에는 어떤 일이 생기는가?
- `useEffect(..., [])`는 언제 실행되는가?
- `fetch()`로 객체를 보낼 때 왜 `JSON.stringify()`가 필요한가?
- `response.ok`는 왜 확인해야 하는가?
- `map()`으로 목록을 만들 때 `key`가 필요한 이유는 무엇인가?
- `await`를 사용하는 함수를 왜 `async`로 선언해야 하는가?
- 수정 요청에서 `new: true`, `runValidators: true`는 각각 무엇을 의미하는가?
- `localhost:5173`과 `localhost:5001` 사이에 CORS 설정이 필요한 이유는 무엇인가?

---

## 13. 한 문장으로 최종 정리

> React는 사용자 입력과 화면 상태를 관리하고, `fetch()`로 Express API에 요청하며, Express는 Mongoose를 통해 MongoDB를 조작한 뒤 JSON으로 응답하고, React는 그 결과를 상태에 반영해 화면을 다시 그린다.

