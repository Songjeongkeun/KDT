# [39일차] React - CRUD 프로젝트 정리

## 1. 이번 정리에서 다루는 내용

이번 내용은 React 프론트엔드와 Express 백엔드, MongoDB를 연결해 상품 관리 CRUD 프로젝트를 만드는 흐름을 정리한다.

주요 내용은 다음과 같다.

- CRUD의 의미
- 프론트엔드와 백엔드 역할 분리
- React에서 상품 등록 폼 만들기
- `fetch()`로 API 요청 보내기
- Express 서버 만들기
- CORS 설정
- MongoDB와 Mongoose 연결
- Mongoose Schema와 Model
- REST API 라우터 만들기
- 상품 등록, 조회, 수정, 삭제
- HTTP 상태 코드
- 비동기 처리와 오류 처리
- 현재 코드에서 주의할 오타와 수정 포인트

---

## 2. CRUD란?

CRUD는 데이터를 다루는 가장 기본적인 네 가지 기능을 의미한다.

| 기능 | 의미 | 예시 |
|---|---|---|
| Create | 데이터 생성 | 새 상품 등록 |
| Read | 데이터 조회 | 상품 목록 조회 |
| Update | 데이터 수정 | 상품명, 가격 수정 |
| Delete | 데이터 삭제 | 상품 삭제 |

웹 서비스 대부분은 CRUD 구조를 기반으로 만들어진다. 게시판이라면 글 작성, 글 목록 조회, 글 수정, 글 삭제가 CRUD다. 쇼핑몰 관리자 페이지라면 상품 등록, 상품 조회, 상품 수정, 상품 삭제가 CRUD다.

이번 프로젝트에서는 **상품 관리** 기능을 기준으로 CRUD를 구현한다.

---

## 3. 프로젝트 전체 흐름

이번 프로젝트는 프론트엔드와 백엔드를 분리해서 만든다.

```text
사용자
  ↓ 상품명, 가격 입력
React 프론트엔드
  ↓ fetch()로 HTTP 요청
Express 백엔드
  ↓ Mongoose로 DB 작업
MongoDB
  ↓ 처리 결과 반환
Express 백엔드
  ↓ JSON 응답
React 프론트엔드
  ↓ 상태 변경 후 화면 갱신
사용자 화면
```

각 기술의 역할은 다음과 같다.

| 기술 | 역할 |
|---|---|
| React | 화면을 만들고 입력값, 상품 목록 상태를 관리한다. |
| Vite | React 개발 서버를 실행한다. |
| Fetch API | 프론트엔드에서 백엔드로 HTTP 요청을 보낸다. |
| Express | API 서버를 만들고 요청을 처리한다. |
| MongoDB | 상품 데이터를 저장한다. |
| Mongoose | JavaScript 코드로 MongoDB를 쉽게 다룰 수 있게 해준다. |
| CORS | 다른 포트에서 오는 프론트엔드 요청을 허용한다. |
| dotenv | `.env` 파일의 환경변수를 사용할 수 있게 한다. |

---

## 4. 폴더 구조

프로젝트는 `backend`와 `frontend`로 나뉜다.

```text
8_CRUDProject
├── backend
│   ├── server.js
│   ├── package.json
│   ├── models
│   │   └── Product.js
│   └── routes
│       └── products.js
│
└── frontend
    ├── package.json
    └── src
        ├── App.jsx
        ├── App.css
        ├── main.jsx
        └── index.css
```

백엔드는 데이터베이스와 연결하고 API를 제공한다. 프론트엔드는 사용자가 보는 화면과 입력 상태를 관리한다.

---

## 5. CRUD와 HTTP 메서드

CRUD 기능은 HTTP 메서드와 연결해서 생각하면 이해하기 쉽다.

| CRUD | HTTP 메서드 | API 주소 | 역할 |
|---|---|---|---|
| Create | `POST` | `/api/products` | 새 상품 등록 |
| Read | `GET` | `/api/products` | 전체 상품 조회 |
| Read | `GET` | `/api/products/:id` | 특정 상품 조회 |
| Update | `PUT` | `/api/products/:id` | 특정 상품 수정 |
| Delete | `DELETE` | `/api/products/:id` | 특정 상품 삭제 |

`/:id`는 실제 문자열 `id`가 아니라 MongoDB가 각 데이터에 부여한 `_id` 값이 들어가는 자리다.

