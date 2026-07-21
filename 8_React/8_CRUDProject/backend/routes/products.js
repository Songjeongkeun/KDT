import express from "express"
import mongoose from "mongoose"
import Product from "../models/Product.js"

const router = express.Router()

// 전체 상품 조회
router.get("/", async (req, res) => {
    try {
        const products = await Product.find().sort({ createdAt: -1 })
        res.status(200).json(products)
    } catch (error) {
        console.error("상품 조회 오류: ", error)
        res.status(500).json({
            message: "상품 목록을 불러오지 못했습니다."
        })
    }
})

// 특정 상품 조회 (id)
router.get("/:id", async (req, res) => {
    try {
        const { id } = req.params
        if (!mongoose.isValidObjectId(id)) {
            return res.status(400).json({
                message: "올바르지 않은 상품 ID입니다."
            })
        }

        const products = await Product.findById(id)
        if (!products) {
            return res.status(404).json({
                message: "상품을 찾을 수 없습니다."
            })
        }
        res.status(200).json(products)
    } catch (error) {
        console.error("상품 상세 조회 오류: ", error)
        res.status(500).json({
            message: "상품 정보를 불러오지 못했습니다."
        })
    }
})

router.post("/", async (req, res) => {
    try {
        const { name, price } = req.body
        if (!name || price === undefined) {
            return res.status(400).json({
                message: "상품명과 가격을 입력해 주세요."
            })
        }

        const product = await Product.create({
            name, price
        })
        res.status(201).json(product)
    } catch (error) {
        console.error("상품 등록 오류: ", error)
        res.status(400).json({
            message: "상품을 등록하지 못했습니다.",
            error: error.message
        })
    }
})

// 상품 수정
router.put("/:id", async (req, res) => {
    try{
        const { id } = req.params
        const { name, price } = req.body

        if(!mongoose.isValidObjectId(id)){
            return res.status(400).json({
                message: "올바르지 않은 상품 ID입니다."
            })
        }

        if(!name || price === undefined){
            return res.status(400).json({
                message: "상품명과 가격을 입력해 주세요."
            })
        }

        //{ new: true, runValidators: true }
        // new: ture -> 수정 후의 최신 데이터를 반환
        // runValidators: true -> 스키마의 유효성 검사도 함께 실행
        const updatedProduct = await Product.findByIdAndUpdate(
            id, {name, price}, { new: true, runValidators: true }
        )

        if(!updatedProduct){
            return res.status(404).json({
                message: "수정할 상품을 찾을 수 없습니다."
            })
        }

        return res.status(200).json(updatedProduct)
    } catch (error){    
        console.error("상품 수정 오류: ", error)
        res.status(400).json({
            message: "상품을 수정하지 못했습니다.",
            error: error.message
        })
    }
    
})

// 상품 삭제
router.delete("/:id", async (req, res) => {
    try{
        const { id } = req.params
        if(!mongoose.isValidObjectId(id)){
            return res.status(400).json({
                message: "올바르지 않은 상품 ID입니다."
            })
        }

        const deleteProduct = await Product.findByIdAndDelete(id)
        if(!deleteProduct){
            return res.status(404).json({
                message: "삭제할 상품을 찾을 수 없습니다."
            })
        }
        
        res.status(200).json({
            message: "상품이 삭제되었습니다.",
            product: deleteProduct
        })
    }catch (error){
        console.error("상품 삭제 오류: ", error)
        res.status(500).json({
            message: "상품을 삭제하지 못했습니다."
        })
    }
})

export default router