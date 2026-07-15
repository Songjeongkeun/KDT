import express from "express"
import { Server } from "socket.io"
import { createServer } from "http"
import path from "path"
import { fileURLToPath } from "url"

const app = express()
const server = createServer(app)
const io = new Server(server)

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

app.use(express.static(path.join(__dirname, "public")))

const users = {}
io.on("connection", (socket) => {
    console.log("사용자가 연결되었음")

    socket.on("join", ({ nickname, channel }) => {
        Object.keys(users).forEach((id) => {
            if (users[id].nickname === nickname) {
                delete users[id];
            }
        });
        socket.nickname = nickname
        socket.channel = channel
        users[socket.id] = { nickname, channel }
        socket.join(channel)
        // console.log(socket.id)
        const msg = { user: "system", text: `${nickname}님이 입장했습니다.` }
        console.log("nickname: ", nickname, "channel: ", channel)
        io.to(channel).emit("message", msg)
        updateUserList()
    })

    socket.on("chat", ({ text, to }) => {
        const sender = users[socket.id]
        if (!sender) return
        const payload = { user: sender.nickname, text }
        if (to) {
            const receiverSocket = Object.entries(users).find(
                ([id, u]) => u.nickname === to)?.[0]
            if (receiverSocket) {
                io.to(receiverSocket).emit("whisper", payload)
                socket.emit("whisper", payload)
            }
        } else {
            io.to(sender.channel).emit("message", payload)
            console.log("sender.channel: ", sender.channel, "payload: ", payload)
        }
    })

    socket.on("changeChannel", ({ newChannel }) => {
        const user = users[socket.id]
        if (!user) {
            console.log("비정상 접속 사용자!")
            return
        }

        const oldChannel = socket.channel
        const nickname = socket.nickname
        socket.leave(oldChannel)
        io.to(oldChannel).emit("message", {
            user: "system",
            text: `${nickname}님이 ${newChannel} 채널로 이동했습니다`
        })
        socket.channel = newChannel
        users[socket.id].channel = newChannel
        socket.join(newChannel)
        const joinMsg = { user: "system", text: `${nickname}님이 입장했습니다` }
        io.to(newChannel).emit("message", joinMsg)
        updateUserList()
    })

    socket.on("disconnect", () => {
        const user = users[socket.id]
        if (user) {
            const msg = { user: "system", text: `${user.nickname}님이 퇴장했습니다` }
            io.to(user.channel).emit("message", msg)
            delete users[socket.id]
        }

        updateUserList()
    })

    function updateUserList() {
        const userList = Object.values(users)
        // console.log(userList)
        io.emit("userList", userList)
    }
})



server.listen(3000, () => {
    console.log("서버 실행 중...")
})

