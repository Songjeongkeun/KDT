import Hotel from "../models/Hotel.js"
import Room from "../models/Room.js"

const hotelFields = ["name", "region", "address", "description", "minPrice", "imageUrl", "amenities"]
const roomFields = ["name", "description", "price", "capacity", "quantity", "amenities", "imageUrl", "isActive"]

function pickFields(source, allowedFields) {
  return Object.fromEntries(
    allowedFields.filter((field) => source[field] !== undefined).map((field) => [field, source[field]])
  )
}

async function updateHotelMinPrice(hotelId) {
  const lowestRoom = await Room.findOne({ hotel: hotelId, isActive: true }).sort({ price: 1 })
  await Hotel.findByIdAndUpdate(hotelId, { minPrice: lowestRoom ? lowestRoom.price : 0 })
}

export async function createHotel(req, res, next) {
  try {
    const hotel = await Hotel.create(pickFields(req.body, hotelFields))
    return res.status(201).json({ success: true, data: hotel, message: "호텔이 등록되었습니다." })
  } catch (error) {
    next(error)
  }
}

export async function updateHotel(req, res, next) {
  try {
    const hotel = await Hotel.findByIdAndUpdate(
      req.params.hotelId,
      pickFields(req.body, hotelFields),
      { new: true, runValidators: true }
    )

    if (!hotel) return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })
    return res.status(200).json({ success: true, data: hotel, message: "호텔 정보가 수정되었습니다." })
  } catch (error) {
    next(error)
  }
}

export async function deleteHotel(req, res, next) {
  try {
    const hotel = await Hotel.findByIdAndDelete(req.params.hotelId)
    if (!hotel) return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })

    await Room.deleteMany({ hotel: hotel._id })
    return res.status(200).json({ success: true, message: "호텔과 소속 객실이 삭제되었습니다." })
  } catch (error) {
    next(error)
  }
}

export async function createRoom(req, res, next) {
  try {
    const hotel = await Hotel.findById(req.params.hotelId)
    if (!hotel) return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })

    const room = await Room.create({ ...pickFields(req.body, roomFields), hotel: hotel._id })
    await updateHotelMinPrice(hotel._id)
    return res.status(201).json({ success: true, data: room, message: "객실이 등록되었습니다." })
  } catch (error) {
    next(error)
  }
}

export async function updateRoom(req, res, next) {
  try {
    const room = await Room.findByIdAndUpdate(
      req.params.roomId,
      pickFields(req.body, roomFields),
      { new: true, runValidators: true }
    )

    if (!room) return res.status(404).json({ success: false, message: "객실을 찾을 수 없습니다." })
    await updateHotelMinPrice(room.hotel)
    return res.status(200).json({ success: true, data: room, message: "객실 정보가 수정되었습니다." })
  } catch (error) {
    next(error)
  }
}

export async function deleteRoom(req, res, next) {
  try {
    const room = await Room.findByIdAndDelete(req.params.roomId)
    if (!room) return res.status(404).json({ success: false, message: "객실을 찾을 수 없습니다." })

    await updateHotelMinPrice(room.hotel)
    return res.status(200).json({ success: true, message: "객실이 삭제되었습니다." })
  } catch (error) {
    next(error)
  }
}