```text
/api/products/6690abcdef1234567890abcd
              └──── 상품의 _id ────┘
```

---

## 6. 백엔드 패키지

백엔드에서는 다음 패키지를 사용한다.

```json
{
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.7",
    "express": "^5.1.0",
    "mongoose": "^8.13.2"
  },
  "devDependencies": {
    "nodemon": "^3.1.9"
  }
}
```

각 패키지의 역할은 다음과 같다.

| 패키지 | 역할 |
|---|---|
| `express` | Node.js로 웹 서버와 API를 만들 때 사용한다. |
| `mongoose` | MongoDB 데이터를 JavaScript 객체처럼 다룰 수 있게 해준다. |
| `cors` | 다른 출처에서 오는 요청을 허용한다. |
| `dotenv` | `.env` 파일의 환경변수를 `process.env`로 읽게 해준다. |
| `nodemon` | 서버 코드가 변경되면 자동으로 서버를 재시작한다. |

---

## 7. server.js

`server.js`는 백엔드 서버의 시작점이다.

```js
import express from "express"
import dotenv from "dotenv"
import cors from "cors"
import mongoose from "mongoose"
import productRouter from "./routes/products.js"

dotenv.config()

const app = express()

const PORT = process.env.PORT || 5001
const MONGODB_URI = process.env.MONGODB_URI

app.use(
  cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type"],
  })
)

app.use(express.json())

app.get("/", (req, res) => {
  res.send("Node.js CRUD API 서버가 정상 실행 중입니다.")
})

app.use("/api/products", productRouter)

const startServer = async () => {
  try {
    await mongoose.connect(MONGODB_URI)
    console.log("MongoDB 연결 성공")

    app.listen(PORT, () => {
      console.log("서버 실행 중...")
    })
  } catch (error) {
    console.error("서버 시작 실패: ", error)
    process.exit(1)
  }
}

startServer()
```

---

## 8. dotenv

`dotenv`는 `.env` 파일에 작성한 환경변수를 Node.js 코드에서 사용할 수 있게 해준다.

```js
import dotenv from "dotenv"

dotenv.config()
```

이후 다음처럼 값을 꺼낼 수 있다.

```js
const PORT = process.env.PORT || 5001
const MONGODB_URI = process.env.MONGODB_URI
```

데이터베이스 주소처럼 외부에 공개하면 안 되는 값은 코드에 직접 쓰지 않고 `.env`에 보관하는 것이 좋다.

```text
MONGODB_URI=mongodb://127.0.0.1:27017/crud_project
PORT=5001
```

`.env` 파일은 보통 Git에 올리지 않는다.

---

## 9. express.json()

프론트엔드에서 JSON 데이터를 보내면 서버는 요청 본문을 읽어야 한다.

```json
{
  "name": "키보드",
  "price": 50000
}
```

Express에서 JSON 요청 본문을 읽으려면 다음 미들웨어가 필요하다.

```js
app.use(express.json())
```

이 코드가 있어야 라우터에서 `req.body`를 사용할 수 있다.

```js
const { name, price } = req.body
```

만약 `express.json()`을 등록하지 않으면 `req.body`가 비어 있거나 예상대로 읽히지 않을 수 있다.

---

## 10. CORS

CORS는 서로 다른 출처에서 요청할 때 브라우저가 적용하는 보안 정책이다.

이번 프로젝트에서는 프론트엔드와 백엔드 주소가 다르다.

```text
React 프론트엔드: http://localhost:5173
Express 백엔드:  http://127.0.0.1:5001
```

포트가 다르기 때문에 브라우저는 다른 출처로 판단한다. 그래서 백엔드에서 프론트엔드 요청을 허용해야 한다.

```js
app.use(
  cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type"],
  })
)
```

각 옵션의 의미는 다음과 같다.

| 옵션 | 의미 |
|---|---|
| `origin` | 요청을 허용할 프론트엔드 주소다. |
| `methods` | 허용할 HTTP 메서드 목록이다. |
| `allowedHeaders` | 허용할 요청 헤더 목록이다. |

---

## 11. 라우터 연결

`server.js`에서는 상품 관련 API를 별도 라우터로 분리한다.

```js
import productRouter from "./routes/products.js"

app.use("/api/products", productRouter)
```

