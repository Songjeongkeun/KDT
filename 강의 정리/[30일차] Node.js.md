# [30일차] Node.js, MongoDB

MongoDB는 대표적인 NoSQL 데이터베이스 중 하나로, 데이터를 테이블이 아닌 문서(Documnet) 형태로 저장한다.

Express 서버와 MongoDB를 연결하면 클라이언트가 보낸 데이터를 데이터베이스에 저장하고, 다시 조회하거나 수정, 삭제하는 API를 만들 수 있다.



## 1. MongoDB란?

MongoDB는 NoSQL 데이터베이스 시스템 중 하나다. 관계형 데이터베이스처럼 데이터를 행과 열로 이루어진 테이블에 저장하지 않고, JSON과 비슷한 BSON(Binary JSON) 형식의 문서로 저장한다.

관계형 데이터베이스에서는 보통 다음처럼 테이블 구조를 먼저 정한다.

```tex
member 테이블
┌────┬────────┬────────┬───────────────┐
│ no │ userid │ userpw │ email         │
├────┼────────┼────────┼───────────────┤
│ 1  │ apple  │ 1111   │ a@apple.com   │
│ 2  │ banana │ 2222   │ b@banana.com  │
└────┴────────┴────────┴───────────────┘
```

MongoDB에서는 데이터를 문서 형태로 저장한다.

```js
{
  no: 1,
  userid: "apple",
  userpw: "1111",
  email: "apple@apple.com"
}
```



## 2. NoSQL 이란?

NoSQL은 Not Only SQL의 의미로, 관계형 데이터베이스가 아닌 다양한 방식의 데이터 저장 구조를 말한다.

대표적인 NoSQL 데이터베이스에는 다음이 있다.

| 종류         | 설명                             |
| ------------ | -------------------------------- |
| Document DB  | 문서 형태로 데이터 저장          |
| Key-Value DB | key와 value 형태로 데이터 저장   |
| Graph DB     | 노드와 관계 중심으로 데이터 저장 |
| Column DB    | 컬럼 단위로 데이터 저장          |

MongoDB는 이 중에서 문서 지향 데이터베이스(Document-Oriented Database)에 해당한다.



## 3. 문서 지향 데이터베이스

문서 지향 데이터베이스는 데이터를 문서(Document) 단위로 저장한다.

MongoDB의 문서는 BSON 형식으로 저장되며, 구조는 JSON과 매우 비슷하다.

```js
{
  _id: ObjectID("..."),
  text: "점심 메뉴 정해줘",
  createdAt: ISODate("2026-07-01T...")
}
```

문서는 key-value 쌍으로 이루어져 있다.

| key         | value                           |
| ----------- | ------------------------------- |
| `_id`       | MongoDB가 자동 생성하는 고유 ID |
| `text`      | 메모 내용                       |
| `createdAt` | 생성 날짜                       |

MongoDB에선ㄴ 여러 문서가 모여 컬레션(Collection)을 이룬다.

```tex
Database
└── memo
    └── Collection
        └── memos
            ├── Document 1
            ├── Document 2
            └── Document 3
```

관계형 데이터베이스와 비교하면 다음과 비슷하게 볼 수 있다.

| 관계형 DB   | MongoDB    |
| ----------- | ---------- |
| Database    | Database   |
| Table       | Collection |
| Row         | Document   |
| Column      | Field      |
| Primary Key | `_id`      |



## 4. 스키마가 없는 구조

MongoDB는 관계형 데이터베이스처럼 테이블 스키마를 반드시 먼저 정의하지 않아도 된다.

문서마다 서로 다른 필드를 가질 수 있다.

예를 들어 다음 데이터들이 같은 컬렉션에 저장될 수 있다.

```js
{ no: 1, uerid: "apple", userpw: "1111" }
```

```js
{ no: 2, userid: "banana", userpw: "2222", email: "banana@banana.com" }
```

```js
{ name: "orange", hp: "010-1111-1111" }
```

이처럼 유연하게 데이터를 저장할 수 있다는 장점이 있다.

하지만 너무 자유롭게 저장하면 데이터 구조가 흐트러질 수 있으므로 실제 프로젝트에서는 어느 정도 규칙을 정해두는 것이 좋다.



