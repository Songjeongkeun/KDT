# Socket.IO로 실시간 채팅 만들기

Socket.IO는 클라이언트와 서버가 실시간으로 데이터를 주고받을 수 있게 해주는 라이브러리다.  
일반적인 HTTP 요청/응답 방식은 클라이언트가 요청해야 서버가 응답하지만, Socket.IO를 사용하면 서버도 클라이언트에게 즉시 이벤트를 보낼 수 있다.

이번 글에서는 Express와 Socket.IO를 이용해 실시간 채팅 기능을 만드는 흐름을 정리한다.

1. HTTP 통신과 실시간 통신의 차이
2. Socket.IO 개념
3. Express 서버와 Socket.IO 연결
4. 채팅방 입장 화면
5. 채팅방 화면
6. 닉네임과 채널 저장
7. `join`, `chat`, `changeChannel`, `disconnect` 이벤트
8. 방(Room)과 채널
9. 귓속말 기능
10. 코드에서 주의할 점

---

## 1. HTTP 요청/응답 방식

일반적인 웹 요청은 클라이언트가 서버에 요청을 보내고, 서버가 그 요청에 응답하는 구조다.

```text
클라이언트  ---- 요청 ---->  서버
클라이언트  <--- 응답 ----  서버
```

예를 들어 게시글 목록을 가져오는 요청은 다음처럼 동작한다.

```text
브라우저가 /posts 요청
  ↓
서버가 게시글 목록 응답
  ↓
브라우저가 화면에 출력
```

이 방식은 요청과 응답이 한 번 끝나면 연결이 끊긴다.  
따라서 서버가 새로운 데이터를 클라이언트에게 먼저 보내기 어렵다.

---

## 2. 실시간 통신이 필요한 이유

채팅 앱에서는 누군가 메시지를 보내면 다른 사용자 화면에도 즉시 보여야 한다.

HTTP 방식만 사용하면 클라이언트가 계속 서버에 새 메시지가 있는지 물어봐야 한다.

```text
새 메시지 있어?
새 메시지 있어?
새 메시지 있어?
```

이런 방식은 비효율적이다.  
Socket.IO를 사용하면 서버와 클라이언트가 연결을 유지하고, 필요한 순간에 이벤트를 주고받을 수 있다.

```text
클라이언트  <==== 연결 유지 ====>  서버
클라이언트  ---- chat 이벤트 ----> 서버
클라이언트  <--- message 이벤트 -- 서버
```

---

## 3. Socket.IO란?

Socket.IO는 실시간 양방향 통신을 쉽게 구현할 수 있게 해주는 라이브러리다.

대표적으로 다음 기능을 만들 때 사용한다.

| 기능 | 설명 |
| --- | --- |
| 실시간 채팅 | 메시지를 즉시 주고받음 |
| 알림 | 새로운 알림을 실시간 표시 |
| 게임 | 사용자 입력과 상태를 빠르게 동기화 |
| 실시간 대시보드 | 데이터 변경을 즉시 화면에 반영 |
| 협업 도구 | 여러 사용자가 동시에 문서나 화면을 편집 |

Socket.IO에서는 데이터를 주고받을 때 이벤트 이름을 정해서 사용한다.

```js
socket.emit("chat", { text: "안녕하세요" })
```

```js
socket.on("chat", (data) => {
  console.log(data)
})
```

---

## 4. 필요한 패키지

Express 서버와 Socket.IO를 사용하려면 다음 패키지가 필요하다.

```bash
npm install express socket.io
```

ES Module 방식으로 작성하기 때문에 파일 확장자는 `.mjs`를 사용한다.

```js
import express from "express"
import { Server } from "socket.io"
import { createServer } from "http"
```

---

## 5. 서버 기본 구조

```js
import express from "express"
import { Server } from "socket.io"
import { createServer } from "http"
import path from "path"
import { fileURLToPath } from "url"

const app = express()
const server = createServer(app)
const io = new Server(server)

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

app.use(express.static(path.join(__dirname, "public")))

server.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

---

## 6. `createServer(app)`를 사용하는 이유

Socket.IO는 Express의 `app.listen()`에 바로 붙이는 것이 아니라, Node.js의 HTTP 서버 객체에 연결한다.

```js
const app = express()
const server = createServer(app)
const io = new Server(server)
```

각 객체의 역할은 다음과 같다.

| 코드 | 역할 |
| --- | --- |
| `app` | Express 애플리케이션 |
| `server` | 실제 HTTP 서버 |
| `io` | Socket.IO 서버 객체 |

마지막에도 `app.listen()`이 아니라 `server.listen()`을 사용한다.

```js
server.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

