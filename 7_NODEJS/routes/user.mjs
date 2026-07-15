import express from "express"

const router = express.Router()

// http://127.0.0.1/users (GET)
router.get("/", (req, res) => {
    res.status(200).send("GET: /users 회원정보보기")
})

// http://127.0.0.1/users (POST)
router.post("/", (req, res) => {
    res.status(201).send("POST: /users 회원가입")
})

// http://127.0.0.1/users (PUT)
router.put("/:id", (req, res) => {
    res.status(201).send("PUT: /users:id 정보수정")
})

// http://127.0.0.1/users (DELETE)
router.delete("/:id", (req, res) => {
    res.status(200).send("DELETE: /users:id 회원탈퇴")
})

export default router