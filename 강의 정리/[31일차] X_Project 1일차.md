# [31일차] X_Project 1일차 정리

X_Project : Node.js 기반 Express 서버에서 회원가입, 로그인, JWT 인증, MongoDB 연결, 환경변수 관리를 학습하기 위한 예제 프로젝트

전체 코드 주소 : https://github.com/Songjeongkeun/Server

## 1. 프로젝트 전체 구조

```tex
Server/
├── app.mjs
├── config.mjs
├── db/
│   └── database.mjs
├── router/
│   ├── auth.mjs
│   └── posts.mjs
├── controller/
│   └── auth.mjs
├── data/
│   └── auth.mjs
├── middleware/
│   └── auth.mjs
├── memo.txt
├── package.json
└── .env
```

**각 폴더의 역할**

| 위치              | 역할                                                         |
| ----------------- | ------------------------------------------------------------ |
| `app.mjs`         | 서버의 시작점이다. Express 앱 생성, 미들웨어 등록, 라우터 등록, DB 연결, 서버 실행을 담당한다. |
| `config.mjs`      | 환경변수를 읽고 서버 설정 객체로 정리한다.                   |
| `db/database.mjs` | MongoDB 연결과 컬렉션 접근 함수를 제공한다.                  |
| `router/`         | URL 경로와 HTTP 메서드를 컨트롤러 함수에 연결한다.           |
| `controller/`     | 요청과 응답을 처리하는 실제 비즈니스 로직을 담는다.          |
| `data/`           | DB에 접근하는 함수들을 모아둔다. Repository 계층에 가깝다.   |
| `middleware/`     | 요청 처리 중간에 실행되는 공통 로직을 담는다. 인증 검사 등이 들어간다. |
| `memo.txt`        | 환경변수와 dotenv에 대한 수업 메모가 들어 있다.              |



## 2. Express 서버 실행 흐름

`app.mjs` 는 서버의 시작 위치이다.

```js
const app = express()

app.use(express.json())
app.use("/auth", authRouter)
app.use("/post", postsRouter)
```

여기서 중요한 부분은 `app.use(express.json())` 이다. 클라이언트가 JSON 형태로 보낸 요청 body를 JavaScript 객체로 변환해 주기 때문에, 컨트롤러에서 `req.body.userid`, `req.body.password` 처럼 값을 꺼낼 수 있다.
라우터 등록은 다음처럼 동작한다.

| 등록 코드                       | URL 예시                                  |
| ------------------------------- | ----------------------------------------- |
| `app.use("/auth", authRouter)`  | `/auth/signup`, `/auth/login`, `/auth/me` |
| `app.use("/post", postsRouter)` | `/post/...`                               |

마지막에는 404 처리 미들웨어가 있다.

```js
app.use((req, res) => {
  res.sendStatus(404)
})
```

위에 등록된 라우터 중 어떤 경로와도 일치하지 않으면 404 응답을 보낸다.

서버는 DB 연결이 성공한 뒤에 실행된다.

```js
connectDB().then(() => {
  app.listen(config.host.port, () => {
    console.log("DB/웹 서버 실행 중...")
  })
}).catch(console.error)
```

이렇게 코드를 작성하면, DB 연결 실패 상태에서 서버만 먼저 열리는 문제를 줄일 수 있다. 서버가 요청을 받기 전에 MongoDB 연결을 먼저 보장한다.



## 3. 환경변수와 dotenv

환경변수는 코드 밖에서 프로그램 설정값을 주입하는 방식이다. 특정 값들은 코드에 직접 적지 않는 것이 좋다.

- JWT 비밀키
- 데이터베이스 주소와 비밀번호
- 서버 포트
- API 키
- Bcrypt salt rounds 같은 암호화 설정

`dotenv`는 `.env` 파일에 적어둔 값을 Node.js 의 `process.env` 로 불러오는 라이브러리이다.

```js
import dotenv from "dotenv"

dotenv.config()
```

`.env` 파일에 있는 값은 다음처럼 접근할 수 있다.

```js
process.env.JWT_SECRET
process.env.HOST_PORT
```

프로젝트에서는 `config.mjs` 가 환경변수를 한 번에 읽어서 `config` 객체로 내보낸다.

```js
export const config = {
  jwt: {
        secretKey: required("JWT_SECRET"),
        expiresInSec: parseInt(required("JWT_EXPIRES_SEC"))
    },
    bcrypt: {
        saltRounds: parseInt(required("BCRYPT_SALT_ROUNDS", 10))
    },
    host: {
        port: parseInt(required("HOST_PORT", 8080))
    },
    db: {
        host: required("DB_HOST")
    }
}
```

