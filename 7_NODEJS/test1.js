const express = require("express")
const {MongoClient, ObjectId, ReturnDocument} = require ("mongodb")
// const { memo } = require("react") 

const app = express()
const PORT = 3000

app.use(express.json())

const url = "mongodb://eiruubp:dlffpdlxodml@ac-oqayn0t-shard-00-00.tj7kotr.mongodb.net:27017,ac-oqayn0t-shard-00-01.tj7kotr.mongodb.net:27017,ac-oqayn0t-shard-00-02.tj7kotr.mongodb.net:27017/?ssl=true&replicaSet=atlas-ynru9s-shard-0&authSource=admin&appName=Cluster0"

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

//3
app.get("/memos", async(req, res) => {
    try {
        const { keyword } = req.query
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

        // 2
        const memos = await memoCollection.find().sort({ createdAt: -1}).toArray()

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

//4
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