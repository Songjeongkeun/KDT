import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import { request } from "../services/api.js"

const numberFormatter = new Intl.NumberFormat("ko-KR")

function RoomCard({ room, index }) {
  return (
    <article className="room-card">
      <div className={`room-image room-tone-${index % 3}`}>
        <span>ROOM</span>
        <strong>{room.name.slice(0, 1)}</strong>
      </div>
      <div className="room-content">
        <div className="room-title-row">
          <h2>{room.name}</h2>
          <span className={room.isActive ? "available-badge" : "soldout-badge"}>
            {room.isActive ? "예약 가능" : "판매 중지"}
          </span>
        </div>
        <p>{room.description}</p>
        <p className="room-capacity">최대 {room.capacity}인 · 총 {room.quantity ?? 1}실</p>
        <div className="amenity-list">
          {room.amenities.map((amenity) => <span key={amenity}>{amenity}</span>)}
        </div>
        <div className="room-price-row">
          <p><strong>{numberFormatter.format(room.price)}원</strong> / 1박</p>
          {/* 예약 페이지는 다음 단계에서 /reservations/new 경로로 연결합니다. */}
          <button disabled={!room.isActive}>{room.isActive ? "객실 선택" : "예약 불가"}</button>
        </div>
      </div>
    </article>
  )
}

export default function HotelDetailPage() {
  const { hotelId } = useParams()
  const [detail, setDetail] = useState(null)
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadHotelDetail() {
      try {
        setIsLoading(true)
        setError("")
        const result = await request(`/hotels/${hotelId}`)
        setDetail(result.data)
      } catch (requestError) {
        setError(requestError.message)
      } finally {
        setIsLoading(false)
      }
    }

    loadHotelDetail()
  }, [hotelId])

  if (isLoading) return <p className="detail-message">호텔 정보를 불러오는 중입니다.</p>
  if (error) return <p className="detail-message error-message">{error}</p>

  const { hotel, rooms } = detail
  const rating = hotel.ratingCount ? hotel.ratingAverage.toFixed(1) : "신규"

  return (
    <main className="detail-page">
      <header className="hotel-header">
        <Link to="/hotels" className="hotel-brand">stay<span>hub</span></Link>
        <Link to="/hotels" className="back-link">← 호텔 목록</Link>
      </header>

      <section className="detail-hero">
        <div className="detail-hero-image"><span>{hotel.region}</span><strong>{hotel.name.slice(0, 1)}</strong></div>
        <div className="detail-summary">
          <p className="eyebrow orange">{hotel.region.toUpperCase()} STAY</p>
          <h1>{hotel.name}</h1>
          <p className="detail-address">{hotel.address}</p>
          <p className="detail-description">{hotel.description}</p>
          <div className="detail-rating">★ {rating}{hotel.ratingCount ? ` · 후기 ${hotel.ratingCount}개` : ""}</div>
          <div className="amenity-list detail-amenities">
            {hotel.amenities.map((amenity) => <span key={amenity}>{amenity}</span>)}
          </div>
        </div>
      </section>

      <section className="room-section">
        <div className="section-heading">
          <div><p className="eyebrow orange">ROOMS</p><h1>객실 선택</h1></div>
          <p>체크인 날짜 선택은 다음 예약 단계에서 진행합니다.</p>
        </div>
        {rooms.length === 0 ? (
          <p className="result-message">현재 등록된 객실이 없습니다.</p>
        ) : (
          <div className="room-list">{rooms.map((room, index) => <RoomCard key={room._id} room={room} index={index} />)}</div>
        )}
      </section>
    </main>
  )
}