---

## 7. ES Module에서 `__dirname` 만들기

CommonJS에서는 `__dirname`을 바로 사용할 수 있다.

```js
const path = require("path")
console.log(__dirname)
```

하지만 `.mjs` 파일은 ES Module 방식이기 때문에 `__dirname`이 기본 제공되지 않는다.  
따라서 다음처럼 직접 만들어야 한다.

```js
import path from "path"
import { fileURLToPath } from "url"

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
```

이렇게 만든 `__dirname`을 이용해 `public` 폴더를 정적 파일 폴더로 등록한다.

```js
app.use(express.static(path.join(__dirname, "public")))
```

---

## 8. 정적 파일 제공

```js
app.use(express.static(path.join(__dirname, "public")))
```

이 코드는 `public` 폴더 안의 HTML, CSS, JavaScript 파일을 브라우저에서 접근할 수 있게 만든다.

예를 들어 다음 파일들이 있다.

```text
public/
├── chat_index.html
└── chat_room.html
```

브라우저에서 다음 주소로 접근할 수 있다.

```text
http://localhost:3000/chat_index.html
http://localhost:3000/chat_room.html
```

---

## 9. 채팅 입장 화면

`chat_index.html`은 채팅방에 들어가기 전 닉네임과 채널을 선택하는 화면이다.

```html
<form id="loginForm">
  <h2>채팅방 입장</h2>
  <input type="text" id="nickname" placeholder="닉네임을 입력하세요">
  <select id="channel">
    <option value="lobby">대기실</option>
    <option value="sports">스포츠</option>
    <option value="programming">프로그래밍</option>
    <option value="music">음악</option>
  </select>
  <button type="submit">입장</button>
</form>
```

입력한 닉네임과 선택한 채널은 `localStorage`에 저장된다.

```js
document.getElementById("loginForm").onsubmit = (e) => {
  e.preventDefault()

  const nickname = document.getElementById("nickname").value.trim()
  const channel = document.getElementById("channel").value

  if (!nickname) return alert("닉네임을 입력하세요")

  localStorage.setItem("nickname", nickname)
  localStorage.setItem("channel", channel)

  location.href = "chat_room.html"
}
```

---

## 10. localStorage를 사용하는 이유

`chat_index.html`에서 입력한 닉네임과 채널 정보를 `chat_room.html`에서도 사용해야 한다.  
페이지가 이동되면 JavaScript 변수는 사라지기 때문에, 브라우저 저장소인 `localStorage`에 값을 저장한다.

```js
localStorage.setItem("nickname", nickname)
localStorage.setItem("channel", channel)
```

채팅방 페이지에서는 다시 꺼내서 사용한다.

```js
const nickname = localStorage.getItem("nickname")
let currentChannel = localStorage.getItem("channel")
```

값이 없으면 입장 화면으로 되돌린다.

```js
if (!nickname || !currentChannel) {
  alert("닉네임 또는 채널 정보가 없습니다.")
  location.href = "chat_index.html"
}
```

---

## 11. 채팅방 화면 구조

`chat_room.html`은 메시지 영역, 입력 영역, 채널 선택, 접속자 목록 영역으로 구성되어 있다.

```html
<div id="chat">
  <h3 id="channelName"></h3>

  <div class="chat-container">
    <div class="chat-main">
      <div id="messages"></div>

      <div>
        <input type="text" id="to" placeholder="귓속말 대상(없으면 전체)">
        <input type="text" id="message" placeholder="메시지를 입력하세요">

        <select id="channelSelector">
          <option value="lobby">대기실</option>
          <option value="sports">스포츠</option>
          <option value="programming">프로그래밍</option>
          <option value="music">음악</option>
        </select>

        <button id="emoji">😀</button>
        <button id="send">전송</button>
      </div>
    </div>

    <div id="users">
      <h4>접속자 목록</h4>
      <div id="userCounts"></div>
      <div id="userList"></div>
    </div>
  </div>
</div>
```

