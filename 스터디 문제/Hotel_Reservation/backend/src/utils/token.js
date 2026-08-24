import jwt from "jsonwebtoken"

// 토큰에는 민감한 정보 대신 사용자 ID만 저장합니다.
export function createAccessToken(userId) {
  return jwt.sign({ userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || "1d",
  })
}

