export default function AdminHotelForm({ form, isEditing, onChange, onReset, onClose, onSubmit }) {
  return (
    <form className="admin-form" onSubmit={onSubmit}>
      <div className="admin-form-heading">
        <h2 id="hotel-form-title">{isEditing ? "호텔 수정" : "새 호텔 등록"}</h2>
        <div className="admin-form-actions">
          {isEditing && <button type="button" onClick={onReset}>새로 작성</button>}
          <button type="button" onClick={onClose}>닫기</button>
        </div>
      </div>
      <label>호텔명<input required name="name" value={form.name} onChange={onChange} placeholder="호텔 이름" /></label>
      <label>지역<input required name="region" value={form.region} onChange={onChange} placeholder="예: 서울" /></label>
      <label>주소<input required name="address" value={form.address} onChange={onChange} placeholder="상세 주소" /></label>
      <label>소개<textarea required name="description" value={form.description} onChange={onChange} placeholder="호텔 소개" /></label>
      <label>최저가<input required min="0" name="minPrice" type="number" value={form.minPrice} onChange={onChange} placeholder="1박 기준 가격" /></label>
      <label>편의시설<input name="amenities" value={form.amenities} onChange={onChange} placeholder="수영장, 조식, 피트니스" /></label>
      <button className="admin-submit">{isEditing ? "호텔 수정 저장" : "호텔 등록"}</button>
    </form>
  )
}
