import express from "express"
import cors from "cors"
import authRouter from "./routes/auth.routes.js"
import hotelRouter from "./routes/hotel.routes.js"
import adminRouter from "./routes/admin.routes.js"

const app = express()

// Vite가 기본 포트(5173)를 이미 사용 중이면 5174 등 다른 포트로 실행될 수 있습니다.
// 개발 중 사용하는 프론트 주소들을 모두 허용해 브라우저의 CORS 차단을 막습니다.
const allowedOrigins = ["http://localhost:5174"]

app.use(
  cors({
    origin(origin, callback) {
      // Postman 같은 브라우저 밖 도구는 Origin 헤더가 없으므로 허용합니다.
      if (!origin || allowedOrigins.includes(origin)) {
        return callback(null, true)
      }

      return callback(new Error("허용되지 않은 출처입니다."))
    },
  })
)
app.use(express.json())

app.get("/api/health", (req, res) => {
  res.status(200).json({ success: true, data: { status: "ok" } })
})

app.use("/api/auth", authRouter)
app.use("/api/hotels", hotelRouter)
app.use("/api/admin", adminRouter)

// 등록되지 않은 URL도 JSON 형식으로 반환합니다.
app.use((req, res) => {
  res.status(404).json({ success: false, message: "요청한 API를 찾을 수 없습니다." })
})

// 컨트롤러에서 next(error)로 전달한 예외를 한 곳에서 처리합니다.
app.use((error, req, res, next) => {
  console.error(error)
  res.status(error.status || 500).json({
    success: false,
    message: error.message || "서버 오류가 발생했습니다.",
  })
})

export default app
