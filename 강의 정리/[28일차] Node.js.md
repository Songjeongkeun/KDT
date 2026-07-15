# [28일차] Node.js

Express는 Node.js에서 웹 서버를 더 쉽고 구조적으로 만들 수 있게 해주는 프레임워크이다.

기본 `http` 모듈만 사용하면 요청 주소와 메서드를 직접 비교해야 하지만, Express를 사용하면 `app.get()`, `app.post()`, `Router`같은 기능으로 서버 코드를 훨씬 깔끔하게 작성할 수 있다.



## 1. 게시물 작성 기능의 전체 흐름

게시물 작성 기능은 사용자가 브라우저에서 글을 작성하면, 서버가 그 데이터를 받아 파일에 저장하고, 저장된 게시물 목록 페이지로 이동시키는 구조이다.

```tex
사용자
  ↓
GET /
  ↓
게시물 작성 화면 렌더링
  ↓
제목, 내용 입력 후 저장 버튼 클릭
  ↓
POST /posts
  ↓
서버가 form 데이터를 받음
  ↓
post.txt 파일에 저장
  ↓
GET /posts로 이동
  ↓
저장된 게시물 목록 출력
```



## 2. 서버 코드

```js
const express = require("express")
const fs = require("fs")
const path = requrie("path")

const app = express()
const PORT = 3000 

app.set = express()
app.set("views", path.join(__dirname, "view"))

app.use(express.urlencoded({ extended: true }))

const filePath = path.join(__dirname, "data", "post.txt")

// 게시물 작성 화면
app.get("/", (req, res) => {
  res.render("write")
})

// 게시물 저장
app.post("/posts", (req, res) => {
  const { title, content } = req.body
  
  const saveText = `
  =============================
  제목: ${title}
  내용: ${content}
  작성일: ${new Date().toLocalString()}
  =============================
  `
  
  fs.appendFile(filePath, saveText, "utf8", (err) => {
    if(err){
      console.error(err)
      return res.send("파일 저장 중 오류가 발생함")
    }
    res.redirect("/posts")
  })
})

// 게시물 리스트
app.get("/posts", (req, res) => {
  fs.readFile(filePath, "utf8", (err, data) => {
    if(err){
      console.error(err)
      return res.render("posts", { posts: "아직 저장된 게시물이 없습니다."})
    }
    res.render("posts", { posts: data })
  })
})

app.listen(3000, () => {
  console.log("서버 실행 중...")
})
```



## 3. 코드 설명

**express 불러오기**

```js
const express = require("express")
const app = express()
```

`express` 모듈을 불러오고, Express 애플리케이션 객체를 만든다.

이 `app` 객체를 이용해 라우팅, 미들웨어 등록, 서버 실행을 처리한다.

---------------

**fs 와 path 불러오기**

```js
const fs = require("fs")
const path = require("path")
```

`fs`는 파일을 읽고 쓰기 위한 Node.js 내장 모듈이다.

`path`는 운영체제에 맞게 파일 경로를 안전하게 만들기 위한 내장 모듈이다.

```js
const filePath = path.join(__dirname, "data", "post.txt")
```

현재 파일이 있는 폴더를 기준으로 `data/post.txt` 경로를 만든다.

`path.join()`을 사용하면 macOS, Windows 같은 운영체제 차이에 더 안전하다.

---------------

**EJS 설정**

```js
app.set("view engine", "ejs")
app.set("views", path.join(_dirname, "view"))
```

Express에서 EJS 템플릿 엔진을 사용하겠다고 설정한다.

| 설정          | 의미                      |
| ------------- | ------------------------- |
| `view engine` | 사용할 템플릿 엔진        |
| `views`       | EJS 파일이 들어 있는 폴더 |

즉, `res.render("write")` 를 호출하면 Express는 `view/write.ejs` 파일을 찾아 HTML로 변환해 응답한다.

---------------