## 5. MongoDB를 사용하는 이유

MongoDB는 다음과 같은 상황에 많이 사용된다.

| 상황                                   | 이유                                   |
| -------------------------------------- | -------------------------------------- |
| 데이터 구조가 자주 바뀌는 서비스       | 스키마가 유연하다                      |
| JSON 형태 데이터를 많이 다루는 서비스  | 문서 구조가 JavaScript 객체와 비슷하다 |
| 빠르게 프로토타입을 만들어야 하는 경우 | 테이블 설계 부담이 적다                |
| 대량의 비정형 데이터를 저장하는 경우   | 유연한 구조가 유리하다                 |

단, 모든 상황에서 MongoDB가 더 좋은 것은 아니다.

복잡한 조인, 강한 데이터 정합성, 명확한 관계 구조가 중요한 시스템에서는 관계형 데이터베이스가 더 적합할 수 있다.



## 6. 요청 본문 Body

클라이언트가 서버에 데이터를 보낼 때, 그 데이터는 요청 본문(Body) 에 담겨온다.

예를 들어 클라이언트가 메모를 추가하기 위해 다음 JSON을 보낼 수 있다.

```json
{
  "text": "점심 메뉴 정해줘"
}
```

Express 서버에서는 `req.body()` 로 이 데이터를 읽는다.

```js
const { text } = req.body
```

단, JSON 요청 본문을 읽으려면 반드시 `express.json()` 미들웨어를 등록해야 한다.

```js
app.use(erxpress.json())
```



## 7.MongoDB 패키지 설치

Node.js에서 MongoDB를 사용하려면 `mongodb` 패키지를 설치한다.

```bash
npm install mongodb
```

설치 후 다음처럼 불러온다.

```js
const { MongoClient, ObjectId } = require("mongodb")
```

| 이름          | 역할                                   |
| ------------- | -------------------------------------- |
| `MongoClient` | MongoDB 서버와 연결하는 객체           |
| `ObjectId`    | MongoDB 문서의 `_id` 값을 다룰 때 사용 |



## 8. Express와 MongoDB 연결

```js
const express = require("express")
const path = require("path")
const { MongoClient, ObjectId } = require("mongodb")

const app = express()
const PORT = 3000

app.use(express.json())
app.use(express.static(path.join(__dirname, "public")))

const url = "mongodb+srv://<username>:<password>@<cluster-url>/"
const client = new MongoClient(url)

const dbName = "memo"
let memoCollection
```

### 설명

```js
app.use(express.json())
```

클라이언트가 보낸 JSON 요청 본문을 `req.body` 로 읽을 수 있게 한다.

```js
app.use(express.static(path.join(__dirname, "public")))
```

`public`폴더 안의 정적 파일을 브라우저에서 접근할 수 있게 한다.

예를 들어, `public/index.html` , `public/app.js` , `public/style.css` 를 웹 페이지로 사용할 수 있다.

```js
const client = new MongoClient(url)
```

MongoDB 에 연결할 클라이언트 객체를 만든다.



## 9. 서버 시작 함수

MongoDB 연결은 비동기 작업이다.

따라서 `async/await`를 사용해 MongoDB 연결이 성공한 뒤 서버를 실행한다.

```js
async function startServer(){
  try{
    await client.connect()
    console.log("MongoDB 연결 성공!!")
    
    const db = client.db(dbName)
    memoCollection = db.collection("memos")
    
    app.listen(PORT, () => {
      console.log("서버 실행 중...")
    })
  }catch (error) { 
  	console.log("MongoDB 연결 실패: ", error)
  }
}
```

### 흐름

```tex
MongoDB 연결 시도
  ↓
연결 성공
  ↓
memo 데이터베이스 선택
  ↓
memos 컬렉션 선택
  ↓
Express 서버 실행
```

MongoDB 연결 전에 서버가 먼저 실행되면 `memoCollection`이 준비되지 않은 상태에서 요청이 들어올 수 있다.

그래서 연결 성공 후 `app.listen()`을 실행하는 구조가 안전하다.



## 10. 메모 조회: GET `/memos`

메모 목록을 조회할 때는 `GET` 요청을 사용한다.

