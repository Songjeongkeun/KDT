# Node.js 기초 정리: HTTP 서버, 요청·응답, 파일 입출력, Express

Node.js는 브라우저 밖에서도 JavaScript를 실행할 수 있게 해주는 런타임이다.  
브라우저에서 JavaScript가 화면 조작이나 이벤트 처리에 많이 사용된다면, Node.js에서는 서버 생성, 파일 입출력, 데이터 처리, API 서버 개발 같은 작업을 할 수 있다.

이번 글에서는 다음 흐름으로 Node.js의 기본 개념을 정리한다.

1. `http` 모듈로 서버 만들기
2. 요청과 응답 처리하기
3. `fs` 모듈로 파일 읽기/쓰기
4. Express로 서버 코드 단순화하기
5. EJS로 HTML에 데이터 넣어 보여주기

---

## 1. Node.js와 서버

서버는 클라이언트의 요청을 받고, 그 요청에 맞는 응답을 돌려주는 프로그램이다.

웹 브라우저에서 `http://localhost:3000`에 접속하면 브라우저는 서버에게 요청을 보낸다.  
서버는 요청을 확인한 뒤 HTML, JSON, 이미지, 파일 같은 데이터를 응답으로 보내준다.

```text
브라우저(Client)  ---- 요청(Request) ---->  서버(Server)
브라우저(Client)  <--- 응답(Response) ---  서버(Server)
```

Node.js에서는 기본 내장 모듈인 `http`를 사용해 웹 서버를 만들 수 있다.

---

## 2. http 모듈로 서버 만들기

`http` 모듈은 Node.js에서 기본으로 제공하는 서버 관련 모듈이다.  
따로 설치하지 않아도 `require("http")`로 불러와 사용할 수 있다.

```js
const http = require("http")

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" })
  res.end("<h1>안녕하세요!</h1>")
})

server.listen(3000, () => {
  console.log("서버 실행 중..")
})
```

### 코드 설명

```js
const http = require("http")
```

Node.js의 내장 `http` 모듈을 불러온다.

```js
http.createServer((req, res) => {
  // 요청과 응답 처리
})
```

서버를 생성한다.  
콜백 함수의 매개변수 `req`와 `res`는 다음 의미를 가진다.

| 매개변수 | 의미 |
| --- | --- |
| `req` | 클라이언트가 보낸 요청 정보 |
| `res` | 서버가 클라이언트에게 보낼 응답 객체 |

```js
res.writeHead(200, { "Content-Type": "text/html" })
```

응답 상태 코드와 헤더 정보를 설정한다.

| 값 | 의미 |
| --- | --- |
| `200` | 요청이 정상 처리되었다는 의미 |
| `Content-Type` | 응답 데이터의 종류 |
| `text/html` | HTML 문서로 응답한다는 의미 |

```js
res.end("<h1>안녕하세요!</h1>")
```

응답을 종료하면서 브라우저에 HTML 문자열을 보낸다.

```js
server.listen(3000)
```

서버를 3000번 포트에서 실행한다.  
실행 후 브라우저에서 아래 주소로 접속할 수 있다.

```text
http://localhost:3000
```

---

## 3. Content-Type

`Content-Type`은 서버가 응답하는 데이터의 형식을 브라우저에게 알려주는 헤더다.  
브라우저는 이 값을 보고 응답을 HTML로 해석할지, JSON으로 해석할지, 이미지로 처리할지 결정한다.

| Content-Type | 의미 |
| --- | --- |
| `text/html` | HTML 문서 |
| `text/plain` | 일반 텍스트 |
| `application/json` | JSON 데이터 |
| `text/css` | CSS 파일 |
| `application/javascript` | JavaScript 파일 |
| `image/png` | PNG 이미지 |
| `image/jpeg` | JPEG 이미지 |
| `multipart/form-data` | 파일 업로드 등에 사용 |

예를 들어 JSON 데이터를 응답할 때는 다음처럼 작성한다.

```js
res.writeHead(200, { "Content-Type": "application/json" })
res.end(JSON.stringify({ name: "김사과", age: 20 }))
```

---

## 4. 요청과 응답

HTTP 서버는 클라이언트가 어떤 주소로 요청했는지, 어떤 방식으로 요청했는지에 따라 다른 응답을 줄 수 있다.

### req.url

`req.url`은 클라이언트가 요청한 주소 경로를 나타낸다.

```js
console.log(req.url)
```

예를 들어 브라우저에서 다음 주소로 접속하면,

```text
http://localhost:3000/about
```

`req.url` 값은 다음과 같다.

```text
/about
```

### req.method

`req.method`는 요청 방식을 나타낸다.

