import { useState } from "react"
import "./App.css"
import { useEffect } from "react"

const API_URL = "http://127.0.0.1:5001/api/products"

export default function App() {
  const [products, setProducts] = useState([])
  const [name, setName] = useState("")
  const [price, setPrice] = useState("")
  const [editingId, setEditingId] = useState(null)
  const [loading, setLoading] = useState(null)
  const [error, setError] = useState("")

  const fetchProducts = async () => {
    try {
      setLoading(true)
      setError("")

      const response = await fetch(API_URL)
      if (!response.ok) {
        throw new Error("상품 목록을 불러오지 못했습니다.")
      }

      const data = await response.json()
      setProducts(data)
    } catch (error) {
      console.error(error)
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const resetForm = () => {
    setName("")
    setPrice("")
    setEditingId(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim() || price === "") {
      alert("상품명과 가격을 입력해주세요.")
      return
    }

    try {
      setError("")
      const isEditing = editingId !== null
      const url = isEditing ? `${API_URL}/${editingId}` : API_URL
      const method = isEditing ? "PUT" : "POST"

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name.trim(),
          price: Number(price)
        })
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || "요청 처리에 실패했습니다.")
      }

      resetForm()
      await fetchProducts()

    } catch (error) {
      console.error(error)
      setError(error.message)
    }
  }

  const handleEdit = (product) => {
    setName(product.name)
    setPrice(product.price)
    setEditingId(product.editingId)
  }

  const handleDelete = async (id) => {
    const isConfirmed = window.confirm("상품을 삭제하시겠습니까?")
    if (!isConfirmed) {
      return
    }
    try {
      setError("")
      const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || "상품 삭제에 실패했습니다.")
      }

      if (editingId === id) {
        resetForm()
      }

      await fetchProducts()
    } catch (error) {
      console.error(error)
      setError(error.message)
    }
  }

  return (
    <main className="container">
      <h1>상품 관리</h1>
      <form className="product-form" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">상품명</label>
          <input id="name" type="text" placeholder="상품명을 입력하세요." value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div>
          <label htmlFor="price">가격</label>
          <input id="price" type="number" min="0" placeholder="가격을 입력하세요." value={price} onChange={(e) => setPrice(e.target.value)} />
        </div>
        <div className="button-group">
          <button type="submit">
            {editingId ? "수정 완료" : "상품 등록"}
          </button>

          {editingId && (
            <button type="button" className="cancel-button" onClick={resetForm}>
              수정 취소
            </button>
          )}
        </div>
      </form>

      {error && <p className="error-message">{error}</p>}
      {loading ? (
        <p>상품 목록을 불러오는 중입니다.</p>
      ) : products.length === 0 ? (
        <p>등록된 상품이 없습니다.</p>
      ) : (
        <ul className="product-list">
          {products.map((product) => (
            <li key={product._id}>
              <div><strong>{product.name}</strong><span>{product.price.toLocaleString()}원</span></div>
              <div className="button-group">
                <button type="button" onClick={() => handleEdit(product)}>수정</button>
                <button type="button" onClick={() => handleDelete(product._id)}>삭제</button>
              </div>
            </li>
          ))}

        </ul>
      )}

    </main>
  )
}