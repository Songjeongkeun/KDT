import mongoose from "mongoose"

// 서버가 시작될 때 한 번만 MongoDB에 연결합니다.
export async function connectDatabase() {
  const mongoUri = process.env.MONGO_URI

  if (!mongoUri) {
    throw new Error("MONGO_URI 환경 변수가 설정되지 않았습니다.")
  }

  await mongoose.connect(mongoUri)
  console.log("MongoDB connected")
}