이 코드는 `products.js` 안에 작성된 라우터 앞에 `/api/products`를 붙인다는 의미다.

```text
router.get("/")       -> GET /api/products
router.post("/")      -> POST /api/products
router.get("/:id")    -> GET /api/products/:id
router.put("/:id")    -> PUT /api/products/:id
router.delete("/:id") -> DELETE /api/products/:id
```

라우터를 분리하면 `server.js`가 복잡해지는 것을 막고, 기능별로 파일을 관리할 수 있다.

---

## 12. Mongoose Schema

Mongoose Schema는 MongoDB에 저장할 데이터의 형태와 규칙을 정의한다.

```js
import mongoose from "mongoose"

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "상품명은 필수입니다."],
      trim: true,
    },
    price: {
      type: Number,
      required: [true, "가격은 필수입니다."],
      min: [0, "가격은 0원 이상이어야 합니다."],
    },
  },
  {
    timestamps: true,
  }
)

const Product = mongoose.model("Product", productSchema)

export default Product
```

각 옵션의 의미는 다음과 같다.

| 옵션 | 의미 |
|---|---|
| `type` | 저장할 값의 자료형이다. |
| `required` | 반드시 입력되어야 하는 값인지 검사한다. |
| `trim` | 문자열 앞뒤 공백을 제거한다. |
| `min` | 숫자의 최소값을 제한한다. |
| `timestamps` | `createdAt`, `updatedAt`을 자동으로 만든다. |

---

## 13. Mongoose Model

Schema가 데이터의 규칙이라면 Model은 실제로 MongoDB에 접근하는 도구다.

```js
const Product = mongoose.model("Product", productSchema)
```

이후 다음과 같은 메서드를 사용할 수 있다.

| 메서드 | 역할 |
|---|---|
| `Product.find()` | 상품 전체를 조회한다. |
| `Product.findById(id)` | 특정 id의 상품을 조회한다. |
| `Product.create(data)` | 새 상품을 생성한다. |
| `Product.findByIdAndUpdate(id, data, options)` | 특정 상품을 수정한다. |
| `Product.findByIdAndDelete(id)` | 특정 상품을 삭제한다. |

---

## 14. 상품 전체 조회 API

상품 전체 조회는 `GET /api/products` 요청으로 처리한다.

```js
router.get("/", async (req, res) => {
  try {
    const products = await Product.find().sort({ createdAt: -1 })
    res.status(200).json(products)
  } catch (error) {
    console.error("상품 조회 오류: ", error)
    res.status(500).json({
      message: "상품 목록을 불러오지 못했습니다.",
    })
  }
})
```

### 코드 흐름

1. 클라이언트가 `GET /api/products`로 요청한다.
2. `Product.find()`로 전체 상품을 조회한다.
3. `sort({ createdAt: -1 })`로 최신 상품이 먼저 오도록 정렬한다.
4. 성공하면 `200` 상태 코드와 상품 배열을 JSON으로 응답한다.
5. 실패하면 `500` 상태 코드와 오류 메시지를 응답한다.

---

## 15. 특정 상품 조회 API

특정 상품 조회는 `GET /api/products/:id` 요청으로 처리한다.

```js
router.get("/:id", async (req, res) => {
  try {
    const { id } = req.params

    if (!mongoose.isValidObjectId(id)) {
      return res.status(400).json({
        message: "올바르지 않은 상품 ID입니다.",
      })
    }

    const product = await Product.findById(id)

    if (!product) {
      return res.status(404).json({
        message: "상품을 찾을 수 없습니다.",
      })
    }

    res.status(200).json(product)
  } catch (error) {
    console.error("상품 상세 조회 오류: ", error)
    res.status(500).json({
      message: "상품 정보를 불러오지 못했습니다.",
    })
  }
})
```

`req.params`는 URL 경로에 포함된 값을 읽을 때 사용한다.

```text
GET /api/products/123
                  └─ req.params.id
```

---

## 16. MongoDB ObjectId 검사

MongoDB의 `_id`는 정해진 형식이 있다. 잘못된 형식의 id를 `findById()`에 전달하면 오류가 발생할 수 있다.

그래서 DB 작업 전에 id 형식을 먼저 검사한다.

```js
if (!mongoose.isValidObjectId(id)) {
  return res.status(400).json({
    message: "올바르지 않은 상품 ID입니다.",
  })
}
```