```js
app.get("/memos", async (req, res) => {
  try {
    const { keyword } = req.query
    let filter = {}

    if (keyword && keyword.trim() !== "") {
      filter = {
        text: { $regex: keyword.trim(), $options: "i" },
      }
    }

    const memos = await memoCollection
      .find(filter)
      .sort({ createdAt: -1 })
      .toArray()

    res.json({
      success: true,
      count: memos.length,
      memos,
    })
  } catch (error) {
    console.log("메모 조회 오류: ", error)
    res.status(500).json({
      success: false,
      message: "메모 조회 중 오류가 발생!",
    })
  }
})
```

## 11. 전체 메모 조회

브라우저에서 다음 주소로 접속하면 전체 메모를 조회할 수 있다.

```tex
http://127.0.0.1:3000/memos
```

`GET` 요청은 브라우저 주소창에서도 쉽게 확인할 수 있다.

응답 예시는 다음과 같다.

```json
{
  "success": true,
  "count": 2,
  "memos": [
    {
      "_id": "6864...",
      "text": "MongoDB 공부",
      "createdAt": "2026-07-01T..."
    },
    {
      "_id": "6863...",
      "text": "Express 복습",
      "createdAt": "2026-07-01T..."
    }
  ]
}
```

## 12. Query String으로 검색하기

검색어를 전달할 때는 Query String을 사용할 수 있다.

```tex
http://127.0.0.1:3000/memos?keyword=공부
```

서버에서는 `req.query.keyword` 로 읽을 수 있다.

```js
const { keyword } = req.query
```

만약 `keyword=공부` 가 들어오면 다음과 같은 필터를 만든다.

```js
filter = {
  text: { $regex: keyword.trim(), $options: "i" },
}
```

> **$regex**
>
> $regex 는 MongoDB에서 문자열 패턴 검색을 할 때 사용하는 연산자이다.
>
> ```tex
> text: { $regex: "공부" }
> ```
>
> 이 조건은 `text` 필드 안에 `"공부"`라는 문자열이 포함된 문서를 찾겠다는 뜻이다.
>
> 예를 들어 다음 문서들이 있다고 하자.
>
> ```js
> { text: "MongoDB 공부하기" }
> { text: "Node.js 복습하기" }
> { text: "알고리즘 공부" }
> ```
>
> `$regex: "공부"` 로 검색하면 다음 두 문서가 조회된다.
>
> ```js
> { text: "MongoDB 공부하기" }
> { text: "알고리즘 공부" }
> ```



>**$options: "i"**
>
>$options: "i" 는 대소문자를 구분하지 않고 검색하겠다는 뜻이다.
>
>```js
>text: { $regex: "mongo", $options: "i"}
>```
>
>위 조건은 다음 문자열을 모두 찾을 수 있다.
>
>```tex
>MongoDB
>mongodb
>MONGODB
>```



## 13. 배열로 반환: toArray()

MongoDB의 `find()` 는 바로 배열을 반환하지 않는다.

커서(Cursor)를 반환하기 때문에 실제 배열로 사용하려면 `toArray()` 를 호출한다.

```js
const memos = await memoCollection.find(filter).toArray()
```



## 14. 메모 추가: POST `/memo`

새로운 메모를 저장할 때는 `POST` 요청을 사용한다.

```js
app.post("/memo", async (req, res) => {
  try{
    const { text } = req.body
    
    if(!text || text.trim() === ""){
      return res.status(400).json({
        success: false,
        message: "메모 내용을 입력해주세요"
      })
    }
    const newMenmo = {
      text: text.trim(),
      createdAt: new Date()
    }
    
    await memoCollection.insertOne(newMemo)
    
    const memos = await memoCollection
    	.find()
    	.sort({ createdAt: -1})
    	.toArray()
    
    res.status(201)json({
      success: true,
      message: "메모가 추가되었습니다.",
      memos
    })
  }catch (error) {
    console.log("메모 저장 오류: ", error)
    res.status(500).json({
      success: false,
      message: "서버 오류가 발생!!",
    })
  }
})
```

### 요청 Body

```json
{
  "text": "점심 메뉴 정해줘"
}
```

### 저장되는 문서

```js
{
  _id : ObjectId()
  text: "점심 메뉴 정해줘",
  createdAt: new Date()
}
```



