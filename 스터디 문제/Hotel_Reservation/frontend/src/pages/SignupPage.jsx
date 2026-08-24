import { useState } from "react"
import { useNavigate } from "react-router-dom"
import AuthLayout from "../components/AuthLayout.jsx"
import { request } from "../services/api.js"

const initialForm = { email: "", nickname: "", password: "", passwordConfirm: "" }
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function SignupPage() {
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const navigate = useNavigate()

  function handleChange(event) {
    const { name, value } = event.target
    setForm((previous) => ({ ...previous, [name]: value }))
  }

  function validateForm() {
    if (!emailPattern.test(form.email)) return "올바른 이메일 주소를 입력해 주세요."
    if (form.nickname.trim().length < 2) return "닉네임은 2자 이상 입력해 주세요."
    if (form.password.length < 8) return "비밀번호는 8자 이상 입력해 주세요."
    if (form.password !== form.passwordConfirm) return "비밀번호 확인이 일치하지 않습니다."
    return ""
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const validationError = validateForm()
    setError(validationError)
    if (validationError) return

    try {
      setIsSubmitting(true)
      const result = await request("/auth/signup", {
        method: "POST",
        body: JSON.stringify(form),
      })

      // 회원가입 직후 받은 토큰으로 바로 로그인된 상태를 만듭니다.
      localStorage.setItem("accessToken", result.data.token)
      localStorage.setItem("user", JSON.stringify(result.data.user))
      navigate("/hotels")
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthLayout
      title="StayHub 시작하기"
      description="간단한 정보 입력 후 여행을 준비해 보세요."
      footerText="이미 계정이 있으신가요?"
      footerLink="/login"
      footerLinkText="로그인"
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate>
        <label>이메일<input name="email" type="email" value={form.email} onChange={handleChange} placeholder="stayhub@example.com" autoComplete="email" /></label>
        <label>닉네임<input name="nickname" value={form.nickname} onChange={handleChange} placeholder="2자 이상 입력" autoComplete="nickname" /></label>
        <label>비밀번호<input name="password" type="password" value={form.password} onChange={handleChange} placeholder="8자 이상 입력" autoComplete="new-password" /></label>
        <label>비밀번호 확인<input name="passwordConfirm" type="password" value={form.passwordConfirm} onChange={handleChange} placeholder="비밀번호를 다시 입력하세요" autoComplete="new-password" /></label>
        {error && <p className="form-error" role="alert">{error}</p>}
        <button className="primary-button" disabled={isSubmitting}>{isSubmitting ? "가입 처리 중..." : "회원가입"}</button>
      </form>
    </AuthLayout>
  )
}
