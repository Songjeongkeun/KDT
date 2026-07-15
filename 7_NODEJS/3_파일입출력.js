/*
    파일 입출력
    fs(File System) 모듈을 사용해서 파일을 읽고 쓰는 작업을 수행
*/

const fs = require("fs")

// 동기 방식으로 파일 읽기 : 에러 처리 방식 x -> 에러 처리를 할려면 try-catch를 사용해야 한다.
const data = fs.readFileSync("./example1.txt", "utf8")
console.log("파일 내용: ", data)

// 비동기 방식으로 파일 읽기 : 에러 처리 방식을 기본적으로 가지고 있다.
fs.readFile("example2.txt", "utf8", (err, data) => {
    if (err) {
        console.log("파일 일기 실패: ", err)
        return
    }
    console.log("파일 내용: ", data)
})

// 동기 방식으로 파일 쓰기
fs.writeFileSync("output1.txt", "이 내용이 파일에 저장됩니다. 동기방식!")
console.log("파일 저장 완료 (동기)")

// 비동기 방식으로 파일 쓰기
fs.writeFile("output2.txt", "비동기 방식으로 저장합니다.", (err) => {
    if (err) {
        console.log("저장 실패: ", err)
        return
    }
    console.log("파일 저장 완료 (비동기)")
})

// 비동기 방식으로 파일에 내용 추가
fs.appendFile("output2.txt", "\n 새로운 줄이 추가됩니다.", (err) => {
    if(err) throw err
    console.log("내용 추가 완료 ")
})

fs.unlink("output2.txt", (err) => {
    if(err) throw err
    console.log("파일 삭제 완료")
})