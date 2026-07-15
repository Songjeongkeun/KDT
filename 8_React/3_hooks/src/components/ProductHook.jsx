import React, { useState } from "react"
import useProducts from "../hooks/useProducts"

export default function Products() {
    const [checked, setChecked] = useState(false)
    const [loading, error, products] = useProducts({ salesOnly: checked })

    const handleChange = () => setChecked((prev) => !prev)

    if (loading) return <p>Loading 중...</p>
    if (error) return <p>{error}</p>

    return (
        <>
            <input id="checkbox" type="checkbox" checked={checked} value={checked} onChange={handleChange} />
            <label htmlFor="checkbox">세일상품보기</label>
            <ul>
                {products.map((product) => (
                    <li key={product.id}>
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