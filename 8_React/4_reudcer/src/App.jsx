import React, { useCallback, useMemo, memo } from "react"
import './App.css'

function App() {

  const handleAdd = useCallback(() => {
    const name = prompt("멘토의 이름을 입력하세요")
    const title = prompt("멘토의 직함을 입력하세요")
  })

  const handleUpdate = useCallback(() => {
    const prev = prompt("변경 이전의 멘토 이름을 입력하세요")
    const title = prompt("변경 이후의 멘토 이름을 입력하세요")
  })

  const handleDelete = useCallback(() => {
    const name = prompt("삭제할 멘토 이름을 입력하세요")
  })

  return (
    <>
      <div>
        <h1>
          김사과 프로젝트 매니저
        </h1>
        <p>김사과의 멘토는: </p>
        <Button text="멘토 추가하기" onClick={handleAdd}>멘토 추가하기</Button>
        <Button text="멘토 이름 바꾸기" onClick={handleUpdate}>멘토 이름 바꾸기</Button>
        <Button text="멘토 삭제하기" onClick={handleDelete}>멘토 삭제하기</Button>
      </div>
    </>
  )
}

function calculator() {
  for(let i = 0; i < 10000; i++){
    console.log("😝")
  }
  return 10000 
}

const Button = memo(({ text, onClick }) => {
    console.log("Button", text, "랜더링 되었음!")
    const result = useMemo(() => calculator(), [])
    return (
      <button onClick={onClick} style={{ 
        backgroundColor: "deepskyblue", color: "white", borderRadius: "20px", margin: "0.4rem", padding: "20px"
      }}>{`${text} ${result}`}</button>
    )
})

export default App