import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { request } from "../services/api.js"

const numberFormatter = new Intl.NumberFormat("ko-KR")

function HotelCard({ hotel, index }) {
  const rating = hotel.ratingCount ? hotel.ratingAverage.toFixed(1) : "신규"

  return (
    <article className="hotel-card">
      <Link className="hotel-card-link" to={`/hotels/${hotel._id}`}>
        <div className={`hotel-card-image tone-${index % 3}`}>
          <span>{hotel.region}</span>
          <strong>{hotel.name.slice(0, 1)}</strong>
        </div>
        <div className="hotel-card-body">
          <p className="hotel-region">{hotel.region} · {hotel.address}</p>
          <h2>{hotel.name}</h2>
          <p className="hotel-description">{hotel.description}</p>
          <div className="amenity-list">
            {hotel.amenities.slice(0, 3).map((amenity) => <span key={amenity}>{amenity}</span>)}
          </div>
          <div className="hotel-card-bottom">
            <span className="rating">★ {rating}{hotel.ratingCount ? ` (${hotel.ratingCount})` : ""}</span>
            <p><strong>{numberFormatter.format(hotel.minPrice)}원</strong><span> / 1박</span></p>
          </div>
        </div>
      </Link>
    </article>
  )
}

export default function HotelListPage() {
  const [region, setRegion] = useState("")
  const [keyword, setKeyword] = useState("")
  const [sort, setSort] = useState("")
  const [appliedFilter, setAppliedFilter] = useState({ region: "", keyword: "", sort: "" })
  const [hotels, setHotels] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem("user") || "null")

  useEffect(() => {
    async function loadHotels() {
      try {
        setIsLoading(true)
        setError("")

        const params = new URLSearchParams()
        if (appliedFilter.region) params.set("region", appliedFilter.region)
        if (appliedFilter.keyword) params.set("keyword", appliedFilter.keyword)
        if (appliedFilter.sort) params.set("sort", appliedFilter.sort)

        const query = params.toString()
        const result = await request(`/hotels${query ? `?${query}` : ""}`)
        setHotels(result.data)
      } catch (requestError) {
        setError(requestError.message)
      } finally {
        setIsLoading(false)
      }
    }

    loadHotels()
  }, [appliedFilter])

  function handleSearch(event) {
    event.preventDefault()
    setAppliedFilter({ region, keyword, sort })
  }

  function handleSortChange(event) {
    const nextSort = event.target.value
    setSort(nextSort)
    setAppliedFilter({ region, keyword, sort: nextSort })
  }

  function resetFilters() {
    setRegion("")
    setKeyword("")
    setSort("")
    setAppliedFilter({ region: "", keyword: "", sort: "" })
  }

  function logout() {
    localStorage.removeItem("accessToken")
    localStorage.removeItem("user")
    navigate("/login")
  }

  return (
    <main className="hotel-page">
      <header className="hotel-header">
        <Link to="/hotels" className="hotel-brand">stay<span>hub</span></Link>
        <div className="header-user">
          <span>{user ? `${user.nickname}님` : "여행자님"}</span>
          {user?.role === "ADMIN" && <Link to="/admin">관리자</Link>}
          {user ? <button onClick={logout}>로그아웃</button> : <Link to="/login">로그인</Link>}
        </div>
      </header>

      <section className="hotel-hero">
        <p className="eyebrow orange">FIND YOUR STAY</p>
        <h1>어디로 떠나시나요?</h1>
        <p>원하는 지역과 호텔을 찾아 특별한 휴식을 계획해 보세요.</p>

        <form className="hotel-search" onSubmit={handleSearch}>
          <label>
            <span>지역</span>
            <input value={region} onChange={(event) => setRegion(event.target.value)} placeholder="예: 서울, 제주" />
          </label>
          <label>
            <span>호텔명</span>
            <input value={keyword} onChange={(event) => setKeyword(event.target.value)} placeholder="호텔 이름으로 검색" />
          </label>
          <button type="submit">호텔 검색</button>
        </form>
      </section>

      <section className="hotel-results">
        <div className="result-heading">
          <div>
            <p className="eyebrow orange">STAYS</p>
            <h1>추천 호텔</h1>
          </div>
          <select aria-label="정렬 기준" value={sort} onChange={handleSortChange}>
            <option value="">최신 등록순</option>
            <option value="price">낮은 가격순</option>
            <option value="rating">높은 평점순</option>
          </select>
        </div>

        {isLoading && <p className="result-message">호텔 정보를 불러오는 중입니다.</p>}
        {error && <p className="result-message error-message">{error}</p>}
        {!isLoading && !error && hotels.length === 0 && (
          <div className="empty-result">
            <h2>조건에 맞는 호텔이 없어요.</h2>
            <p>다른 검색어를 입력하거나 전체 호텔을 확인해 보세요.</p>
            <button className="outline-button" onClick={resetFilters}>전체 호텔 보기</button>
          </div>
        )}
        {!isLoading && !error && hotels.length > 0 && (
          <div className="hotel-grid">
            {hotels.map((hotel, index) => <HotelCard key={hotel._id} hotel={hotel} index={index} />)}
          </div>
        )}
      </section>
    </main>
  )
}