여기서 `return`을 사용하는 이유는 응답을 보낸 뒤 아래 코드가 계속 실행되는 것을 막기 위해서다.

```js
return res.status(400).json(...)
```

`return`이 없으면 에러 응답을 보낸 뒤에도 `Product.findById(id)`가 실행될 수 있다.

---

## 17. 상품 등록 API

상품 등록은 `POST /api/products` 요청으로 처리한다.

```js
router.post("/", async (req, res) => {
  try {
    const { name, price } = req.body

    if (!name || price === undefined) {
      return res.status(400).json({
        message: "상품명과 가격을 입력해 주세요.",
      })
    }

    const product = await Product.create({
      name,
      price,
    })

    res.status(201).json(product)
  } catch (error) {
    console.error("상품 등록 오류: ", error)
    res.status(400).json({
      message: "상품을 등록하지 못했습니다.",
      error: error.message,
    })
  }
})
```

### 코드 흐름

1. 클라이언트가 상품명과 가격을 JSON으로 보낸다.
2. 서버가 `req.body`에서 `name`, `price`를 꺼낸다.
3. 값이 없으면 `400 Bad Request`로 응답한다.
4. 값이 있으면 `Product.create()`로 MongoDB에 저장한다.
5. 생성에 성공하면 `201 Created`로 응답한다.

---

## 18. 상품 수정 API

상품 수정은 `PUT /api/products/:id` 요청으로 처리한다.

```js
router.put("/:id", async (req, res) => {
  try {
    const { id } = req.params
    const { name, price } = req.body

    if (!mongoose.isValidObjectId(id)) {
      return res.status(400).json({
        message: "올바르지 않은 상품 ID입니다.",
      })
    }

    if (!name || price === undefined) {
      return res.status(400).json({
        message: "상품명과 가격을 입력해 주세요.",
      })
    }

    const updatedProduct = await Product.findByIdAndUpdate(
      id,
      { name, price },
      { new: true, runValidators: true }
    )

    if (!updatedProduct) {
      return res.status(404).json({
        message: "수정할 상품을 찾을 수 없습니다.",
      })
    }

    return res.status(200).json(updatedProduct)
  } catch (error) {
    console.error("상품 수정 오류: ", error)
    res.status(400).json({
      message: "상품을 수정하지 못했습니다.",
      error: error.message,
    })
  }
})
```

수정할 때 중요한 옵션은 다음과 같다.

| 옵션 | 의미 |
|---|---|
| `new: true` | 수정 전 데이터가 아니라 수정된 최신 데이터를 반환한다. |
| `runValidators: true` | 수정할 때도 Schema의 유효성 검사를 실행한다. |

`runValidators: true`가 없으면 `min`, `required` 같은 Schema 검사가 수정 시 제대로 적용되지 않을 수 있다.

---

## 19. 상품 삭제 API

상품 삭제는 `DELETE /api/products/:id` 요청으로 처리한다.

```js
router.delete("/:id", async (req, res) => {
  try {
    const { id } = req.params

    if (!mongoose.isValidObjectId(id)) {
      return res.status(400).json({
        message: "올바르지 않은 상품 ID입니다.",
      })
    }

    const deletedProduct = await Product.findByIdAndDelete(id)

    if (!deletedProduct) {
      return res.status(404).json({
        message: "삭제할 상품을 찾을 수 없습니다.",
      })
    }

    res.status(200).json({
      message: "상품이 삭제되었습니다.",
      product: deletedProduct,
    })
  } catch (error) {
    console.error("상품 삭제 오류: ", error)
    res.status(500).json({
      message: "상품을 삭제하지 못했습니다.",
    })
  }
})
```

삭제 성공 시에는 삭제된 상품 정보를 함께 응답할 수 있다.

```js
res.status(200).json({
  message: "상품이 삭제되었습니다.",
  product: deletedProduct,
})
```

---

## 20. HTTP 상태 코드

API 응답에는 상태 코드를 함께 사용한다.

| 상태 코드 | 의미 | 사용 예시 |
|---|---|---|
| `200 OK` | 요청 성공 | 조회, 수정, 삭제 성공 |
| `201 Created` | 생성 성공 | 상품 등록 성공 |
| `400 Bad Request` | 잘못된 요청 | 입력값 누락, 잘못된 ID |
| `404 Not Found` | 데이터를 찾지 못함 | 해당 id의 상품 없음 |
| `500 Internal Server Error` | 서버 내부 오류 | DB 연결 또는 서버 오류 |