| 요소 | 역할 |
| --- | --- |
| `#channelName` | 현재 채널 이름 출력 |
| `#messages` | 채팅 메시지 출력 |
| `#to` | 귓속말 대상 입력 |
| `#message` | 채팅 메시지 입력 |
| `#channelSelector` | 채널 변경 |
| `#userCounts` | 접속자 수 표시 영역 |
| `#userList` | 접속자 목록 표시 영역 |

---

## 12. 클라이언트에서 Socket.IO 연결하기

Socket.IO를 사용하려면 클라이언트 HTML에서 다음 스크립트를 불러온다.

```html
<script src="/socket.io/socket.io.js"></script>
```

이 파일은 직접 만든 파일이 아니라 Socket.IO 서버가 자동으로 제공하는 클라이언트 라이브러리다.

그 다음 `io()`를 호출해 서버와 연결한다.

```js
const socket = io()
console.log("클라이언트 소켓 생성 성공!")
```

연결이 성공하면 서버에서는 `connection` 이벤트가 발생한다.

---

## 13. 서버에서 연결 감지하기

```js
const users = {}

io.on("connection", (socket) => {
  console.log("사용자가 연결되었음")
})
```

`connection` 이벤트는 클라이언트가 Socket.IO 서버에 접속했을 때 실행된다.

여기서 `socket`은 접속한 사용자 한 명과의 연결을 나타낸다.

```text
사용자 A 접속 → socket A 생성
사용자 B 접속 → socket B 생성
사용자 C 접속 → socket C 생성
```

각 소켓은 고유한 `socket.id`를 가진다.

---

## 14. join 이벤트

클라이언트가 채팅방에 들어오면 서버에 `join` 이벤트를 보낸다.

```js
socket.emit("join", {
  nickname,
  channel: currentChannel,
})
```

서버는 `join` 이벤트를 받아 사용자 정보를 저장하고 채널에 입장시킨다.

```js
socket.on("join", ({ nickname, channel }) => {
  socket.nickname = nickname
  socket.channel = channel

  users[socket.id] = { nickname, channel }

  socket.join(channel)

  const msg = {
    user: "system",
    text: `${nickname}님이 입장했습니다.`,
  }

  console.log("nickname:", nickname, "channel: ", channel)
  io.emit("message", msg)
})
```

---

## 15. socket에 값 저장하기

```js
socket.nickname = nickname
socket.channel = channel
```

`socket` 객체에 닉네임과 채널 정보를 직접 저장한다.  
이렇게 해두면 나중에 채팅 메시지를 보낼 때 누가 보냈는지, 어느 채널에 있는지 확인할 수 있다.

또한 전체 사용자 목록을 관리하기 위해 `users` 객체에도 저장한다.

```js
users[socket.id] = { nickname, channel }
```

예시는 다음과 같다.

```js
{
  "소켓ID1": { nickname: "김사과", channel: "lobby" },
  "소켓ID2": { nickname: "반하나", channel: "music" }
}
```

---

## 16. Room과 Channel

Socket.IO의 Room은 특정 소켓들을 묶어놓는 그룹이다.  
채팅 앱에서는 Room을 채널처럼 사용할 수 있다.

```js
socket.join(channel)
```

예를 들어 사용자가 `music` 채널을 선택하면 `music`이라는 Room에 들어간다.

```text
lobby Room
├── 사용자 A
└── 사용자 B

music Room
└── 사용자 C
```

특정 Room에만 메시지를 보내려면 다음처럼 작성한다.

```js
io.to("music").emit("message", {
  user: "system",
  text: "music 채널 공지",
})
```

---

## 17. 메시지 보내기

클라이언트에서 전송 버튼을 누르거나 Enter를 누르면 `chat` 이벤트를 서버로 보낸다.

```js
const messageInput = document.getElementById("message")

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage()
})

document.getElementById("send").onclick = sendMessage

function sendMessage() {
  const text = messageInput.value.trim()
  const to = toInput.value.trim()

  if (text) {
    socket.emit("chat", { text, to: to || null })
    messageInput.value = ""
  }
}
```

`socket.emit("chat", data)`는 서버에게 `chat` 이벤트를 보내는 코드다.

