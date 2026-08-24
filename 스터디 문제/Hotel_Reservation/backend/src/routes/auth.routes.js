import { Router } from "express"
import { checkEmail, login, signup } from "../controllers/auth.controller.js"

const router = Router()

router.post("/check-email", checkEmail)
router.post("/signup", signup)
router.post("/login", login)

export default router