이렇게 하면 코드에서 `process.env` 를 직접 쓰지 않고 `config.jwt.secretKey`, `config.db.host` 처럼 의미 있는 이름으로 사용할 수 있다.



## 4. required 함수의 의미

```js
function required(key, defaultValue=undefined){
  const value = process.env[key] || defaultValue
  if(value == null){
    throw new Error(`키 ${key}는 undefined`)
  }
  return value
}
```

이 함수의 목적은 필수 설정값이 빠져 있을 때 서버를 잘못 실행하지 않도록 바로 에러를 내는 것이다.

예를 들어 `JWT_SECRET` 이 없으면 JWT 토큰을 안전하게 만들 수 없다. 이때 서버거 애매하게 실행되는 것보다 시작 단계에서 에러가 나는 편이 문제를 더 빨리 찾을 수 있다.



## 5. MongoDB 연결 구조

`db/database.mjs` 는 MongoDB 연결을 담당한다.

```js
let db

export async function connectDB(){
  return MongoDB.MongoClient.connect(config.db.host).then((client) => {
    db = client.db("Xdb")
  })
}
```

`db` 변수는 모듈 전체에서 공유된다. 서버 시작 시 `connectDB()` 가 실행되면 MongoDB 클라이언트를 만들고, `Xdb` 데이터베이스 객체를 `db` 에 저장한다.

컬렉션 접근 함수는 다음과 같다. 

```js
export function getUsers(){
  return db.collection("users")
}

export function getPosts(){
  return db.collection("posts")
}
```

이렇게 함수를 분리하면 다른 파일에서 MongoDB 연결 세부사항을 몰라도 된다. 예를 들어 사용자 관련 DB 작업은 `getUsers()` 만 호출하면 된다.



## 6. 라우터의 역할

라우터는 URL과 컨트롤러를 연결하는 계층이다. `router/auth.mjs` 에는 인증관련 API가 모여있다.

```js
router.post("/signup", authController.signup)
router.post("/login", authcontroller.login)
router.get("/me", isAuth, authController.me)
```

| API            | 메서드 | 역할             |
| -------------- | ------ | ---------------- |
| `/auth/signup` | POST   | 회원가입         |
| `/auth/login`  | POST   | 로그인           |
| `/auth/me`     | GET    | 로그인 유지 확인 |

`/auth/me` 에는 `isAuth` 미들웨어가 먼저 들어간다.

```js
router.get("/me", isAuth, authController.me)
```

이 코드의 의미는 클라이언트가 `/auth/me` 에 요청을 보내면 다음 순서로 처리된다는 것이다.

1. `isAuth` 가 먼저 실행된다.
2. 토큰이 유효한지 확인한다
3. 유효하면 `next()` 로 다음 함수에 넘긴다.
4. `authController.me` 가 실행된다.

>  1일차에서는 `isAuth` 를 완전히 구현하지 않았다.



## 7. Controller 계층

`controller/auth.mjs`는 실제 요청 처리 흐름을 담당한다.



### 7.1 회원가입

```js
export async function signup(req, res) {
    const { userid, password, name, email } = req.body
    // 회원 중복 체크
    const found = await authRepository.findByUserid(userid)
    if (found) {
        return res.status(409).json({ message: `${userid}이 이미 있습니다.` })
    }
    const hashed = bcrypt.hashSync(password, config.bcrypt.saltRounds)
    // 회원 가입
    const user = await authRepository.createUser({
        userid, password: hashed, name, email
    })
    const token = await createJwtToken(user.id)
    console.log(token)
    res.status(201).json({ token, user })
}
```

`signup` 함수는 다음 순서로 동작한다.

1. 요청 body에서 `userid`, `password`, `name`, `email` 을 꺼낸다.
2. 같은 `userid` 를 가진 사용자가 이미 있는지 확인한다.
3. 중복 사용자가 있으면 409 Conflict 를 응답한다.
4. 비밀번호를 bcrypt 로 해싱한다.
5. 사용자 정보를 DB 에 저장한다.
6. JWT 토큰을 만든다.
7. 토큰과 사용자 정보를 응답한다.

### 7.2 로그인

```js
export async function login(req, res) {
    const { userid, password } = req.body
    const user = await authRepository.findByUserid(userid)
    if(!user){
        return res.status(401).json({ message: "아이디 또는 비밀번호 확인"})
    }
    const isValidPassword = await bcrypt.compare(password, user.password)
    if(!isValidPassword){
            return res.status(401).json({ message: "아이디 또는 비밀번호 확인"})
    }
    const token = await createJwtToken(user.id)
    res.status(200).json({ token, user })
}
```

`login` 함수는 다음 순서로 동작한다.

