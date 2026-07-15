import React, { useState } from "react"

function InputUser() {
    // inputs = {userid: "", password: ""}
    const [inputs, setInputs] = useState({
        userid: "",
        password: ""
    })
    const { userid, password } = inputs

    const onChange = (e) => {
        const { value, name } = e.target
        setInputs({
            ...inputs,
            [name]: value
        })
    }

    const onReset = () => {
        setInputs({
            userid: "", password: ""
        })
    }

    return (
        <div>
            <input name="userid" placeholder="아이디를 입력하세요" value={userid} onChange={onChange} />
            <input type="password" name="password" placeholder="비밀번호를 입력하세요" value={password} onChange={onChange}/>
            <button onClick={onReset}>초기화</button>
            <div>
                <b>값: {userid}({password})</b>
            </div>
        </div>
    )
}

export default InputUser