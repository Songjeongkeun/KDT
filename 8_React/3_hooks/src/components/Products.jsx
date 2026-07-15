import React, { useEffect, useState } from "react"

export default function Products() {
    const [loading, setLoading] = useState(false)
    const [checked, setChecked] = useState(false)
    const [error, setError] = useState()
    const [products, setProducts] = useState([])

    const handleChange = () => setChecked((prev) => !prev)

    useEffect(() => {
        setLoading(true)
        setError(undefined)
        fetch(`data/${checked ? "sale_" : ""}products.json`)
            .then((res) => res.json())
            .then((data) => {
                console.log("네트워크에서 데이터를 잘 불러옴")
                setProducts(data)
            })
            .catch((e) => setError("에러가 발생함!"))
            .finally(() => setLoading(false))

        return () => {
            console.log("데이터 처리 완료")
        }
    }, [checked])

    if (loading) return <p>Loading 중...</p>
    if (error) return <p>{error}</p>

    return (
        <>
            <input id="checkbox" type="checkbox" checked={checked} value={checked} onChange={handleChange} />
            <label htmlFor="checkbox">세일상품보기</label>
            <ul>
                {products.map((product) => (
                    <li>
                        <article>
                            <h3>{product.name}</h3>
                            <p>{product.price}</p>
                        </article>
                    </li>
                ))}

            </ul>
        </>
    )
}