## 4. form 데이터 처리 미들웨어

```js
app.use(express.urlencoded({ extended: true }))
```

HTML form에 전송된 데이터를 `req.body` 로 읽을 수 있게 해주는 미들웨어이다.

게시물 작성 폼은 다음처럼 `method="post"` 방식으로 데이터를 전송한다.

```html
<form action="/posts" method="post">
  <p>제목: <input type="text" name="title"></p>
  <p>내용<br>
    <textarea name="content"></textarea>
  </p>
  <p><button type="submit">저장</button></p>
</form>
```

>| HTML name        | 서버에서 접근하는 방법 |
>| ---------------- | ---------------------- |
>| `name="title"`   | `req.body.title`       |
>| `name="content"` | `req.body.content`     |

서버에서는 구조 분해 할당으로 값을 꺼낸다.

```js
const { title, contetn } = req.body
```

-----------

## 5. 게시물 작성 화면

`GET /` 요청이 들어오면 게시물 작성 화면을 보여준다.

```js
app.get("/", (req, res) => {
  res.render("write")
})
```

`write.ejs` 는 게시물 제목과 내용을 입력하는 폼이다. 

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>게시물 작성</title>
  <style>
    textarea {
      width: 300px;
      height: 30px;
      font-size: 18px;
      resize: none;
    }
  </style>
</head>
<body>
  <h1>게시물 작성</h1>
  <form action="/posts" method="post">
    <p>제목: <input type="text" name="title"></p>
    <p>내용<br>
      <textarea name="content"></textarea>
    </p>
    <p><button type="submit">저장</button></p>
  </form>
</body>
</html>
```

사용자가 저장 버튼을 누르면 `/posts` 주소로 POST 요청이 전송된다.

------------

## 6. 게시물 저장

```js
app.post("/posts", (req, res) => {
  const { title, content } = req.body
  
  const saveText = `
  =============================
  제목: ${title}
  내용: ${content}
  작성일: ${new Date().toLocalString()}
  =============================
  `
  
  fs.appendFile(filePath, saveText, "utf8", (err, data) => {
    if (err) {
      console.error(err)
      return res.send("파일 저장 중 오류가 발생함")
    }
    
    res.redirect("/posts")
  })
})
```

**`fs.appendFile()`**은 파일의 기존 내용을 지우지 않고, 뒤에 새로운 내용을 추가한다.

```
fs.appendFile(filePath, saveText, "utf8", callback)
```

| 인자       | 의미                       |
| ---------- | -------------------------- |
| `filePath` | 저장할 파일 경로           |
| `saveText` | 파일에 추가할 내용         |
| `"utf8"`   | 문자 인코딩 방식           |
| `callback` | 저장 완료 후 실행되는 함수 |

게시물을 여러 번 작성하면 `post.txt` 파일에 글이 계속 누적된다.

### `return res.send()`를 사용하는 이유

```Js
if (err) {
  console.error(err)
  return res.send("파일 저장 중 오류가 발생함")
}
```

오류가 발생했을 때 `res.send()`로 응답을 보낸 뒤 `return`으로 함수 실행을 끝낸다.
`return`이 없으면 아래의 `res.redirect("/posts")`까지 실행될 수 있고, 하나의 요청에 응답을 두 번 보내는 문제가 생길 수 있다.

### `res.redirect()`

```
res.redirect("/posts")
```

`redirect`는 클라이언트를 다른 주소로 이동시키는 응답이다.
게시물 저장이 끝난 뒤 자동으로 `/posts` 페이지로 이동하게 만든다.

```tex
POST /posts
  ↓
파일 저장
  ↓
res.redirect("/posts")
  ↓
GET /posts 요청 발생
  ↓
