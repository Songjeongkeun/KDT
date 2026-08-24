import { useState } from "react"
import { useNavigate } from "react-router-dom"
import AuthLayout from "../components/AuthLayout.jsx"
import { request } from "../services/api.js"

const initialForm = { email: "", password: "" }

export default function LoginPage() {
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const navigate = useNavigate()

  function handleChange(event) {
    const { name, value } = event.target
    setForm((previous) => ({ ...previous, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError("")

    if (!form.email || !form.password) {
      setError("이메일과 비밀번호를 모두 입력해 주세요.")
      return
    }

    try {
      setIsSubmitting(true)
      const result = await request("/auth/login", {
        method: "POST",
        body: JSON.stringify(form),
      })

      // 이후 예약/후기 같은 인증 API를 호출할 때 사용할 토큰입니다.
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
      title="다시 만나서 반가워요"
      description="StayHub 계정으로 여행을 이어가세요."
      footerText="아직 회원이 아니신가요?"
      footerLink="/signup"
      footerLinkText="회원가입"
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate>
        <label>
          이메일
          <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="stayhub@example.com" autoComplete="email" />
        </label>
        <label>
          비밀번호
          <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="비밀번호를 입력하세요" autoComplete="current-password" />
        </label>
        {error && <p className="form-error" role="alert">{error}</p>}
        <button className="primary-button" disabled={isSubmitting}>
          {isSubmitting ? "로그인 중..." : "로그인"}
        </button>
      </form>
    </AuthLayout>
  )
}