## 15. insertOne()

`insertOne()` 은 컬레셕에 문서 하나를 추가한다.

```js
await memoCollection.insertOne(newMemo)
```

저장 후 다시 전체 메모를 조회해 최신 목록을  응답한다.

```js
const memos = await memoCollection.find().sort({ createdAt: -1 }).toArray()
```

이렇게 하면 클라이언트는 추가된 메모가 반영된 전체 목록을 바로 다시 그릴 수 있다.



## 16. 메모 수정: PUT `/memos/:id`

이미 존재하는 메모를 수정할 때는 `PUT` 요청을 사용한다.

```js
app.put("/memos/:id", async (req, res) => {
  try {
    const { id } = req.params
    const { text } = req.body

    if (!ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: "올바르지 않은 메모 id 형식!!",
      })
    }

    if (!text || text.trim() === "") {
      return res.status(400).json({
        success: false,
        message: "변경할 메모 내용을 입력해주세요",
      })
    }

    const result = await memoCollection.findOneAndUpdate(
      { _id: new ObjectId(id) },
      {
        $set: {
          text: text.trim(),
          updatedAt: new Date(),
        },
      },
      {
        returnDocument: "after",
      }
    )

    if (!result) {
      return res.status(404).json({
        success: false,
        message: "해당 id의 메모를 찾을 수 없습니다",
      })
    }

    res.json({
      success: true,
      message: "메모가 수정되었습니다. (PUT)",
      memo: result,
    })
  } catch (error) {
    console.log("메모 수정 오류(PUT): ", error)
    return res.status(500).json({
      success: false,
      message: "메모 수정 중 오류가 발생!!",
    })
  }
})
```



## 17. URL 파라미터

URL 파라미터는 주소 안에 들어가는 동적인 값이다.

```tex
http://127.0.0.1:3000/memos/:id
```

실제 요청 예시는 다음과 같다.

```tex
http://127.0.0.1:3000/memos/6a447d778c0c217673dde5a7
```

서버에서는 `req.params.id` 로 읽는다.

```js
const { id } = req.params
```



## 18. ObjectId 검사

MongoDB의 `_id` 는 일반 문자열이 아니라 `ObjectId` 형식이다.

따라서 클라이언트가 보낸 id가 올바른 형식인지 먼저 검사한다.

```js
if (!ObjectId.isValid(id)) {
  return res.status(400).json({
    success: false,
    message: "올바르지 않은 메모 id 형식!!",
  })
}
```

형식이 올바르다면 `new ObjectId(id)` 로 MongoDB가 이해할 수 있는 값으로 변환한다.

```js
{ _id: new ObjectId(id) }
```



## 19. findOneAndUpdate()

`findOneAndUpdate()` 는 조건에 맞는 문서 하나를 찾아 수정한다.

```js
const result = await memoCollection.findOneAndUpdate(
  { _id: new ObjectId(id) },
  {
    $set: {
      text: text.trim(),
      updatedAt: new Date(),
    },
  },
  {
    returnDocument: "after",
  }
)
```

각 부분의 의미는 다음과 같다.

| 부분                        | 의미                    |
| --------------------------- | ----------------------- |
| `{ _id: new ObjectId(id) }` | 수정할 문서를 찾는 조건 |
| $set                        | 특정 필드만 수정        |
| `text`                      | 새 메모 내용            |
| `updatedAt`                 | 수정 날짜               |
| `returnDocument: "after"`   | 수정 후 문서를 반환     |



## 20. PUT과 PATCH 차이

`PUT` 과 `PATCH`는 모두 수정 요청에 사용된다.

하지만 의미가 조금 다르다.

| 메서드  | 의미                             |
| ------- | -------------------------------- |
| `PUT`   | 자원 전체를 교체하거나 전체 수정 |
| `PATCH` | 자원의 일부 필드만 부분 수정     |

예를 들어 메모 문서가 다음과 같다고 하자.

```js
{
  text: "기존 메모",
  color: "yellow",
  pinned: false
}
```

`PUT`은 전체 데이터를 새 값으로 교체하는 의미에 가깝다.

```js
{
  "text": "수정된 메모",
  "color": "white",
  "pinned": true
}
```