게시물 리스트 출력
```

--------------

## 7. 게시물 목록 출력

```js
app.get("/posts", (req, res) => {
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error(err)
      return res.render("posts", { posts: "아직 저장된 게시물이 없습니다." })
    }

    res.render("posts", { posts: data })
  })
})
```

`fs.readFile()`로 `post.txt` 파일을 읽고, 읽은 내용을 `posts.ejs`로 전달한다.

```js
res.render("posts", { posts: data })
```

`posts.ejs`는 다음과 같이 전달받은 `posts` 값을 출력한다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>게시물 리스트</title>
</head>
<body>
  <h1>저장된 게시물 리스트</h1>
  <p><a href="/">게시물 작성</a></p>
  <pre><%= posts %></pre>
</body>
</html>
```

### `<pre>` 태그

`<pre>` 태그는 줄바꿈과 공백을 입력된 그대로 보여준다. 게시물 내용을 파일에 저장할 때 줄바꿈을 포함했기 때문에, `<pre>`를 사용하면 저장된 모양 그대로 출력할 수 있다.

------------

## 8. JSON 요청 처리

HTML form 이 아닌 JSON 데이터를 서버로 보내는 경우에는 다른 미들웨어가 필요하다.

```js
app.use(express.json())
```

`express.json()` 은 요청 본문에 담긴 JSON 문자열을 JavaScript 객체로 변환해 `req.body` 에 넣어준다.

```tex
클라이언트 JSON 요청
  ↓
express.json()
  ↓
req.body로 접근
  ↓
서버 로직 처리
  ↓
res.json()으로 JSON 응답
```

-----------

## 9. JSON API 예제

```js
const express = require("express")
const app = express()

app.use(express.json())

app.post("/user", (req, res) => {
  const { name, age } = req.body
  
  if(!name || !age ){
    return res.status(400).json({ error: "필수값 누락!" })
  }
  
  res.status(201).json({
    message: "등록 완료",
    data: { name, age },
  })
})

app.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

**요청 예시**

브라우저 주소창은 보통 GET 요청만 보내기 때문에, JSON PORT 요청은 Postman 도구를 사용하면 볼 수 있다. 

**응답 예시 (Postman 사용)**

```js
{
  "message": "등록 완료",
  "data": {
    "name": "김사과",
    "age": 20
  }
}
```

## 10. form 데이터와 JSON 데이터 비교

| 구분            | form 요청                           | JSON 요청                 |
| --------------- | ----------------------------------- | ------------------------- |
| 주 사용 위치    | HTML form                           | API 서버, 프론트엔드 통신 |
| Content-Type    | `application/x-www-form-urlencoded` | `application/json`        |
| 필요한 미들웨어 | `express.urlencoded()`              | `express.json()`          |
| 서버 접근 방식  | `req.body`                          | `req.body`                |

둘 다 최종적으로는 `req.body`에서 데이터를 읽는다.
하지만 요청 데이터 형식이 다르기 때문에 사용하는 미들웨어가 다르다.

-------------

## 11. 유효성 검사

서버는 클라이언트가 항상 올바른 데이터를 보낸다고 믿으면 안된다.

필수 데이터가 없으면 요청을 거절하고 오류 응답을 보내야 한다.

```js
app.post("/user", (req, res) => {
  const { name, age } = req.body
  
  if(!name || !age){
    return res.status(400).json({
      error: "name 또는 age 필수",
    })
  }
  
  res.status(201).json({
    message: "등록 완료",
    data: { name, age }
  })
})
```

------------

## 12. CRUD와 HTTP 메서드

API는 보통 자원(Resource)을 기준으로 설계한다.

사용자 데이터를 다룬다면 `/user`, 게시물 데이터를 다룬다면 `/posts` 같은 주소를 사용한다.

| 기능      | HTTP 메서드 | 예시 주소 | 의미                 |
| --------- | ----------- | --------- | -------------------- |
| 조회      | `GET`       | `/user/1` | 1번 사용자 조회      |
| 생성      | `POST`      | `/user`   | 사용자 생성          |
| 전체 수정 | `PUT`       | `/user/1` | 1번 사용자 전체 수정 |
| 부분 수정 | `PATCH`     | `/user/1` | 1번 사용자 일부 수정 |
| 삭제      | `DELETE`    | `/user/1` | 1번 사용자 삭제      |

------------

## 13. 사용자 API 예제

```js
// 조회
app.get("user/:id", (req, res) => {
  res.json({ id: req.params.id, message: "사용자 조회" })
})

