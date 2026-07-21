import { useState } from "react"
import { useNavigate } from "react-router-dom"
import styled, { css } from "styled-components"

const Container = styled.div`
    display: flex;
`

const Button = styled.button`
    background: black;
    border-radius: 3px;
    border: 3px solid deeppink;
    color: white;
    margin: 0 1em;
    padding: 0.25em 1em;  
    ${
        (props) => props.primary && 
        css`
            background: deepskyblue;
            color: ivory;
        `
    }
`

export default function Videos(){
    const [text, setText] = useState("")
    const navigate = useNavigate()

    const handleChange = (e) => {
        setText(e.target.value)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        setText("")
        navigate(`/videos/${text}`)
    }

    return(
        <div>
            Videos
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Video id: " value={text} onChange={handleChange} />
            </form>

            <hr />
            <Container>
                <Button>기본버튼</Button>
                <Button primary>Primary 버튼</Button>
            </Container>
        </div>
    )
}