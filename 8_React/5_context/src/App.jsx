import React from "react"
import { useContext } from "react"
import { DarkModeContext } from "./DarkModeContext"
import "./App.css"

function App() {
  const { darkMode, toggleDarkMode } = useContext(DarkModeContext)

  return (
    <main className="app">
      <section className="content">
        <h1>다크모드 설정</h1>
        <p>현재 화면 모드는{" "} <strong>{darkMode ? "다크모드" : "라이트모드"}</strong>입니다.</p>
        <button type="button" onClick={toggleDarkMode}>{darkMode ? "라이트모드로 변경" : "다크모드로 변경"}</button>
      </section>
    </main>
  )
}


export default App