// 전체 수정
app.put("/user/:id", (req, res) => {
  const { name, age } = req.body

  if (!name || !age) {
    return res.status(400).json({ error: "필수값 누락!" })
  }

  res.json({
    message: "전체 수정 완료",
    id: req.params.id,
    data: { name, age },
  })
})

// 부분 수정
app.patch("/user/:id", (req, res) => {
  const updates = req.body

  if (Object.keys(updates).length === 0) {
    return res.status(400).json({ error: "수정할 데이터가 없습니다." })
  }

  res.json({
    message: "부분 수정 완료",
    id: req.params.id,
    updateData: updates,
  })
})

// 삭제
app.delete("/user/:id", (req, res) => {
  res.json({ message: "삭제 완료", id: req.params.id })
})
```

**`req.params`**

```js
app.get("/user/:id", (req, res) => {
  console.log(req.params.id)
})
```

`/user/3`으로 요청하면 `req.params.id` 값은 `"3"`이 된다.

```tex
/user/:id
       ↑
   동적으로 바뀌는 값
```

-----------------

## 14. RESTful API 설계

RESTful API는 URL과 HTTP 메서드를 이용해 자원을 직관적으로 표현하는 API 설계 방식이다.

일반적으로 다음 구조를 많이 사용한다.

```tex
/api/버전/리소스
```

예시는 다음과 같다.

```tex
/api/v1/users
/api/v1/posts
/api/v1/products
```

| 요소    | 의미              |
| ------- | ----------------- |
| `api`   | API 요청임을 표시 |
| `v1`    | API 버전          |
| `users` | 사용자 자원       |
| `posts` | 게시물 자원       |

RESTful API에서는 URL에는 명사를 쓰고, 동작은 HTTP 메서드로 표현하는 것이 일반적이다.

```
좋은 예
GET /posts
POST /posts
PUT /posts/1
DELETE /posts/1

아쉬운 예
GET /getPosts
POST /createPost
GET /deletePost
```

## 15. HTTP 상태 코드

상태 코드는 서버가 요청을 어떻게 처리했는지 알려주는 번호다.

| 범위  | 의미                 |
| ----- | -------------------- |
| `1xx` | 요청 처리 중         |
| `2xx` | 성공                 |
| `3xx` | 다른 주소로 이동     |
| `4xx` | 클라이언트 요청 문제 |
| `5xx` | 서버 문제            |

자주 사용하는 상태 코드는 다음과 같다.

| 상태 코드 | 의미                            |
| --------- | ------------------------------- |
| `200`     | 요청 성공                       |
| `201`     | 데이터 생성 성공                |
| `301`     | 주소가 영구적으로 변경됨        |
| `302`     | 임시로 다른 주소로 이동         |
| `400`     | 잘못된 요청                     |
| `401`     | 인증 필요                       |
| `403`     | 접근 금지                       |
| `404`     | 페이지 또는 자원을 찾을 수 없음 |
| `500`     | 서버 내부 오류                  |

예를 들어 데이터를 새로 생성했다면 `201`을 사용할 수 있다.

```js
res.status(201).join({
  message: "등록 완료"
})
```

수정이나 삭제처럼 이미 존재하는 지원을 처리한 경우에는 보통 `200` 또는 `204` 를 많이 사용한다.

----------

## 16. 모듈

모듈은 코드를 기능별 파일로 나누어 재사용할 수 있게 만든 구조이다.

Node.js에서는 크게 CommonJS 방식과 ES Module 방식이 있다.

----------

## 17. CommonJS 방식

CommonJS는 Node.js에서 오래전부터 사용하던 모듈 방식이다.

`require()` 로 불러오고, `module.exports`  로 내보낸다.

**counter.js**

```js
let count = 0