대표적인 요청 방식은 다음과 같다.

| Method | 의미 |
| --- | --- |
| `GET` | 데이터를 조회할 때 사용 |
| `POST` | 데이터를 생성하거나 전송할 때 사용 |
| `PUT` | 데이터를 전체 수정할 때 사용 |
| `PATCH` | 데이터를 일부 수정할 때 사용 |
| `DELETE` | 데이터를 삭제할 때 사용 |

주의할 점은 `req.method` 값이 대문자로 들어온다는 것이다.

```js
if (req.method === "POST") {
  console.log("POST 요청")
}
```

`"post"`처럼 소문자로 비교하면 조건이 맞지 않는다.

---

## 5. http 모듈로 라우팅하기

라우팅은 요청 주소에 따라 다른 코드를 실행하는 방식이다.  
`http` 모듈만 사용할 때는 `req.url`과 `req.method`를 직접 확인해서 라우팅을 구현한다.

```js
const http = require("http")

const server = http.createServer((req, res) => {
  if (req.url === "/" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" })
    res.end("<h1>메인 페이지</h1>")
    return
  }

  if (req.url === "/about" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" })
    res.end("<h1>소개 페이지</h1>")
    return
  }

  if (req.url === "/api/user" && req.method === "GET") {
    const user = {
      name: "김사과",
      age: 20,
      job: "개발자",
    }

    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" })
    res.end(JSON.stringify(user))
    return
  }

  res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" })
  res.end("<h1>페이지를 찾을 수 없다.</h1>")
})

server.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

### 실행 결과

| 접속 주소 | 응답 |
| --- | --- |
| `/` | 메인 페이지 |
| `/about` | 소개 페이지 |
| `/api/user` | JSON 사용자 데이터 |
| 그 외 주소 | 404 페이지 |

---

## 6. Query String 처리하기

Query String은 URL 뒤에 `?`를 붙이고 데이터를 전달하는 방식이다.

```text
http://localhost:3000/?userid=apple&username=김사과
```

위 주소에서 Query String은 다음 부분이다.

```text
userid=apple&username=김사과
```

Node.js에서는 `URL` 객체를 사용하면 Query String을 쉽게 꺼낼 수 있다.

```js
const http = require("http")

const server = http.createServer((req, res) => {
  const requestUrl = new URL(req.url, `http://${req.headers.host}`)

  const pathname = requestUrl.pathname
  const userid = requestUrl.searchParams.get("userid")
  const username = requestUrl.searchParams.get("username")

  if (pathname === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" })
    res.end(`
      <h1>Query String 확인</h1>
      <p>userid: ${userid}</p>
      <p>username: ${username}</p>
    `)
    return
  }

  res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" })
  res.end("<h1>Not Found</h1>")
})

server.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

### 실행 주소

```text
http://localhost:3000/?userid=apple&username=김사과
```

### 출력 결과

```text
userid: apple
username: 김사과
```

---

## 7. JSON 데이터 응답

JSON은 JavaScript Object Notation의 약자로, 데이터를 주고받을 때 많이 사용하는 문자열 형식이다.

JavaScript 객체는 그대로 네트워크 응답으로 보낼 수 없기 때문에 문자열로 변환해야 한다.

```js
const user = {
  name: "김사과",
  age: 20,
  job: "개발자",
}

const jsonUser = JSON.stringify(user)
console.log(jsonUser)
```

### 출력 결과

```json
{"name":"김사과","age":20,"job":"개발자"}
```

문자열 형태의 JSON을 다시 객체로 바꿀 때는 `JSON.parse()`를 사용한다.

```js
const jsonStr = '{"name":"김사과","age":20,"job":"개발자"}'
const user = JSON.parse(jsonStr)

console.log(user.name)
console.log(user.age)
```

### 출력 결과

```text
김사과
20
```

---

## 8. nodemon

Node.js 서버 파일을 수정하면 보통 서버를 종료하고 다시 실행해야 한다.

```bash
node 4_express.js
```

`nodemon`을 사용하면 파일이 수정될 때 서버를 자동으로 재시작해준다.

```bash
npm install --save-dev nodemon
```

현재 프로젝트의 `package.json`에는 다음 실행 스크립트가 들어 있다.

```json
{
  "scripts": {
    "dev": "nodemon 4_express.js"
  }
}
```

따라서 아래 명령어로 개발 서버를 실행할 수 있다.

```bash
npm run dev
```

---

## 9. fs 모듈

`fs`는 File System의 약자로, Node.js에서 파일을 읽고 쓰고 삭제할 때 사용하는 내장 모듈이다.

```js
const fs = require("fs")
```