`PATCH`는 필요한 필드만 일부 수정하는 의미에 가깝다.

```
{
  "text": "수정된 메모"
}
```



## 21. 메모 삭제: DELETE `/memos/:id` 

메모를 삭제할 때는 `DELETE` 요청을 사용한다.

```js
app.delete("/memos/:id", async (req, res) => {
  try {
    const { id } = req.params

    if (!ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: "올바르지 않은 메모 id 형식!!",
      })
    }

    const result = await memoCollection.deleteOne({
      _id: new ObjectId(id),
    })

    if (result.deletedCount === 0) {
      return res.status(404).json({
        success: false,
        message: "삭제할 메모를 찾을 수 없습니다.",
      })
    }

    const memos = await memoCollection
      .find()
      .sort({ createdAt: -1 })
      .toArray()

    res.json({
      success: true,
      message: "메모가 삭제되었습니다.",
      memo: result,
      count: memos.length,
      memos,
    })
  } catch (error) {
    console.log("메모 삭제 오류: ", error)
    return res.status(500).json({
      success: false,
      message: "메모 삭제 중 오류가 발생!!",
    })
  }
})
```

### delteOne()

`deleteOne()` 은 조건에 맞는 문서 하나를 삭제한다.

```js
const result = awailt memoCollection.deleteOne({ _id: new ObjectId(id), })
```

삭제 결과는 `deleteCount` 로 학인할 수 있다.

```js
if (result.deletedCount === 0) {
  return res.status(404).json({
    success: false,
    message: "삭제할 메모를 찾을 수 없습니다.",
  })
}
```

`deleteCount`가 `0`이면 조건에 맞는 문서를 찾기 못했다는 뜻이다.



## 22. API 전체 정리

| 기능           | Method   | URL                   | 데이터 위치                      |
| -------------- | -------- | --------------------- | -------------------------------- |
| 메모 전체 조회 | `GET`    | `/memos`              | 없음                             |
| 메모 검색      | `GET`    | `/memos?keyword=공부` | `req.query.keyword`              |
| 메모 추가      | `POST`   | `/memo`               | `req.body.text`                  |
| 메모 수정      | `PUT`    | `/memos/:id`          | `req.params.id`, `req.body.text` |
| 메모 삭제      | `DELETE` | `/memos/:id`          | `req.params.id`                  |



## 23. fetch로 메모 조회하기

```js
const memoInput = document.getElementById("memoInput")
const addBtn = document.getElementById("addBtn")
const memoList = document.getElementById("memoList")

async function loadMemos() {
  try {
    const response = await fetch("/memos")
    const data = await response.json()
    renderMemos(data.memos)
  } catch (error) {
    console.log("메모 조회 실패: ", error)
  }
}

loadMemos()
```

`fetch("/memos")`는 서버의 `GET /memos` API를 호출한다.
응답으로 받은 JSON 데이터를 `response.json()`으로 JavaScript 객체로 변환한 뒤 `renderMemos()`에 전달한다.

------

## 24. fetch로 메모 추가하기

```js
addBtn.addEventListener("click", async () => {
  const text = memoInput.value.trim()

  if (!text) {
    alert("메모를 입력하세요")
    return
  }

  try {
    const response = await fetch("/memo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    })

    const data = await response.json()
    memoInput.value = ""
    renderMemos(data.memos)
  } catch (error) {
    console.log("메모 추가 실패", error)
  }
})
```

### 코드 설명

```js
const text = memoInput.value.trim()
```

입력창의 값을 가져오고 앞뒤 공백을 제거한다.

```js
if (!text) {
  alert("메모를 입력하세요")
  return
}
```

빈 값이면 요청을 보내지 않고 중단한다.

```js
headers: {
  "Content-Type": "application/json",
}
```

서버에게 JSON 형식으로 데이터를 보낸다고 알려준다.

```js
body: JSON.stringify({ text })
```

JavaScript 객체를 JSON 문자열로 변환해 요청 본문에 담는다.

------

## 25. 메모 목록 화면에 그리기

```js
function renderMemos(memos) {
  memoList.innerHTML = ""

  memos.forEach((memo) => {
    const li = document.createElement("li")
    li.className = "memo-item"
    li.innerHTML = `
      <span>${memo.text}</span>
      <div class="memo-buttons">
        <button>수정</button>
        <button>삭제</button>
      </div>
    `
    memoList.appendChild(li)
  })
}
```