function increase(){
  count++
}

function getCount(){
  return count
}

module.exports.increase = incease
module.exports.getCount = getCount
```

**main.js**

```js
const counter = require.("./counter")

counter.increase()
console.log(counter.getCount())
```

출력

```tex
1
```



## 18. ES Module 방식

ES Module은 `import`, `export` 를 사용하는 모듈 방식이다.

파일 확장자를 `.mjs` 로 사용하거나, `package.json` 에 `"type": "module"` 을 설정하면 사용할 수 있다.

**counter.mjs**

```js
let count = 0

export function increase(){
  count++
}

export function getCount(){
  return count
}
```

**main.mjs**

```js
import { increase, getCount } from "./counter.mjs"

increase()
console.log(getCount())
```

출력

```tex
1
```

## 19. CommonJS와 ES Module 비교

| 구분         | CommonJS          | ES Module                 |
| ------------ | ----------------- | ------------------------- |
| 불러오기     | `require()`       | `import`                  |
| 내보내기     | `module.exports`  | `export`                  |
| 주 사용 파일 | `.js`             | `.mjs` 또는 module 설정   |
| 특징         | Node.js 전통 방식 | JavaScript 표준 모듈 방식 |

현재 예제에서 `5_게시물작성.js`, `6_json요청.js`는 CommonJS 방식이고, `7_라우팅.mjs`, `8_라우트활용.mjs`는 ES Module 방식이다.



## 20. app.route()

같은 경로에서 여러 HTTP 메서드를 처리할 때는 `app.route)()` 를 사용할 수 있다.

```js
import express from "express" 

const app = express()

app.route("/posts")
  .get((req, res) => {
    res.status(200).send("/posts GET 호출")
  })
  .post((req, res) => {
    res.status(201).send("/posts POST 호출")
  })
  .put((req, res) => {
    res.status(200).send("/posts PUT 호출")
  })
  .delete((req, res) => {
    res.status(200).send("/posts DELETE 호출")
  })

app.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

`/post` 라는 같은 경로를 기준으로 GET, POST, PUT, DELETE 요청을 한 곳에 묶을 수 있다.

```tex
GET    /posts  → 글 목록 조회
POST   /posts  → 글 작성
PUT    /posts  → 글 수정
DELETE /posts  → 글 삭제
```

라우트가 많지 않을 때는 `app.route()` 로 묶으면 읽기 좋다.

하지만 기능이 많아지면 파일이 커지므로 `express.Router()` 로 분리하는 것이 좋다.



## 21. express.Router()

`express.Router()`는 라우팅 코드를 별도 파일로 분리할 때 사용한다.

프로젝트가 커지면 모든 라우트를 하나의 파일에 작성하기 어렵다.

```tex
app.js
├── users 관련 라우트
├── posts 관련 라우트
├── products 관련 라우트
└── comments 관련 라우트
```

이런 구조는 코드가 길어질수록 유지보수가 어려워진다.
그래서 기능별로 라우터 파일을 나눈다.

```tex
routes/
├── user.mjs
└── post.mjs
```



## 22. 라우터 활용

```js
import express from "express"
import userRouter from "./routes/user.mjs"
import postRouter from "./routes/post.mjs"

const app = express()

app.use(express.json())

app.use("/users", userRouter)
app.use("/posts", postRouter)

app.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

### 코드 설명

```js
import userRouter from "./routes/user.mjs"
import postRouter from "./routes/post.mjs"
```

사용자 라우터와 게시물 라우터를 가져온다.

```js
app.use("/users", userRouter)
```

`/users`로 시작하는 요청은 `userRouter`가 처리한다.

```js
app.use("/posts", postRouter)
```

`/posts`로 시작하는 요청은 `postRouter`가 처리한다.



## 23. user 라우터

```js
import express from "express"

