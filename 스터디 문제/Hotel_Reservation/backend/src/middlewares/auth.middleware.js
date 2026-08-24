import jwt from "jsonwebtoken"
import User from "../models/User.js"

// 보호된 API에서 Authorization: Bearer <token>을 검증할 때 사용합니다.
export async function requireAuth(req, res, next) {
  try {
    const authorization = req.headers.authorization

    if (!authorization?.startsWith("Bearer ")) {
      return res.status(401).json({ success: false, message: "로그인이 필요합니다." })
    }

    const token = authorization.split(" ")[1]
    const { userId } = jwt.verify(token, process.env.JWT_SECRET)
    const user = await User.findById(userId).select("-password")

    if (!user) {
      return res.status(401).json({ success: false, message: "유효하지 않은 사용자입니다." })
    }

    // 이후 예약/후기 컨트롤러에서 req.user._id로 로그인 사용자를 알 수 있습니다.
    req.user = user
    next()
  } catch (error) {
    return res.status(401).json({ success: false, message: "유효하지 않거나 만료된 토큰입니다." })
  }
}

// requireAuth 다음에 연결합니다. 로그인 여부뿐 아니라 관리자 역할도 확인합니다.
export function requireAdmin(req, res, next) {
  if (req.user.role !== "ADMIN") {
    return res.status(403).json({ success: false, message: "관리자만 접근할 수 있습니다." })
  }

  next()
}