`fs` 모듈은 크게 동기 방식과 비동기 방식으로 사용할 수 있다.

| 방식 | 특징 |
| --- | --- |
| 동기 방식 | 작업이 끝날 때까지 다음 코드가 실행되지 않는다 |
| 비동기 방식 | 작업을 요청해두고 다음 코드가 먼저 실행될 수 있다 |

---

## 10. 파일 읽기

### 동기 방식 readFileSync

```js
const fs = require("fs")

try {
  const data = fs.readFileSync("./example1.txt", "utf8")
  console.log(data)
} catch (err) {
  console.log("파일 읽기 실패", err)
}
```

`readFileSync()`는 파일 읽기가 끝날 때까지 다음 코드로 넘어가지 않는다.  
간단한 실습 코드에서는 이해하기 쉽지만, 서버 코드에서는 요청 처리가 막힐 수 있으므로 주의해야 한다.

### 비동기 방식 readFile

```js
const fs = require("fs")

fs.readFile("example2.txt", "utf8", (err, data) => {
  if (err) {
    console.log("파일 읽기 실패", err)
    return
  }

  console.log(data)
})
```

`readFile()`은 파일을 읽은 뒤 콜백 함수를 실행한다.  
파일 읽기가 진행되는 동안 다른 코드가 먼저 실행될 수 있다.

---

## 11. 파일 쓰기

### 동기 방식 writeFileSync

```js
const fs = require("fs")

fs.writeFileSync("output1.txt", "Hello Node.js!")
console.log("파일 쓰기 완료")
```

`writeFileSync()`는 파일을 생성하거나 기존 파일 내용을 덮어쓴다.

### 비동기 방식 writeFile

```js
const fs = require("fs")

fs.writeFile("output2.txt", "Hello Async Node.js!", (err) => {
  if (err) {
    console.log("파일 쓰기 실패", err)
    return
  }

  console.log("파일 쓰기 완료")
})
```

비동기 방식은 작업이 끝난 뒤 콜백 함수가 실행된다.

---

## 12. 파일 내용 추가 appendFile

기존 파일의 내용을 지우지 않고 뒤에 내용을 추가하려면 `appendFile()`을 사용한다.

```js
const fs = require("fs")

fs.appendFile("output2.txt", "\n내용 추가!", (err) => {
  if (err) {
    console.log("파일 추가 실패", err)
    return
  }

  console.log("파일 내용 추가 완료")
})
```

---

## 13. 파일 삭제 unlink

파일을 삭제할 때는 `unlink()`를 사용한다.

```js
const fs = require("fs")

fs.unlink("output2.txt", (err) => {
  if (err) {
    console.log("파일 삭제 실패", err)
    return
  }

  console.log("파일 삭제 완료")
})
```

### 비동기 작업 순서 주의

다음처럼 `appendFile()`과 `unlink()`를 바로 이어서 실행하면, 파일 추가가 끝나기 전에 삭제가 먼저 실행될 수도 있다.

```js
fs.appendFile("output2.txt", "\n내용 추가!", () => {
  console.log("파일 내용 추가 완료")
})

fs.unlink("output2.txt", () => {
  console.log("파일 삭제 완료")
})
```

비동기 작업의 순서를 보장하려면 콜백 안에서 다음 작업을 실행한다.

```js
const fs = require("fs")

fs.appendFile("output2.txt", "\n내용 추가!", (err) => {
  if (err) {
    console.log("파일 추가 실패", err)
    return
  }

  console.log("파일 내용 추가 완료")

  fs.unlink("output2.txt", (err) => {
    if (err) {
      console.log("파일 삭제 실패", err)
      return
    }

    console.log("파일 삭제 완료")
  })
})
```

---

## 14. Express

Express는 Node.js에서 서버를 더 쉽게 만들 수 있도록 도와주는 웹 프레임워크다.

`http` 모듈만 사용하면 요청 주소, 요청 방식, 응답 헤더, 라우팅 등을 직접 처리해야 한다.  
Express를 사용하면 이런 작업을 더 간단하고 읽기 좋게 작성할 수 있다.

```bash
npm install express
```

기본 서버 코드는 다음과 같다.

```js
const express = require("express")

const app = express()
const port = 3000

app.get("/", (req, res) => {
  res.send("Hello Express!")
})

app.listen(port, () => {
  console.log("서버 실행중...")
})
```

### 코드 설명

```js
const express = require("express")
```

Express 모듈을 불러온다.

```js
const app = express()
```

Express 애플리케이션 객체를 생성한다.

```js
app.get("/", (req, res) => {
  res.send("Hello Express!")
})
```

