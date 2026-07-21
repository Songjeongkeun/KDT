import styles from "./Home.module.css"
import "../App.css"

export default function Home(){
    return(
        <div>
            Home <button className={styles.button}>버튼1</button>
            <button className="button">버튼2</button>
        </div>
    )
}