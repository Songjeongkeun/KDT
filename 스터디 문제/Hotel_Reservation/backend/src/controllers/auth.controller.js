import User from "../models/User.js"
import { createAccessToken } from "../utils/token.js"

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function userResponse(user) {
  return {
    id: user._id,
    email: user.email,
    nickname: user.nickname,
    role: user.role,
  }
}

export async function checkEmail(req, res, next) {
  try {
    const email = req.body.email?.trim().toLowerCase()

    if (!emailPattern.test(email || "")) {
      return res.status(400).json({ success: false, message: "올바른 이메일 형식이 아닙니다." })
    }

    const user = await User.findOne({ email })
    return res.status(200).json({
      success: true,
      data: { available: !user },
      message: user ? "이미 사용 중인 이메일입니다." : "사용 가능한 이메일입니다.",
    })
  } catch (error) {
    next(error)
  }
}

export async function signup(req, res, next) {
  try {
    const { email, nickname, password, passwordConfirm } = req.body

    if (!email || !nickname || !password || !passwordConfirm) {
      return res.status(400).json({ success: false, message: "모든 항목을 입력해 주세요." })
    }

    if (!emailPattern.test(email)) {
      return res.status(400).json({ success: false, message: "올바른 이메일 형식이 아닙니다." })
    }

    if (password.length < 8) {
      return res.status(400).json({ success: false, message: "비밀번호는 8자 이상이어야 합니다." })
    }

    if (password !== passwordConfirm) {
      return res.status(400).json({ success: false, message: "비밀번호 확인이 일치하지 않습니다." })
    }

    const normalizedEmail = email.trim().toLowerCase()
    const exists = await User.findOne({ email: normalizedEmail })

    if (exists) {
      return res.status(409).json({ success: false, message: "이미 사용 중인 이메일입니다." })
    }

    const user = await User.create({ email: normalizedEmail, nickname, password })
    const token = createAccessToken(user._id.toString())

    return res.status(201).json({
      success: true,
      data: { user: userResponse(user), token },
      message: "회원가입이 완료되었습니다.",
    })
  } catch (error) {
    // unique 제약조건이 동시에 요청된 경우도 처리합니다.
    if (error.code === 11000) {
      return res.status(409).json({ success: false, message: "이미 사용 중인 이메일입니다." })
    }
    next(error)
  }
}

export async function login(req, res, next) {
  try {
    const { email, password } = req.body

    if (!email || !password) {
      return res.status(400).json({ success: false, message: "이메일과 비밀번호를 입력해 주세요." })
    }

    const user = await User.findOne({ email: email.trim().toLowerCase() })

    if (!user || !(await user.comparePassword(password))) {
      return res.status(401).json({ success: false, message: "이메일 또는 비밀번호가 올바르지 않습니다." })
    }

    const token = createAccessToken(user._id.toString())
    return res.status(200).json({
      success: true,
      data: { user: userResponse(user), token },
      message: "로그인되었습니다.",
    })
  } catch (error) {
    next(error)
  }
}