```text
클라이언트 → 서버
chat 이벤트 발생
{ text: "안녕하세요", to: null }
```

---

## 18. 서버에서 chat 이벤트 처리하기

```js
socket.on("chat", ({ text, to }) => {
  const sender = users[socket.id]

  if (!sender) return

  const payload = {
    user: sender.nickname,
    text,
  }

  if (to) {
    const receiverSocket = Object.entries(users).find(
      ([id, user]) => user.nickname === to
    )?.[0]

    if (receiverSocket) {
      io.to(receiverSocket).emit("whisper", payload)
      socket.emit("whisper", payload)
    }
  } else {
    io.to(sender.channel).emit("message", payload)
  }
})
```

메시지 처리 흐름은 다음과 같다.

```text
chat 이벤트 수신
  ↓
socket.id로 보낸 사람 정보 찾기
  ↓
귓속말 대상이 있나?
  ├── 있다 → 해당 사용자에게 whisper 이벤트 전송
  └── 없다 → 현재 채널 전체에 message 이벤트 전송
```

---

## 19. 전체 메시지와 귓속말

전체 메시지는 현재 채널에 있는 사용자에게만 보낸다.

```js
io.to(sender.channel).emit("message", payload)
```

귓속말은 특정 소켓에게만 보낸다.

```js
io.to(receiverSocket).emit("whisper", payload)
```

귓속말을 보낸 사람도 자기 화면에서 확인할 수 있도록 자신에게도 보낸다.

```js
socket.emit("whisper", payload)
```

---

## 20. 메시지 출력하기

서버에서 `message` 이벤트가 오면 클라이언트는 메시지를 화면에 추가한다.

```js
const messages = document.getElementById("messages")

socket.on("message", ({ user, text }) => {
  const div = document.createElement("div")
  div.textContent = `[${user}] ${text}`

  if (user === "system") {
    div.className = "system-msg"
  }

  messages.appendChild(div)
  messages.scrollTop = messages.scrollHeight
})
```

`messages.scrollTop = messages.scrollHeight`는 새 메시지가 추가될 때 스크롤을 아래로 내리는 코드다.

---

## 21. 귓속말 출력하기

서버에서 `whisper` 이벤트가 오면 귓속말 형식으로 출력한다.

```js
socket.on("whisper", ({ user, text }) => {
  const div = document.createElement("div")
  div.textContent = `(귓속말) [${user}] ${text}`
  div.style.color = "deeppink"

  messages.appendChild(div)
  messages.scrollTop = messages.scrollHeight
})
```

전체 메시지와 구분하기 위해 색상을 다르게 지정한다.

---

## 22. 채널 변경

채널 선택 값이 바뀌면 클라이언트는 서버에 `changeChannel` 이벤트를 보낸다.

```js
channelSelector.onchange = () => {
  const newChannel = channelSelector.value

  if (newChannel !== currentChannel) {
    socket.emit("changeChannel", { newChannel })

    currentChannel = newChannel
    channelName.textContent = `[채널: ${currentChannel}]`
    messageInput.value = ""
    localStorage.setItem("channel", currentChannel)
  }
}
```

서버에서는 기존 채널에서 나가고 새 채널에 들어가게 처리한다.

```js
socket.on("changeChannel", ({ newChannel }) => {
  const oldChannel = socket.channel
  const nickname = socket.nickname

  socket.leave(oldChannel)

  io.to(oldChannel).emit("message", {
    user: "system",
    text: `${nickname}님이 ${newChannel} 채널로 이동했습니다.`,
  })

  socket.join(newChannel)

  socket.channel = newChannel
  users[socket.id].channel = newChannel

  const joinMsg = {
    user: "system",
    text: `${nickname}님이 입장했습니다.`,
  }

  io.to(newChannel).emit("message", joinMsg)
})
```

---

## 23. `socket.leave()`

```js
socket.leave(oldChannel)
```

현재 소켓을 기존 Room에서 제거한다.  
채널 이동 기능에서는 이전 채널 메시지를 더 이상 받지 않게 하기 위해 필요하다.

---

## 24. disconnect 이벤트

사용자가 브라우저를 닫거나 새로고침하거나 연결이 끊어지면 `disconnect` 이벤트가 발생한다.