프론트엔드에서는 `response.ok`로 성공 여부를 확인할 수 있다.

```js
if (!response.ok) {
  throw new Error(data.message || "요청 처리에 실패했습니다.")
}
```

---

## 21. 프론트엔드 상태 설계

프론트엔드의 핵심 코드는 `frontend/src/App.jsx`에 있다.

```jsx
const API_URL = "http://127.0.0.1:5001/api/products"

export default function App() {
  const [products, setProducts] = useState([])
  const [name, setName] = useState("")
  const [price, setPrice] = useState("")
  const [editingId, setEditingId] = useState(null)
  const [loading, setLoading] = useState(null)
  const [error, setError] = useState("")
}
```

각 상태의 역할은 다음과 같다.

| 상태 | 의미 |
|---|---|
| `products` | 서버에서 받아온 상품 목록 배열이다. |
| `name` | 상품명 입력값이다. |
| `price` | 가격 입력값이다. |
| `editingId` | 현재 수정 중인 상품의 id다. 수정 중이 아니면 `null`이다. |
| `loading` | 상품 목록을 불러오는 중인지 표시한다. |
| `error` | 사용자에게 보여줄 오류 메시지다. |

---

## 22. 제어 컴포넌트

React에서 입력값을 상태로 관리하는 방식을 제어 컴포넌트라고 한다.

```jsx
<input
  id="name"
  type="text"
  placeholder="상품명을 입력하세요."
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

입력 흐름은 다음과 같다.

```text
사용자가 입력
        ↓
onChange 이벤트 발생
        ↓
setName(e.target.value) 실행
        ↓
name 상태 변경
        ↓
value={name}에 반영
```

가격 입력도 같은 방식으로 관리한다.

```jsx
<input
  id="price"
  type="number"
  min="0"
  placeholder="가격을 입력하세요."
  value={price}
  onChange={(e) => setPrice(e.target.value)}
/>
```

input에서 들어오는 값은 기본적으로 문자열이다. 그래서 서버에 보낼 때 숫자로 변환한다.

```js
price: Number(price)
```

---

## 23. 첫 렌더링 시 상품 목록 가져오기

상품 목록은 컴포넌트가 처음 화면에 나타날 때 서버에서 가져온다.

```jsx
useEffect(() => {
  fetchProducts()
}, [])
```

빈 의존성 배열 `[]`을 사용하면 첫 렌더링 이후 한 번 실행된다.

목록을 가져오는 함수는 다음과 같다.

```jsx
const fetchProducts = async () => {
  try {
    setLoading(true)
    setError("")

    const response = await fetch(API_URL)

    if (!response.ok) {
      throw new Error("상품 목록을 불러오지 못했습니다.")
    }

    const data = await response.json()
    setProducts(data)
  } catch (error) {
    console.error(error)
    setError(error.message)
  } finally {
    setLoading(false)
  }
}
```

### 코드 흐름

1. 로딩 상태를 `true`로 바꾼다.
2. 기존 에러 메시지를 비운다.
3. `fetch(API_URL)`로 백엔드에 GET 요청을 보낸다.
4. 응답이 실패라면 에러를 발생시킨다.
5. 성공하면 `response.json()`으로 JSON 데이터를 JavaScript 값으로 바꾼다.
6. `setProducts(data)`로 상품 목록 상태를 업데이트한다.
7. 성공·실패와 관계없이 마지막에 로딩 상태를 `false`로 바꾼다.

---

## 24. async / await / try / catch / finally

서버 요청은 시간이 걸리는 비동기 작업이다. 그래서 `async/await`를 사용한다.

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

각 구문의 역할은 다음과 같다.

| 구문 | 역할 |
|---|---|
| `async` | 함수 안에서 `await`를 사용할 수 있게 한다. |
| `await` | Promise가 끝날 때까지 기다린다. |
| `try` | 성공할 가능성이 있는 코드를 작성한다. |
| `catch` | 오류가 발생했을 때 실행된다. |
| `finally` | 성공·실패와 관계없이 마지막에 실행된다. |

예를 들어 로딩 상태는 성공해도 꺼야 하고, 실패해도 꺼야 한다. 이런 코드는 `finally`에 두면 좋다.

```js
finally {
  setLoading(false)
}
```

---

## 25. 상품 등록과 수정 처리

상품 등록과 수정은 하나의 form에서 처리한다.

```jsx
const handleSubmit = async (e) => {
  e.preventDefault()

  if (!name.trim() || price === "") {
    alert("상품명과 가격을 입력해주세요.")
    return
  }

  try {
    setError("")

    const isEditing = editingId !== null
    const url = isEditing ? `${API_URL}/${editingId}` : API_URL
    const method = isEditing ? "PUT" : "POST"

    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name.trim(),
        price: Number(price),
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "요청 처리에 실패했습니다.")
    }

    resetForm()
    await fetchProducts()
  } catch (error) {
    console.error(error)
    setError(error.message)
  }
}
```

---

## 26. 하나의 폼으로 POST와 PUT 나누기

`editingId`가 있는지를 기준으로 등록인지 수정인지 판단한다.

```js
const isEditing = editingId !== null
const url = isEditing ? `${API_URL}/${editingId}` : API_URL
const method = isEditing ? "PUT" : "POST"
```

흐름은 다음과 같다.

```text
editingId === null
        ↓
