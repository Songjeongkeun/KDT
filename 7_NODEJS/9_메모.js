const express = require("express")
const path = require("path")
const { MongoClient, ObjectId, ReturnDocument } = require("mongodb")

const app = express()
const PORT = 3000

app.use(express.json())
app.use(express.static(path.join(__dirname, "public")))
// /KDT/7_NODEJS/public
const url = process.env.MONGODB_URL

if (!url) {
    throw new Error("MONGODB_URL 환경변수를 설정해주세요.")
}

const client = new MongoClient(url)

const dbName = "memo"
let memoCollection

async function startServer() {
    try {
        await client.connect()
        console.log("MongoDB 연결 성공!!")

        const db = client.db(dbName)
        memoCollection = db.collection("memos")

        app.listen(PORT, () => {
            console.log("서버 실행 중...")
        })
    } catch (error) {
        console.log("MongoDB 연결 실패: ", error)
    }
}

startServer()

app.get("/memos", async(req, res) => {
    try {
        // console.log("req: ", req)
        console.log("req.query: ", req.query)
        const { keyword } = req.query   // { }
        let filter = {}

        if(keyword && keyword.trim() !== "") {
            filter = {
                text: { $regex: keyword.trim(), $options: "i" }
            }
        }

        const memos = await memoCollection.find(filter).sort({ createdAt: -1 }).toArray()
        res.json({
            success: true,
            count: memos.length,
            memos
        })
    }catch(error) {
        console.log("메모 조회 오류: ", error)
        res.status(500).json({
            success: false,
            message: "메모 조회 중 오류가 발생!"
        })
    }
})


app.post("/memo", async(req, res) => {
    try {
        // { text: "메모값" }

        const { text } = req.body 
        if(!text || text.trim() === "") {
            return res.status(400).json({
                success: false,
                message: "메모 내용을 입력해주세요"
            })
        }

        const newMemo = {
            text: text.trim(),
            createdAt: new Date()
        }

        await memoCollection.insertOne(newMemo)

        const memos = await memoCollection.find().sort({ createdAt: -1 }).toArray()

        res.status(201).json({
                success: true,
                message: "메모가 추가되었습니다.",
                memos
        })
    } catch (error) {
        console.log("메모 저장 오류: ", error)
        res.status(500).json({
                success: false,
                message: "서버 오류가 발생!!"
        })
    }
})

app.put("/memos/:id", async (req, res) => {
    try{
        const { id } = req.params
        const { text } = req.body

        // id가 MongoDB ObjectId 형식인지 검사하고 아니면 400에러를 반환
        if(!ObjectId.isValid(id)) {
            return res.status(400).json({
                success: false,
                message: "올바르지 않은 메모 id 형식!!"
            })
        }

        if(!text || text.trim() === "") {
            return res.status(400).json({
                success: false,
                message: "변경할 메모 내용을 입력해주세요"
            })
        }

        const result = await memoCollection.findOneAndUpdate(
            { _id: new ObjectId(id) },
            {
                $set: {
                    text: text.trim(),
                    updatedAt: new Date()
                }
            },
            {
                returnDocument: "after"
            }
        )

        if(!result) {
            return res.status(404).json({
                success: false,
                message: "해당 id의 메모를 찾을 수 없습니다"
            })
        }

        res.json({
            success: true,
            message: "메모가 수정되었습니다. (PUT)",
            memo: result
        })
    }catch(error){
        console.log("메모 수정 오류(PUT): ", error)
        return res.status(500).json({
            success: false,
            message: "메모 수정 중 오류가 발생!!"
        })
    }
})

app.delete("/memos/:id", async(req, res) => {
    try{
        const { id } = req.params

        if(!ObjectId.isValid(id)) {
            return res.status(400).json({
                success: false,
                message: "올바르지 않은 메모 id 형식!!"
            })
        }

        const result = await memoCollection.deleteOne({
            _id: new ObjectId(id)
        })

        if (result.deletedCount === 0) {
            return res.status(404).json({
                success: false,
                message: "삭제할 메모를 찾을 수 없습니다."
            })
        }

        const memos = await memoCollection.find().sort({ createdAt: -1 }).toArray()
        res.json({
            success: true,
            message: "메모가 삭제되었습니다.",
            memo: result,
            count: memos.length,
            memos
        })
    }catch(error){
        console.log("메모 삭제 오류: ", error)
        return res.status(500).json({
            success: false,
            message: "메모 삭제 중 오류가 발생!!"
        })
    }
})
