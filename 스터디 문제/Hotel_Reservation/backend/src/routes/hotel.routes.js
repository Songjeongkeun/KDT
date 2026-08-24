import { Router } from "express"
import { getHotelById, getHotels, getRegions, getRoomsByHotel } from "../controllers/hotel.controller.js"

const router = Router()

router.get("/regions", getRegions)
router.get("/", getHotels)
router.get("/:hotelId/rooms", getRoomsByHotel)
router.get("/:hotelId", getHotelById)

export default router
