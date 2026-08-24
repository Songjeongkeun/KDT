// Vite 개발 서버의 proxy가 /api 요청을 http://localhost:5001으로 전달합니다.
// 따라서 브라우저 관점에서는 같은 출처로 요청하게 되어 CORS 오류가 발생하지 않습니다.
const API_BASE_URL = "/api"

// fetch 요청과 공통 에러 처리를 한 곳에 모읍니다.
// 나중에 호텔, 예약 API도 이 함수를 그대로 사용합니다.
export async function request(path, options = {}) {
  const token = localStorage.getItem("accessToken")

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      // 토큰이 있을 때만 전송합니다. 로그인·회원가입 API에는 토큰이 없습니다.
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  const result = await response.json()

  if (!response.ok) {
    throw new Error(result.message || "요청 처리에 실패했습니다.")
  }

  return result
}