```js
socket.on("disconnect", () => {
  console.log("사용자가 퇴장했습니다.")
})
```

실제 채팅 앱에서는 연결이 끊겼을 때 사용자 목록에서도 제거하는 것이 좋다.

```js
socket.on("disconnect", () => {
  const user = users[socket.id]

  if (user) {
    io.to(user.channel).emit("message", {
      user: "system",
      text: `${user.nickname}님이 퇴장했습니다.`,
    })

    delete users[socket.id]
  }
})
```

---

## 25. 이벤트 흐름 정리

| 이벤트 이름 | 방향 | 역할 |
| --- | --- | --- |
| `connection` | 클라이언트 → 서버 | 소켓 연결 감지 |
| `join` | 클라이언트 → 서버 | 닉네임과 채널 정보 전달 |
| `chat` | 클라이언트 → 서버 | 채팅 메시지 전송 |
| `message` | 서버 → 클라이언트 | 일반 메시지 수신 |
| `whisper` | 서버 → 클라이언트 | 귓속말 메시지 수신 |
| `changeChannel` | 클라이언트 → 서버 | 채널 변경 요청 |
| `disconnect` | 클라이언트 연결 종료 | 접속 종료 처리 |

---

## 26. 서버 전체 흐름

```text
서버 실행
  ↓
public 폴더 정적 파일 제공
  ↓
클라이언트가 chat_index.html 접속
  ↓
닉네임, 채널 선택
  ↓
chat_room.html 이동
  ↓
Socket.IO 연결
  ↓
join 이벤트 발생
  ↓
채팅 메시지 송수신
  ↓
채널 변경 또는 연결 종료
```

---

## 27. 코드에서 주의할 점

현재 예제는 학습용 흐름을 보여주는 코드라 몇 가지 수정하면 더 안정적으로 동작한다.

### 1. 사용하지 않는 import 제거

```js
import { Socket } from "dgram"
```

위 코드는 현재 사용되지 않는다.  
Socket.IO의 `socket`과도 관계가 없으므로 제거하는 것이 좋다.

---

### 2. `chat` 이벤트에서 `to`도 받아야 한다

서버 코드에서 귓속말 대상을 사용하려면 구조 분해 할당에 `to`를 포함해야 한다.

```js
socket.on("chat", ({ text, to }) => {
  // ...
})
```

`({ text })`만 받으면 `to` 변수를 사용할 수 없다.

---

### 3. 클라이언트의 `nill` 오타 수정

현재 클라이언트 코드에 다음과 같은 부분이 있다.

```js
socket.emit("chat", { text, to: to || nill })
```

JavaScript에는 `nill`이라는 값이 없다.  
없음을 표현하려면 `null`을 사용해야 한다.

```js
socket.emit("chat", { text, to: to || null })
```

---

### 4. 귓속말 emit 코드 수정

다음 코드는 문법이 잘못되어 있다.

```js
io.to(receiverSocket),emit("whisper", payload)
```

다음처럼 작성해야 한다.

```js
io.to(receiverSocket).emit("whisper", payload)
```

---

### 5. 채널 이동 메시지의 템플릿 문자열 수정

다음 코드는 `{newChannel}`이 문자열 그대로 출력된다.

```js
text: `${nickname}님이 {newChannel} 채널로 이동했습니다.`
```

변수 값을 넣으려면 `${newChannel}`로 작성해야 한다.

```js
text: `${nickname}님이 ${newChannel} 채널로 이동했습니다.`
```

---

### 6. 채널 이동 시 새 채널에 join 해야 한다

기존 채널에서 나간 뒤 새 채널에 들어가야 한다.

```js
socket.leave(oldChannel)
socket.join(newChannel)
```

`socket.join(newChannel)`이 없으면 새 채널 Room에 실제로 들어가지 못한다.

---

### 7. 입장 메시지는 해당 채널에만 보내는 것이 자연스럽다

현재 코드에서는 입장 메시지를 모든 사용자에게 보낸다.

```js
io.emit("message", msg)
```

채널 채팅이라면 해당 채널에만 보내는 것이 더 자연스럽다.

```js
io.to(channel).emit("message", msg)
```

---

### 8. 접속 종료 시 users에서 삭제해야 한다

