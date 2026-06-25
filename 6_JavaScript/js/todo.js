// todo.js
// 2026-06-23

const todoInput = document.getElementById("todoInput")
const addBtn = document.getElementById("addBtn")
const todoList = document.getElementById("todoList")
const remainingCount = document.getElementById("remainingCount")
const totalCount = document.getElementById("totalCount")

// 화면 그리기 함수
function render(){
    todoList.innerHTML = ""
    // [{text:"아침식사", done:false}, {text="운동하기", done:false}, ...]
    todos.forEach((todo, index) => {
        const li = document.createElement("li") // <li></li>
        if(todo.done) li.classList.add("done")  // <li class=done>운동하기</li>.  

        const left = document.createElement("div")
        left.className = "left" // <div class="left"></div>

        const checkbox = document.createElement("input") // <input></input>
        checkbox.type = "checkbox" // <input type="checkbox"></input>
        checkbox.checked = todo.done // <input type="checkbox" checked="false"></input>
        checkbox.addEventListener("change", () => {
            todo.done = checkbox.checked
            render()
        })

        const text = document.createElement("span") // <span></span>
        text.className = "todo-text" // <span class="todo-text"></span>
        text.textContent = todo.text // <span class="todo-text">아침식사</span>

        const delBtn = document.createElement("button") // <button></button>
        delBtn.type = "button"    // <button type="button"></button>
        delBtn.className = "delete-btn"
        delBtn.textContent = "삭제" // <button type="button">삭제</button>
        delBtn.addEventListener("click", () => {
            todos.splice(index, 1)
            render()
        })
        
        left.appendChild(checkbox)
        left.appendChild(text)
        left.appendChild(delBtn)

        li.appendChild(left)
        todoList.appendChild(li)
    })
    updateCounts()
    render()
}   

function updateCounts(){
    remainingCount.textContent = String(todos.filter(todo => !todo.done).length)
    totalCount.textContent = String(todos.length)
}

// 상태를 메모리에만 저장(새로고침하면 사라짐)
const todos =[]

function addTodo(){
    const text = todoInput.value.trim()
    if(!text) return

    // 키랑 변수명이 동일하면 생략가능
    todos.push({ text, done: false})
    todoInput.value = ""
    todoInput.focus()

    // 화면 그리지
    render()
}

addBtn.addEventListener("click", addTodo)

todoInput.addEventListener("keydown", (e) => {
    if(e.key === "Enter") addTodo()
    if (e.isComposing) return;
})

render()