import { Router } from "express"
import { createReservation, getMyReservation, getReservationById } from "../controllers/reservation.controller"
import { requireAuth } from "../middlewares/auth.middleware"

const router = Router() 

router.use(requireAuth)

router.post("/", createReservation)
router.get("/me", getMyReservation)
router.get("/:reservationId", getReservationById)


export default router