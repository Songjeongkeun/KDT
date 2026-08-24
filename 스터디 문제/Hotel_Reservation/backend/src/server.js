import "dotenv/config"
import app from "./app.js"
import { connectDatabase } from "./config/db.js"

// 5000번 포트는 다른 로컬 프로그램이 사용하는 경우가 많아 5001을 기본값으로 둡니다.
const port = process.env.PORT || 5001

async function startServer() {
  try {
    await connectDatabase()
    app.listen(port, () => console.log(`StayHub API: http://localhost:${port}`))
  } catch (error) {
    console.error("서버 시작 실패:", error.message)
    process.exit(1)
  }
}

startServer()
