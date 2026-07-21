import { Link } from "react-router-dom"

export default function Navbar(){
    return(
        <>
        <nav>
            <Link to="/">Home</Link>
            <Link to="/videos">Videos</Link>
        </nav>
        <hr />
        <div>
            <h1 className="text-8xl">메뉴</h1>
            <button className="bg-blue-500 rounded-xl px-2">버튼</button>
        </div>
        </>
    )
}