### 흐름

```
기존 목록 비우기
  ↓
메모 배열 반복
  ↓
li 요소 생성
  ↓
메모 텍스트와 버튼 추가
  ↓
ul에 li 추가
```

현재 프론트엔드에는 수정 버튼과 삭제 버튼 UI가 있지만, 실제 `PUT`, `DELETE` 요청 이벤트는 아직 연결되어 있지 않다.
서버에는 수정과 삭제 API가 있으므로 버튼에 이벤트를 추가하면 기능을 완성할 수 있다.

------

## 26. 수정 버튼 연결 예시

수정 버튼을 동작시키려면 각 메모의 `_id`를 이용해 `PUT /memos/:id` 요청을 보내면 된다.

```js
async function updateMemo(id, oldText) {
  const newText = prompt("수정할 내용을 입력하세요", oldText)

  if (!newText || newText.trim() === "") {
    return
  }

  const response = await fetch(`/memos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: newText }),
  })

  const data = await response.json()
  console.log(data.message)
  loadMemos()
}
```

------

## 27. 삭제 버튼 연결 예시

삭제 버튼을 동작시키려면 `DELETE /memos/:id` 요청을 보내면 된다.

```js
async function deleteMemo(id) {
  const ok = confirm("정말 삭제하시겠습니까?")

  if (!ok) {
    return
  }

  const response = await fetch(`/memos/${id}`, {
    method: "DELETE",
  })

  const data = await response.json()
  console.log(data.message)
  renderMemos(data.memos)
}
```

`renderMemos(data.memos)`를 호출하면 삭제 후 서버가 보내준 최신 목록으로 화면을 다시 그릴 수 있다.

------

## 28. CSS 구조

메모 앱은 `public/style.css`로 화면을 꾸민다.

```css
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  padding: 40px;
}

.container {
  max-width: 600px;
  margin: auto;
  background: white;
  padding: 20px;
  border-radius: 10px;
}

.input-area {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.memo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #eee;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}
```



## 29. 전체 흐름 정리

```tex
브라우저 접속
  ↓
Express가 public/index.html 제공
  ↓
app.js 실행
  ↓
fetch("/memos")로 메모 목록 요청
  ↓
Express 서버가 MongoDB에서 메모 조회
  ↓
JSON 응답
  ↓
브라우저가 메모 목록 렌더링
```

메모 추가 흐름은 다음과 같다.

```tex
입력창에 메모 작성
  ↓
추가 버튼 클릭
  ↓
fetch("/memo", { method: "POST" })
  ↓
Express가 req.body.text 읽음
  ↓
MongoDB에 insertOne()
  ↓
최신 메모 목록 응답
  ↓
브라우저가 목록 다시 렌더링
```



## 30. 정리

MongoDB는 JSON과 비슷한 문서 형태로 데이터를 저장하는 NoSQL 데이터베이스다.
테이블 구조를 엄격하게 먼저 정의하지 않아도 되기 때문에 데이터 구조를 유연하게 다룰 수 있다.

Express에서는 `express.json()` 미들웨어를 사용해 클라이언트가 보낸 JSON 요청 본문을 `req.body`로 읽을 수 있다.
MongoDB는 `MongoClient`로 연결하고, `db.collection()`으로 컬렉션을 선택한 뒤 `find()`, `insertOne()`, `findOneAndUpdate()`, `deleteOne()` 같은 메서드로 데이터를 다룬다.

이번 메모 앱의 핵심은 다음과 같다.

```
GET /memos          메모 조회
GET /memos?keyword  메모 검색
POST /memo          메모 추가
PUT /memos/:id      메모 수정
DELETE /memos/:id   메모 삭제
```

그리고 클라이언트에서는 `fetch()`를 사용해 서버 API를 호출한다.
서버는 MongoDB와 통신한 뒤 JSON으로 결과를 돌려주고, 브라우저는 그 결과를 이용해 화면을 다시 그린다.

즉, 이번 예제는 Express, MongoDB, fetch가 연결되는 기본적인 풀스택 흐름을 이해하기 좋은 구조다.