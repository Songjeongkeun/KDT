const memoInput = document.getElementById("memoInput")
const addBtn = document.getElementById("addBtn")
const memoList = document.getElementById("memoList")

// 메모 불러오기
async function loadMemos() {
    try {
        const response = await fetch("/memos")
        const data = await response.json()
        renderMemos(data.memos)
    } catch (error) {
        console.log("메모 조회 실패: ", error)
    }
}

// 메모 추가하기
addBtn.addEventListener("click", async () => {
    const text = memoInput.value.trim()
    if (!text) {
        alert("메모를 입력하세요")
        return
    }

    try {
        const response = await fetch("/memo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        })
        const data = await response.json()
        memoInput.value = ""
        renderMemos(data.memos)
    } catch (error) {
        console.log("메모 추가 실패", error)
    }
})

function renderMemos(memos) {
    memoList.innerHTML = ""

    // memo 에 아이디 값이 들어있음. 
    memos.forEach((memo) => {
        const li = document.createElement("li") // <li></li>
        li.className = "memo-item"  // <li class="memo-item"></li>
        li.innerHTML = `
            <span>${memo.text}</span>
            <div class="memo-buttons">
                <button onclick="editMemo('${memo._id}')">수정</button> <button onclick="deleteMemo('${memo._id}')">삭제</button>
            </div>
        `
        memoList.appendChild(li)
    })
}

// 메모 삭제
async function deleteMemo(id) {
    const check = confirm("정말 삭제하시겠습니까")
    // console.log(check)
    // console.log(_id)
    if (!check) return

    try {
        const response = await fetch(`/memos/${id}`, {
            method: "DELETE"
        })
        const data = await response.json()
        console.log(data)
        renderMemos(data.memos)
    } catch (error) {
        console.log("메모 삭제 실패: ", error)
    }
}

// 메모 수정
async function editMemo(id) {
    const newText = prompt("수정할 내용을 입력하세요.")
    console.log(newText)

    if (!newText || newText.trim() === "") return

    try {
        const response = await fetch(`/memos/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: newText }) // text, newText 가 이름이 다르므로 둘 다 적어줘야함!
        })
        loadMemos()
    } catch (error) {
        console.log("메모 수정 실패: ", error)
    }
}

loadMemos()