`GET /` 요청이 들어왔을 때 실행할 코드를 정의한다.

```js
app.listen(3000)
```

3000번 포트에서 서버를 실행한다.

---

## 15. http 모듈과 Express 비교

### http 모듈

```js
if (req.url === "/" && req.method === "GET") {
  res.writeHead(200, { "Content-Type": "text/html" })
  res.end("Hello")
}
```

요청 주소와 요청 방식을 직접 비교해야 한다.

### Express

```js
app.get("/", (req, res) => {
  res.send("Hello")
})
```

라우팅을 메서드 단위로 나눠 작성할 수 있어 코드가 더 직관적이다.

---

## 16. Express 라우팅

Express에서는 요청 방식에 따라 `app.get()`, `app.post()` 같은 메서드를 사용한다.

```js
app.get("/", (req, res) => {
  res.send("메인 페이지")
})

app.get("/hello", (req, res) => {
  res.send("Hello 페이지")
})

app.post("/submit", (req, res) => {
  res.send("post로 호출!")
})
```

| 코드 | 의미 |
| --- | --- |
| `app.get("/", callback)` | `/` 주소로 들어온 GET 요청 처리 |
| `app.get("/hello", callback)` | `/hello` 주소로 들어온 GET 요청 처리 |
| `app.post("/submit", callback)` | `/submit` 주소로 들어온 POST 요청 처리 |

---

## 17. 미들웨어

미들웨어는 요청과 응답 사이에서 실행되는 함수다.

```text
요청 → 미들웨어 → 라우터 → 응답
```

Express에서는 `app.use()`를 사용해 미들웨어를 등록한다.

```js
app.use(express.urlencoded({ extended: true }))
```

위 코드는 HTML form에서 전송된 데이터를 `req.body`로 읽을 수 있게 해준다.

```js
app.post("/submit", (req, res) => {
  const { name, age } = req.body

  console.log("name: ", name)
  console.log("age: ", age)

  res.send("post로 호출!")
})
```

---

## 18. 정적 파일 제공

정적 파일은 이미지, CSS, JavaScript처럼 서버에서 그대로 제공하는 파일을 의미한다.

```js
app.use("/static", express.static("public"))
```

위 코드는 `public` 폴더 안의 파일들을 `/static` 주소로 접근할 수 있게 만든다.

예를 들어 `public/spring.png` 파일이 있다면 브라우저에서 다음 주소로 접근할 수 있다.

```text
http://localhost:3000/static/spring.png
```

---

## 19. EJS 템플릿 엔진

EJS는 HTML 안에 JavaScript 값을 넣어 동적으로 페이지를 만들 수 있게 해주는 템플릿 엔진이다.

```bash
npm install ejs
```

Express에서 EJS를 사용하려면 다음 설정이 필요하다.

```js
const path = require("path")

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "view"))
```

| 설정 | 의미 |
| --- | --- |
| `view engine` | 사용할 템플릿 엔진 설정 |
| `views` | EJS 파일이 들어 있는 폴더 경로 설정 |

---

## 20. EJS로 데이터 출력하기

`/hello` 주소로 접속하면 `hello.ejs` 파일을 렌더링한다.

```js
app.get("/hello", (req, res) => {
  res.render("hello", { name: "김사과" })
})
```

`res.render()`는 EJS 파일을 HTML로 변환해 응답한다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>환영합니다!</title>
</head>
<body>
  <h2>안녕하세요!! <%= name %>님 :)</h2>
</body>
</html>
```

`<%= name %>` 부분에 서버에서 전달한 `"김사과"` 값이 들어간다.

### 실행 결과

```text
안녕하세요!! 김사과님 :)
```

---

## 21. form 데이터 전송하기

`/submit` 주소로 접속하면 입력 폼을 보여준다.

```js
app.get("/submit", (req, res) => {
  res.render("submit")
})
```

`submit.ejs` 파일은 다음과 같다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>submit</title>
</head>
<body>
  <form action="/submit" method="post">
    <p>이름 <input type="text" name="name"></p>
    <p>나이 <input type="text" name="age"></p>
    <p><button type="submit">전송</button></p>
  </form>
</body>
</html>
```

폼에서 중요한 부분은 `action`, `method`, `name`이다.

| 속성 | 의미 |
| --- | --- |
| `action="/submit"` | 데이터를 보낼 주소 |
| `method="post"` | POST 방식으로 전송 |
| `name="name"` | 서버에서 `req.body.name`으로 읽을 수 있는 이름 |
| `name="age"` | 서버에서 `req.body.age`로 읽을 수 있는 이름 |

서버에서는 다음처럼 값을 받는다.