등록 모드
        ↓
POST /api/products
```

```text
editingId !== null
        ↓
수정 모드
        ↓
PUT /api/products/:id
```

삼항 연산자는 조건에 따라 값을 선택할 때 사용한다.

```js
조건 ? 참일_때_값 : 거짓일_때_값
```

---

## 27. JSON 요청 보내기

프론트엔드에서 서버로 객체를 보낼 때는 JSON 문자열로 변환해야 한다.

```js
body: JSON.stringify({
  name: name.trim(),
  price: Number(price),
})
```

그리고 요청 헤더에 JSON 형식임을 알려준다.

```js
headers: {
  "Content-Type": "application/json",
}
```

서버는 `express.json()`을 통해 이 JSON 본문을 해석하고 `req.body`로 사용할 수 있다.

```js
const { name, price } = req.body
```

---

## 28. 폼 초기화

등록이나 수정이 끝나면 입력 폼을 초기화한다.

```js
const resetForm = () => {
  setName("")
  setPrice("")
  setEditingId(null)
}
```

각 상태를 초기값으로 되돌린다.

| 상태 | 초기화 값 |
|---|---|
| `name` | `""` |
| `price` | `""` |
| `editingId` | `null` |

`editingId`가 `null`이 되면 다시 등록 모드가 된다.

---

## 29. 수정 모드로 전환하기

상품 목록에서 수정 버튼을 누르면 기존 상품 정보를 입력창에 넣고 수정 모드로 전환한다.

```jsx
const handleEdit = (product) => {
  setName(product.name)
  setPrice(product.price)
  setEditingId(product._id)
}
```

### 코드 흐름

1. 사용자가 특정 상품의 수정 버튼을 클릭한다.
2. 해당 상품 객체가 `handleEdit(product)`로 전달된다.
3. 상품명이 `name` 상태에 들어간다.
4. 가격이 `price` 상태에 들어간다.
5. 상품의 `_id`가 `editingId`에 들어간다.
6. 버튼 문구가 `"상품 등록"`에서 `"수정 완료"`로 바뀐다.
7. form 제출 시 `POST`가 아니라 `PUT` 요청을 보낸다.

---

## 30. 상품 삭제하기

삭제는 사용자의 실수를 막기 위해 먼저 확인 창을 띄운다.

```jsx
const handleDelete = async (id) => {
  const isConfirmed = window.confirm("상품을 삭제하시겠습니까?")

  if (!isConfirmed) {
    return
  }

  try {
    setError("")

    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "상품 삭제에 실패했습니다.")
    }

    if (editingId === id) {
      resetForm()
    }

    await fetchProducts()
  } catch (error) {
    console.error(error)
    setError(error.message)
  }
}
```

### 코드 흐름

1. 삭제 버튼을 클릭한다.
2. `window.confirm()`으로 삭제 여부를 확인한다.
3. 취소하면 함수가 종료된다.
4. 확인하면 `DELETE /api/products/:id` 요청을 보낸다.
5. 서버에서 상품을 삭제한다.
6. 삭제 성공 후 최신 상품 목록을 다시 가져온다.
7. 삭제 중이던 상품이 수정 모드였다면 폼을 초기화한다.

---

## 31. 조건부 렌더링

상태에 따라 서로 다른 화면을 보여줄 수 있다.

```jsx
{error && <p className="error-message">{error}</p>}
```

`error`가 빈 문자열이면 아무것도 표시하지 않는다. `error`에 메시지가 있으면 에러 문구를 표시한다.

목록 영역은 로딩 상태와 데이터 유무에 따라 다르게 렌더링한다.

```jsx
{loading ? (
  <p>상품 목록을 불러오는 중입니다.</p>
) : products.length === 0 ? (
  <p>등록된 상품이 없습니다.</p>
) : (
  <ul className="product-list">
    {products.map((product) => (
      <li key={product._id}>
        <div>
          <strong>{product.name}</strong>
          <span>{product.price.toLocaleString()}원</span>
        </div>
      </li>
    ))}
  </ul>
)}
```

판단 순서는 다음과 같다.

```text
loading이 true인가?
        ↓
