import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import AdminHotelForm from "../components/admin/AdminHotelForm.jsx"
import AdminHotelList from "../components/admin/AdminHotelList.jsx"
import AdminRoomForm from "../components/admin/AdminRoomForm.jsx"
import AdminRoomList from "../components/admin/AdminRoomList.jsx"
import { request } from "../services/api.js"
import { emptyHotel, emptyRoom, toHotelForm, toHotelPayload, toRoomForm, toRoomPayload } from "../utils/admin.js"

export default function AdminPage() {
  const [hotels, setHotels] = useState([])
  const [selectedHotelId, setSelectedHotelId] = useState("")
  const [selectedHotel, setSelectedHotel] = useState(null)
  const [hotelForm, setHotelForm] = useState(emptyHotel)
  const [roomForm, setRoomForm] = useState(emptyRoom)
  const [editingHotelId, setEditingHotelId] = useState(null)
  const [editingRoomId, setEditingRoomId] = useState(null)
  const [isHotelFormOpen, setIsHotelFormOpen] = useState(false)
  const [isRoomFormOpen, setIsRoomFormOpen] = useState(false)
  const [message, setMessage] = useState("")
  const [error, setError] = useState("")
  const navigate = useNavigate()

  async function loadHotels() {
    const result = await request("/hotels")
    setHotels(result.data)
  }

  async function loadSelectedHotel(hotelId) {
    if (!hotelId) return setSelectedHotel(null)
    const result = await request(`/hotels/${hotelId}`)
    setSelectedHotel(result.data)
  }

  function handleError(requestError) {
    setMessage("")
    setError(requestError.message)
  }

  function showResult(text) {
    setError("")
    setMessage(text)
  }

  function updateForm(setForm) {
    return (event) => {
      const { name, value, checked, type } = event.target
      setForm((previous) => ({ ...previous, [name]: type === "checkbox" ? checked : value }))
    }
  }

  useEffect(() => {
    loadHotels().catch(handleError)
  }, [])

  useEffect(() => {
    loadSelectedHotel(selectedHotelId).catch(handleError)
  }, [selectedHotelId])

  async function saveHotel(event) {
    event.preventDefault()
    try {
      const path = editingHotelId ? `/admin/hotels/${editingHotelId}` : "/admin/hotels"
      const method = editingHotelId ? "PATCH" : "POST"
      const result = await request(path, { method, body: JSON.stringify(toHotelPayload(hotelForm)) })
      showResult(result.message)
      setHotelForm(emptyHotel)
      setEditingHotelId(null)
      setIsHotelFormOpen(false)
      await loadHotels()
    } catch (requestError) {
      handleError(requestError)
    }
  }

  async function saveRoom(event) {
    event.preventDefault()
    if (!selectedHotelId) return setError("객실을 등록할 호텔을 먼저 선택해 주세요.")

    try {
      const path = editingRoomId ? `/admin/rooms/${editingRoomId}` : `/admin/hotels/${selectedHotelId}/rooms`
      const method = editingRoomId ? "PATCH" : "POST"
      const result = await request(path, { method, body: JSON.stringify(toRoomPayload(roomForm)) })
      showResult(result.message)
      setRoomForm(emptyRoom)
      setEditingRoomId(null)
      setIsRoomFormOpen(false)
      await Promise.all([loadHotels(), loadSelectedHotel(selectedHotelId)])
    } catch (requestError) {
      handleError(requestError)
    }
  }

  function editHotel(hotel) {
    setSelectedHotelId(hotel._id)
    setEditingHotelId(hotel._id)
    setHotelForm(toHotelForm(hotel))
    setIsHotelFormOpen(true)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  function selectHotel(hotel) {
    setSelectedHotelId(hotel._id)
  }

  function openHotelCreateForm() {
    setEditingHotelId(null)
    setHotelForm(emptyHotel)
    setIsHotelFormOpen(true)
  }

  function closeHotelForm() {
    setEditingHotelId(null)
    setHotelForm(emptyHotel)
    setIsHotelFormOpen(false)
  }

  function editRoom(room) {
    setEditingRoomId(room._id)
    setRoomForm(toRoomForm(room))
    setIsRoomFormOpen(true)
  }

  function openRoomCreateForm() {
    setEditingRoomId(null)
    setRoomForm(emptyRoom)
    setIsRoomFormOpen(true)
  }

  function closeRoomForm() {
    setEditingRoomId(null)
    setRoomForm(emptyRoom)
    setIsRoomFormOpen(false)
  }

  async function removeHotel(hotel) {
    if (!window.confirm(`'${hotel.name}' 호텔과 모든 객실을 삭제할까요?`)) return
    try {
      const result = await request(`/admin/hotels/${hotel._id}`, { method: "DELETE" })
      showResult(result.message)
      if (selectedHotelId === hotel._id) setSelectedHotelId("")
      await loadHotels()
    } catch (requestError) {
      handleError(requestError)
    }
  }

  async function removeRoom(room) {
    if (!window.confirm(`'${room.name}' 객실을 삭제할까요?`)) return
    try {
      const result = await request(`/admin/rooms/${room._id}`, { method: "DELETE" })
      showResult(result.message)
      await Promise.all([loadHotels(), loadSelectedHotel(selectedHotelId)])
    } catch (requestError) {
      handleError(requestError)
    }
  }

  function logout() {
    localStorage.removeItem("accessToken")
    localStorage.removeItem("user")
    navigate("/login")
  }

  return (
    <main className="admin-page">
      <header className="hotel-header admin-header">
        <Link to="/hotels" className="hotel-brand">stay<span>hub</span></Link>
        <nav><Link to="/hotels">호텔 목록</Link><button onClick={logout}>로그아웃</button></nav>
      </header>

      <section className="admin-hero"><p className="eyebrow">ADMINISTRATION</p><h1>호텔과 객실 관리</h1><p>등록된 숙소 정보와 객실을 관리합니다.</p></section>

      <section className="admin-content">
        {(message || error) && <p className={error ? "admin-alert error-message" : "admin-alert"}>{error || message}</p>}
        {isHotelFormOpen && <div className="admin-modal" role="dialog" aria-modal="true" aria-labelledby="hotel-form-title"><div className="admin-modal-card"><AdminHotelForm form={hotelForm} isEditing={Boolean(editingHotelId)} onChange={updateForm(setHotelForm)} onReset={() => { setEditingHotelId(null); setHotelForm(emptyHotel) }} onClose={closeHotelForm} onSubmit={saveHotel} /></div></div>}
        {isRoomFormOpen && <div className="admin-modal" role="dialog" aria-modal="true" aria-labelledby="room-form-title"><div className="admin-modal-card"><AdminRoomForm hotels={hotels} selectedHotelId={selectedHotelId} form={roomForm} isEditing={Boolean(editingRoomId)} onHotelChange={(event) => setSelectedHotelId(event.target.value)} onChange={updateForm(setRoomForm)} onReset={() => { setEditingRoomId(null); setRoomForm(emptyRoom) }} onClose={closeRoomForm} onSubmit={saveRoom} /></div></div>}
        <AdminHotelList hotels={hotels} onCreate={openHotelCreateForm} onSelect={selectHotel} onEdit={editHotel} onDelete={removeHotel} />
        <AdminRoomList selectedHotel={selectedHotel} onCreate={openRoomCreateForm} onEdit={editRoom} onDelete={removeRoom} />
      </section>
    </main>
  )
}