1. 요청 body 에서 `userid`, `password` 를 꺼낸다.
2. DB에서 해당 `userid` 의 사용자를 찾는다.
3. 사용자가 없으면 401 Unauthorized를 응답한다.
4. Bcrypt로 입력 비밀번호와 저장된 해신 비밀번호를 비교한다.
5. 비밀번호가 틀리면 401 Unauthorized를 응답한다.
6. 로그인 성공 시 JWT 토큰을 발급한다.
7. 토큰과 사용자 정보를 응답한다.

로그인 실패 시 "아이디가 틀림" 과 "비밀번호가 틀림"을 구체적으로 나누지 않는 것이 보안상 더 좋다. 



## 8. Repository 계층

`data/auth.mjs` 는 사용자 데이터에 접근하는 함수들을 모아둔 파일이다.

```js
export async function findByUserid(userid){
  return getUsers().find({ userid }).next().then(mapOptionalUser)
}
```

`find({ userid}).next()`는 조건에 맞는 첫 번째 문서를 가져온다. 가져온 MongoDB 문서는 `_id` 필드를 가지고 있는데, JavaScript에서 다루기 쉽게 `id` 문자열 필드를 추가한다. 

```js
function mapOptionalUser(user){
  return user ? { ...user, id: user._id.toString() } : user
}
```

이 함수는 MongoDB에서 가져온 user 데이터가 있으면 복사해서 가공해서 반환하고, 없으면 그대로 반환한다.

```js
export async function findById(id){
	return getUsers().find({ _id: new ObjectId(id) }).next().then(mapOptionalUser)
}
```

`findById` 는 문자열 id를 MongoDB의 ObjectId 로 변환해서 찾는다.

MongoDb의 `_id` 는 일반 문자열이 아니라 `ObjectId` 타입이다. 그래서 URL 이나 JWT에서 받은 문자열 id를 그대로 비교하면 찾지 못할 수 있다. 반드시 `new ObjectId(id)` 로 변환해야 한다. 



## 9. bcrypt로 비밀번호 보호하기

비밀번호는 절대 원문 그대로 DB에 저장하면 안 된다. 프로젝터에서는 `bcrypt` 를 사용한다.

회원가입에서는 비밀번호를 해싱한다.

```js
const hashed = bcrypt.hashSync(password, config.bcrypt.saltRounds)
```

로그인에서는 입력한 비밀번호와 DB에 저장된 해시값을 비교한다.

```js
const isValidPassword = await bcrypt.compare(password, user.password)
```

해싱은 암호화와 다르다. 암호화는 복호화가 가능하지만, 해싱은 원래 값으로 되돌릴 수 없도록 설계된다. 로그인할 때도 DB의 해시를 원문으로 되돌리는 것이 아니라, 입력값을 같은 방식으로 검증해서 일치 여부만 확인하다.

`BCRYPT_SALT_ROUNDS` 는 해싱을 얼마나 복잡하게 할지 정하는 값이다. 값이 높을수록 보안이 강해지지만 처리 속도는 느려진다. 



## 10. JWT 인증 흐름

JWT는 로그인 성공 후 서버가 클라이언트에게 발급하는 토큰이다.

**토큰 생성 함수**

```js
async function createJwtToken(id){
  return jwt.sign({ id }, config.jwt.secretKey, {
  	expiresIn: config.jwt.expiresInSec
  })
}
```

토큰 안에는 `{ id }` 가 payload 로 들어간다. 서버는 나중에 이 토큰을 검증해서 "어떤 사용자의 요청인지" 확인할 수 있다.

일반적인 JWT 인증 흐름은 다음과 같다.

1. 사용자가 로그인한다.
2. 서버가 사용자 id를 담은 JWT를 발급한다.
3. 클라이언트가 토큰을 저장한다
4. 인증이 필요한 API 요청 시 `Authorization` 헤더에 토큰을 넣어 보낸다.
5. 서버의 인증 미들웨어가 토큰을 검증한다.
6. 검증 성공 시 요청 객체에 사용자 정보를 담고 다음 로직으로 넘긴다.

Authorization 헤더는 보통 다음 형태를 사용한다.

```tex
Authorization: Bearer 토큰값
```



## 11. 프로젝트 1일차 요청 흐름

**회원가입 요청 흐름**

```tex
Client
  -> POST /auth/signup
  -> app.mjs
  -> router/auth.mjs
  -> controller/auth.mjs signup()
  -> data/auth.mjs findByUserid()
  -> bcrypt.hashSync()
  -> data/auth.mjs createUser()
  -> jwt.sign()
  -> JSON 응답
```

**로그인 요청 흐름**

```tex
Client
  -> POST /auth/login
  -> router/auth.mjs
  -> controller/auth.mjs login()
  -> data/auth.mjs findByUserid()
  -> bcrypt.compare()
  -> jwt.sign()
  -> JSON 응답
```

