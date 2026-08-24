import { Router } from "express"
import {
  createHotel,
  createRoom,
  deleteHotel,
  deleteRoom,
  updateHotel,
  updateRoom,
} from "../controllers/admin.controller.js"
import { requireAdmin, requireAuth } from "../middlewares/auth.middleware.js"

const router = Router()

router.use(requireAuth, requireAdmin)

router.post("/hotels", createHotel)
router.patch("/hotels/:hotelId", updateHotel)
router.delete("/hotels/:hotelId", deleteHotel)
router.post("/hotels/:hotelId/rooms", createRoom)
router.patch("/rooms/:roomId", updateRoom)
router.delete("/rooms/:roomId", deleteRoom)

export default router

