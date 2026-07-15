const http = require("http")

const server = http.createServer((req, res) => {
  const requestUrl = new URL(req.url, `http://${req.headers.host}`)

  const pathname = requestUrl.pathname
  const userid = requestUrl.searchParams.get("userid")
  const username = requestUrl.searchParams.get("username")

  if (pathname === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" })
    res.end(`
      <h1>Query String 확인</h1>
      <p>userid: ${userid}</p>
      <p>username: ${username}</p>
    `)
  }else{
    res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" })
    res.end("<h1>Not Found</h1>")
  }
})

server.listen(3000, () => {
  console.log("서버 실행 중...")
})