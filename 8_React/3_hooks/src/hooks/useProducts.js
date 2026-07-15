import React, { useState, useEffect } from "react"

export default function useProducts({ salesOnly }) {
    // useEffect

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState()
    const [products, setProducts] = useState([])

    useEffect(() => {
        setLoading(true)
        setError(undefined)
        fetch(`data/${salesOnly ? "sale_" : ""}products.json`)
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
    }, [salesOnly])
    return [loading, error, products]
}