import { Navigate, Outlet, Route, Routes } from "react-router-dom"
import LoginPage from "./pages/LoginPage.jsx"
import SignupPage from "./pages/SignupPage.jsx"
import HotelListPage from "./pages/HotelListPage.jsx"
import HotelDetailPage from "./pages/HotelDetailPage.jsx"
import AdminPage from "./pages/AdminPage.jsx"

function AdminRoute() {
  const user = JSON.parse(localStorage.getItem("user") || "null")
  return user?.role === "ADMIN" ? <Outlet /> : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/hotels" element={<HotelListPage />} />
      <Route path="/hotels/:hotelId" element={<HotelDetailPage />} />
      <Route element={<AdminRoute />}><Route path="/admin" element={<AdminPage />} /></Route>
      {/* 첫 접속은 로그인 화면으로 안내합니다. 호텔 목록은 다음 단계에서 연결합니다. */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}
