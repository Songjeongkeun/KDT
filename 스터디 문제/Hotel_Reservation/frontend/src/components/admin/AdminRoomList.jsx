import { priceFormatter } from "../../utils/admin.js"

export default function AdminRoomList({ selectedHotel, onCreate, onEdit, onDelete }) {
  if (!selectedHotel) return null

  const { hotel, rooms } = selectedHotel

  return (
    <section className="admin-list-section room-management">
      <div className="admin-section-heading">
        <h2>{hotel.name} 객실</h2>
        <div className="admin-list-heading-actions"><span>{rooms.length}개</span><button className="admin-add-button" onClick={onCreate}>+ 객실 등록하기</button></div>
      </div>
      {rooms.length === 0 ? <p className="result-message">등록된 객실이 없습니다.</p> : (
        <div className="admin-room-list">
          {rooms.map((room) => (
            <article key={room._id}>
              <div><h3>{room.name}</h3><p>{priceFormatter.format(room.price)}원 · 최대 {room.capacity}인 · {room.quantity ?? 1}실 · {room.isActive ? "판매 중" : "판매 중지"}</p></div>
              <div className="admin-actions"><button onClick={() => onEdit(room)}>수정</button><button className="delete-button" onClick={() => onDelete(room)}>삭제</button></div>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}