맞으면 로딩 메시지

아니면 products 배열이 비었는가?
        ↓
맞으면 빈 목록 메시지

아니면 상품 목록 출력
```

---

## 32. 배열 렌더링과 key

상품 목록은 `map()`으로 렌더링한다.

```jsx
{products.map((product) => (
  <li key={product._id}>
    <div>
      <strong>{product.name}</strong>
      <span>{product.price.toLocaleString()}원</span>
    </div>
    <div className="button-group">
      <button type="button" onClick={() => handleEdit(product)}>
        수정
      </button>
      <button type="button" onClick={() => handleDelete(product._id)}>
        삭제
      </button>
    </div>
  </li>
))}
```

`key`는 React가 각 목록 항목을 구분하기 위한 값이다.

```jsx
key={product._id}
```

MongoDB의 `_id`는 데이터마다 고유하므로 key로 사용하기 좋다.

가격은 `toLocaleString()`을 사용해 쉼표가 포함된 형태로 보여줄 수 있다.

```js
product.price.toLocaleString()
```

예시는 다음과 같다.

```text
50000      -> 50,000
1200000    -> 1,200,000
```

---

## 33. 등록부터 화면 갱신까지 전체 흐름

상품 등록 흐름은 다음과 같다.

```text
1. 사용자가 상품명과 가격을 입력한다.
2. form 제출 이벤트가 발생한다.
3. e.preventDefault()로 새로고침을 막는다.
4. 입력값이 비어 있는지 검사한다.
5. fetch()로 POST /api/products 요청을 보낸다.
6. Express의 express.json()이 JSON 본문을 해석한다.
7. products 라우터가 req.body에서 name, price를 꺼낸다.
8. Product.create()가 MongoDB에 상품을 저장한다.
9. 서버가 201 상태 코드와 생성된 상품을 JSON으로 응답한다.
10. 프론트엔드가 폼을 초기화한다.
11. fetchProducts()로 최신 상품 목록을 다시 조회한다.
12. setProducts()로 상태를 변경한다.
13. React가 상품 목록 화면을 다시 렌더링한다.
```

수정과 삭제도 큰 흐름은 비슷하다.

```text
사용자 이벤트
        ↓
fetch() 요청
        ↓
Express 라우터 처리
        ↓
Mongoose로 MongoDB 작업
        ↓
JSON 응답
        ↓
React 상태 변경
        ↓
화면 갱신
```

---

## 34. 실행 방법

터미널을 두 개 열어 백엔드와 프론트엔드를 각각 실행한다.

### 백엔드 실행

```bash
cd backend
npm install
npm run dev
```

정상 실행되면 다음과 같은 로그를 확인할 수 있다.

```text
MongoDB 연결 성공
서버 실행 중...
```

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 Vite가 알려주는 주소로 접속한다.

```text
http://localhost:5173
```



## 35. 한 문장으로 정리

React는 사용자 입력과 화면 상태를 관리하고, `fetch()`로 Express API에 요청을 보낸다. Express는 요청을 받아 Mongoose로 MongoDB를 조작하고, 처리 결과를 JSON으로 응답한다. React는 응답 결과를 상태에 반영해 화면을 다시 그린다.