const router = express.Router()

// GET /users
router.get("/", (req, res) => {
  res.status(200).send("GET: /users 회원정보보기")
})

// POST /users
router.post("/", (req, res) => {
  res.status(201).send("POST: /users 회원가입")
})

// PUT /users/:id
router.put("/:id", (req, res) => {
  res.status(200).send(`PUT: /users/${req.params.id} 정보수정`)
})

// DELETE /users/:id
router.delete("/:id", (req, res) => {
  res.status(200).send(`DELETE: /users/${req.params.id} 회원탈퇴`)
})

export default router
```

라우터 파일에서는 `app` 대신 `router`를 사용한다.

```js
const router = express.Router()
```

마지막에는 다른 파일에서 사용할 수 있도록 내보낸다.

```js
export default router
```

------

## 24. post 라우터

```js
import express from "express"

const router = express.Router()

// GET /posts
router.get("/", (req, res) => {
  res.status(200).send("GET: /posts 글보기")
})

// POST /posts
router.post("/", (req, res) => {
  res.status(201).send("POST: /posts 글 작성하기")
})

// PUT /posts/:id
router.put("/:id", (req, res) => {
  res.status(200).send(`PUT /posts/${req.params.id} 글 수정하기`)
})

// DELETE /posts/:id
router.delete("/:id", (req, res) => {
  res.status(200).send(`DELETE /posts/${req.params.id} 글 삭제하기`)
})

export default router
```

------

## 25. 라우터가 실제 주소로 연결되는 방식

메인 파일에서 다음처럼 연결했다.

```js
app.use("/users", userRouter)
app.use("/posts", postRouter)
```

라우터 파일 안에서는 `/` 또는 `/:id`처럼 상대 경로를 작성한다.

```js
router.get("/")
router.put("/:id")
```

실제 주소는 `app.use()`에 적은 기본 경로와 라우터 내부 경로가 합쳐져 만들어진다.

| app.use 기본 경로 | 라우터 내부 경로 | 실제 요청 주소 |
| ----------------- | ---------------- | -------------- |
| `/users`          | `/`              | `/users`       |
| `/users`          | `/:id`           | `/users/:id`   |
| `/posts`          | `/`              | `/posts`       |
| `/posts`          | `/:id`           | `/posts/:id`   |

예를 들어 다음 코드는,

```js
app.use("/users", userRouter)
router.delete("/:id")
```

최종적으로 아래 요청을 처리한다.

```js
DELETE /users/3
```



## 26. 정리

게시물 작성 예제는 Express에서 `form` 데이터를 처리하고, 파일에 저장하고, 저장된 데이터를 다시 화면에 보여주는 흐름이다.

`express.urlencoded()` 를 사용하면 HTML form 데이터를 `req.body` 에서 읽을 수 있고, `fs.appendFile()` 과 `fs.readFile()` 을 사용하면 파일 기반으로 간단한 저장 기능을 만들 수 있다.

JSON 요청 예제는 API 서버의 기본 구조를 보여준다.

`express.json()`으로 JSON 데이터를 파싱하고, `res.status()` 와 `res.json()` 으로 상태 코드와 JSON 응답을 함께 보낼 수 있다.

라우팅 예제에서는 같은 경로를 `app.route()` 로 묶는 방법과, 규모가 커졌을 때 `express.Router()` 로 라우터 파일을 분리하는 방법을 확인했다.

라우터를 분리하면 사용자 기능, 게시물 기능처럼 역할별로 코드를 나눌 수 있어 유지보수가 쉬워진다.

Express 서버 개발의 핵슴은 다음과 같다.

```tex
요청 주소 설계
HTTP 메서드 구분
미들웨어로 요청 데이터 처리
라우터 분리로 코드 구조화
```

