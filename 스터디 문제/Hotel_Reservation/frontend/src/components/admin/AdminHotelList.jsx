import { priceFormatter } from "../../utils/admin.js"

export default function AdminHotelList({ hotels, onCreate, onSelect, onEdit, onDelete }) {
  return (
    <section className="admin-list-section">
      <div className="admin-section-heading">
        <h2>등록된 호텔</h2>
        <div className="admin-list-heading-actions"><span>{hotels.length}개</span><button className="admin-add-button" onClick={onCreate}>+ 호텔 등록하기</button></div>
      </div>
      {hotels.length === 0 ? <p className="result-message">등록된 호텔이 없습니다.</p> : (
        <div className="admin-hotel-list">
          {hotels.map((hotel) => (
            <article
              key={hotel._id}
              className="admin-hotel-item selectable-hotel-item"
              role="button"
              tabIndex="0"
              onClick={() => onSelect(hotel)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault()
                  onSelect(hotel)
                }
              }}
            >
              <div><p>{hotel.region} · {priceFormatter.format(hotel.minPrice)}원부터</p><h3>{hotel.name}</h3></div>
              <div className="admin-actions"><button onClick={(event) => { event.stopPropagation(); onEdit(hotel) }}>수정</button><button className="delete-button" onClick={(event) => { event.stopPropagation(); onDelete(hotel) }}>삭제</button></div>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}