```js
app.post("/submit", (req, res) => {
  const { name, age } = req.body

  console.log("name: ", name)
  console.log("age: ", age)

  res.send("post로 호출!")
})
```

단, 이 코드를 사용하려면 반드시 아래 미들웨어가 먼저 등록되어 있어야 한다.

```js
app.use(express.urlencoded({ extended: true }))
```

---

## 22. 전체 Express 예제

```js
const express = require("express")
const path = require("path")

const app = express()
const port = 3000

app.use("/static", express.static("public"))
app.use(express.urlencoded({ extended: true }))

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "view"))

app.get("/", (req, res) => {
  res.send("Hello Express!")
})

app.get("/hello", (req, res) => {
  res.render("hello", { name: "김사과" })
})

app.get("/submit", (req, res) => {
  res.render("submit")
})

app.post("/submit", (req, res) => {
  const { name, age } = req.body

  console.log("name: ", name)
  console.log("age: ", age)

  res.send("post로 호출!")
})

app.listen(port, () => {
  console.log("서버 실행중...")
})
```

---

## 23. 실행 방법

패키지가 설치되어 있지 않다면 먼저 설치한다.

```bash
npm install
```

기본 Node.js 파일은 다음처럼 실행한다.

```bash
node 1_http.js
node 2_요청응답.js
node 3_파일입출력.js
```

Express 서버는 다음처럼 실행할 수 있다.

```bash
node 4_express.js
```

또는 `package.json`에 등록된 스크립트를 사용할 수 있다.

```bash
npm run dev
```

서버가 실행되면 브라우저에서 아래 주소로 접속한다.

```text
http://localhost:3000
```

서버를 종료할 때는 터미널에서 `Ctrl + C`를 누른다.

> 3000번 포트를 사용하는 서버는 동시에 하나만 실행할 수 있다.  
> 이미 서버가 실행 중이면 다른 서버 파일을 실행하기 전에 먼저 종료해야 한다.

---

## 24. 정리

Node.js의 기본 서버 흐름은 요청을 받고 응답을 보내는 구조다.

`http` 모듈은 Node.js의 기본 서버 기능을 직접 다룰 수 있게 해준다.  
`req.url`, `req.method`, `res.writeHead()`, `res.end()`를 사용하면 요청 주소와 방식에 따라 다른 응답을 만들 수 있다.

`fs` 모듈은 파일 읽기, 쓰기, 추가, 삭제를 처리한다.  
동기 방식은 순서가 명확하지만 작업 중 코드가 멈추고, 비동기 방식은 효율적이지만 실행 순서를 신경 써야 한다.

Express는 Node.js 서버 코드를 더 간결하게 작성할 수 있게 해준다.  
라우팅, 미들웨어, 정적 파일 제공, 템플릿 엔진 연결을 통해 실제 웹 애플리케이션에 가까운 구조를 만들 수 있다.

EJS는 HTML 안에 서버 데이터를 넣어 동적인 페이지를 만들 수 있게 해준다.  
`res.render()`로 EJS 파일을 렌더링하고, `<%= 값 %>` 문법으로 데이터를 출력한다.

이번 흐름을 이해하면 Node.js로 간단한 웹 서버를 만들고, 요청을 처리하고, 파일을 다루고, Express 기반 웹 페이지까지 구성할 수 있다.

---

## 25. 실습 중 주의할 점

### 1. `req.method`는 대문자로 비교한다

```js
if (req.method === "POST") {
  // 정상
}
```

```js
if (req.method === "post") {
  // 동작하지 않을 수 있다
}
```

### 2. Query String을 사용하려면 URL을 파싱해야 한다

```js
const requestUrl = new URL(req.url, `http://${req.headers.host}`)
const userid = requestUrl.searchParams.get("userid")
```

`parseUrl` 같은 변수를 사용하려면 먼저 직접 만들어야 한다.

### 3. JSON 문자열은 형식을 지켜야 한다

```js
const jsonStr = '{"name":"김사과","age":20}'
const user = JSON.parse(jsonStr)
```

JSON에서는 key와 문자열 value에 큰따옴표를 사용해야 한다.

### 4. 비동기 파일 작업은 순서가 보장되지 않는다

파일에 내용을 추가한 뒤 삭제해야 한다면, 추가 작업이 끝난 뒤 삭제 작업을 실행해야 한다.

### 5. 파일 이름 오타를 조심한다

```js
fs.writeFileSync("output1.txt.", "Hello Node.js!")
```

위 코드는 `output1.txt`가 아니라 `output1.txt.`라는 파일을 만든다.  
마지막 점까지 파일 이름에 포함되므로 의도한 이름인지 확인해야 한다.
