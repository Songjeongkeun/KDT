import jwt from "jsonwebtoken"

const secretKey = "!@#$%^&*()"


// 1. 토큰 생성
const token = jwt.sign(
    { userid: "apple", role: "admin" },
    secretKey,
    { expiresIn: "1h" }
)

console.log("생성된 토큰: ", token)

// 2. 토큰 검증
try {
    const decoded = jwt.verify(token, secretKey)
    console.log("검증된 트큰 내용: ", decoded)
} catch (error) {
    console.log("토큰 검증 실패: ", error.message)
}