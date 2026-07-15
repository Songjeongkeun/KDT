/*
    http 모듈
    - 웹 서버를 만들 수 있게 해주는 핵심 내장 모듈
    - 클라이언트의 요청을 받고 응답을 반환하는 기능을 제공

    Content-Type
    - 서버가 브라우저에게 "지금 보내는 데이터의 형식이 무엇인지 알려주는 HTTP 헤더"
    - 브라우저는 이 값을 보고 데이터를 어떻게 해석할지 결정
        text/html: html 문서
        text/plain: 일반 텍스트
        application/json: JSON 데이터
        text/css: css 파일
        application/javascript : JavaScript 파일
        image/png : PNG 이미지
        image/jpeg : JPG 이미지
        multipart/form-data : 파일 업로드

    Header
    - 인터넷에서 데이터를 주고받을 때 본문(내용)보다 먼저 전달되는 추가 정보 영역으로, "이 데이터가 무엇인지, 어떻게처리해야 하는지"를 설명해주는 안내문과 같음
    - 브라우저가 서버에 요청을 보낼 때는 어떤 형식을 원하는지, 로그인 정보가 있는지 같은 정보를 헤더에 담고, 서버는 응답할 때 데이터 형식이 무엇인지, 캐시 여부는 어떤지 등의 정보를 헤더에 담아 전달
*/

const http = require("http")

const server = http.createServer((req, res) => {
    // req: 요청 객체, res: 응답 객체
    res.writeHead(200, {"Content-Type": "text/html"})
    // res.end("Hello Node.js!!") // 사용자에게 전달되는 내용
    res.end("<h1>안녕하세요!</h1>")
}) 

server.listen(3000, () => {
    console.log("서버 실행 중..")
})