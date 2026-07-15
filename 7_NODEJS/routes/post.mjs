import express from "express"

const router = express.Router()

// http://127.0.0.1/posts (GET)
router.get("/", (req, res) => {
    res.status(200).send("GET: /posts 글보기")
})

// http://127.0.0.1/posts (POST)
router.post("/", (req, res) => {
    res.status(201).send("POST: /posts 글 작성하기")
})

// http://127.0.0.1/posts (PUT)
router.put("/:id", (req, res) => {
    res.status(201).send("PUT /posts/:id 글 수정하기")
})

// http://127.0.0.1/posts (DELETE)
router.delete("/:id", (req, res) => {
    res.status(200).send("DELETE /posts/:id 글 삭제하기")
})

export default router