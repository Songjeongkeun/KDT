export default function AdminRoomForm({ hotels, selectedHotelId, form, isEditing, onHotelChange, onChange, onReset, onClose, onSubmit }) {
  return (
    <form className="admin-form" onSubmit={onSubmit}>
      <div className="admin-form-heading">
        <h2 id="room-form-title">{isEditing ? "객실 수정" : "새 객실 등록"}</h2>
        <div className="admin-form-actions">
          {isEditing && <button type="button" onClick={onReset}>새로 작성</button>}
          <button type="button" onClick={onClose}>닫기</button>
        </div>
      </div>
      <label>호텔 선택<select required value={selectedHotelId} onChange={onHotelChange}><option value="">호텔을 선택하세요</option>{hotels.map((hotel) => <option key={hotel._id} value={hotel._id}>{hotel.name}</option>)}</select></label>
      <label>객실명<input required name="name" value={form.name} onChange={onChange} placeholder="예: 디럭스 룸" /></label>
      <label>소개<textarea required name="description" value={form.description} onChange={onChange} placeholder="객실 소개" /></label>
      <div className="admin-form-row"><label>1박 가격<input required min="0" name="price" type="number" value={form.price} onChange={onChange} /></label><label>최대 인원<input required min="1" name="capacity" type="number" value={form.capacity} onChange={onChange} /></label></div>
      <label>같은 등급 객실 수<input required min="1" name="quantity" type="number" value={form.quantity} onChange={onChange} /></label>
      <label>편의시설<input name="amenities" value={form.amenities} onChange={onChange} placeholder="킹베드, 욕조" /></label>
      <label className="checkbox-label"><input name="isActive" type="checkbox" checked={form.isActive} onChange={onChange} /> 판매 중인 객실</label>
      <button className="admin-submit">{isEditing ? "객실 수정 저장" : "객실 등록"}</button>
    </form>
  )
}
