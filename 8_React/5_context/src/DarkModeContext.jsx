import React from "react"
import { useEffect } from "react"
import { useState } from "react"
import { createContext } from "react"

export const DarkModeContext = createContext()

export function DarkModeProvider({ children }) {
    const [darkMode, setDarkMode] = useState(() => {
        const savedDarkMode = localStorage.getItem("darkMode")
        return savedDarkMode === "true"
    })

    const toggleDarkMode = () => {
        setDarkMode((prevDarkMode) => !prevDarkMode)
    }

    useEffect(() => {
        localStorage.setItem("darkMode", String(darkMode))
        document.documentElement.classList.toggle("dark", darkMode)
    }, [darkMode])

    return (
        <DarkModeContext.Provider value={{ darkMode, toggleDarkMode }}>
            {children}
        </DarkModeContext.Provider>
    )
}