연결이 끊어진 사용자를 `users` 객체에서 삭제하지 않으면 실제 접속자가 아닌 사용자 정보가 남을 수 있다.

```js
delete users[socket.id]
```

---

## 28. 수정한 서버 코드 예시

아래 코드는 현재 예제의 흐름을 유지하면서 주요 오타를 정리한 버전이다.

```js
import express from "express"
import { Server } from "socket.io"
import { createServer } from "http"
import path from "path"
import { fileURLToPath } from "url"

const app = express()
const server = createServer(app)
const io = new Server(server)

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

app.use(express.static(path.join(__dirname, "public")))

const users = {}

io.on("connection", (socket) => {
  console.log("사용자가 연결되었음")

  socket.on("join", ({ nickname, channel }) => {
    socket.nickname = nickname
    socket.channel = channel
    users[socket.id] = { nickname, channel }

    socket.join(channel)

    io.to(channel).emit("message", {
      user: "system",
      text: `${nickname}님이 입장했습니다.`,
    })
  })

  socket.on("chat", ({ text, to }) => {
    const sender = users[socket.id]

    if (!sender) return

    const payload = {
      user: sender.nickname,
      text,
    }

    if (to) {
      const receiverSocket = Object.entries(users).find(
        ([id, user]) => user.nickname === to
      )?.[0]

      if (receiverSocket) {
        io.to(receiverSocket).emit("whisper", payload)
        socket.emit("whisper", payload)
      }

      return
    }

    io.to(sender.channel).emit("message", payload)
  })

  socket.on("changeChannel", ({ newChannel }) => {
    const oldChannel = socket.channel
    const nickname = socket.nickname

    socket.leave(oldChannel)

    io.to(oldChannel).emit("message", {
      user: "system",
      text: `${nickname}님이 ${newChannel} 채널로 이동했습니다.`,
    })

    socket.join(newChannel)

    socket.channel = newChannel
    users[socket.id].channel = newChannel

    io.to(newChannel).emit("message", {
      user: "system",
      text: `${nickname}님이 입장했습니다.`,
    })
  })

  socket.on("disconnect", () => {
    const user = users[socket.id]

    if (user) {
      io.to(user.channel).emit("message", {
        user: "system",
        text: `${user.nickname}님이 퇴장했습니다.`,
      })

      delete users[socket.id]
    }

    console.log("사용자가 퇴장했습니다.")
  })
})

server.listen(3000, () => {
  console.log("서버 실행 중...")
})
```

---

## 29. 실행 방법

필요한 패키지를 설치한다.

```bash
npm install express socket.io
```

서버를 실행한다.

```bash
node 12_SocketIO.mjs
```

브라우저에서 채팅 입장 화면으로 접속한다.

```text
http://localhost:3000/chat_index.html
```

채팅 기능을 테스트하려면 브라우저 탭을 2개 이상 열어 서로 다른 닉네임으로 입장하면 된다.

```text
탭 1: 김사과 / lobby
탭 2: 반하나 / lobby
```

한쪽에서 메시지를 보내면 같은 채널에 있는 다른 탭에서도 메시지가 보인다.

---

## 30. 정리

Socket.IO는 서버와 클라이언트가 연결을 유지하면서 이벤트를 주고받을 수 있게 해준다.  
일반적인 HTTP 요청/응답 방식과 달리 서버가 클라이언트에게 먼저 메시지를 보낼 수 있어 채팅, 알림, 실시간 대시보드 같은 기능에 적합하다.

이번 채팅 예제의 핵심 흐름은 다음과 같다.

```text
닉네임과 채널 선택
  ↓
localStorage에 저장
  ↓
Socket.IO 연결
  ↓
join 이벤트로 채널 입장
  ↓
chat 이벤트로 메시지 전송
  ↓
message 이벤트로 채널 사용자에게 전달
  ↓
changeChannel 이벤트로 채널 이동
  ↓
disconnect 이벤트로 퇴장 처리
```

Socket.IO에서 중요한 개념은 `emit`, `on`, `socket`, `io`, `Room`이다.  
이 다섯 가지를 이해하면 실시간 채팅뿐 아니라 알림, 접속자 목록, 귓속말, 채널 분리 같은 기능도 확장할 수 있다.
