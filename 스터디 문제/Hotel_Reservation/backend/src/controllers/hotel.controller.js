import Hotel from "../models/Hotel.js"
import Room from "../models/Room.js"

// 정규식 특수문자를 문자 그대로 검색하도록 처리합니다.
function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
}

export async function getHotels(req, res, next) {
  try {
    const { region, keyword, sort } = req.query
    const filter = {}

    if (region?.trim()) {
      filter.region = { $regex: escapeRegExp(region.trim()), $options: "i" }
    }

    if (keyword?.trim()) {
      filter.name = { $regex: escapeRegExp(keyword.trim()), $options: "i" }
    }

    const sortOption = {
      price: { minPrice: 1, _id: 1 },
      rating: { ratingAverage: -1, ratingCount: -1, _id: 1 },
    }[sort] || { createdAt: -1 }

    const hotels = await Hotel.find(filter).sort(sortOption)

    return res.status(200).json({
      success: true,
      data: hotels,
      meta: { count: hotels.length },
    })
  } catch (error) {
    next(error)
  }
}

export async function getRegions(req, res, next) {
  try {
    const regions = await Hotel.distinct("region")
    return res.status(200).json({ success: true, data: regions.sort() })
  } catch (error) {
    next(error)
  }
}

export async function getHotelById(req, res, next) {
  try {
    const hotel = await Hotel.findById(req.params.hotelId)

    if (!hotel) {
      return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })
    }

    // 객실은 가격순으로 함께 내려 주어 상세 페이지가 한 번의 요청으로 완성됩니다.
    const rooms = await Room.find({ hotel: hotel._id }).sort({ price: 1 })

    return res.status(200).json({ success: true, data: { hotel, rooms } })
  } catch (error) {
    // MongoDB ObjectId 형식이 아닌 URL도 '호텔 없음'으로 처리합니다.
    if (error.name === "CastError") {
      return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })
    }
    next(error)
  }
}

export async function getRoomsByHotel(req, res, next) {
  try {
    const hotel = await Hotel.findById(req.params.hotelId)

    if (!hotel) {
      return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })
    }

    const rooms = await Room.find({ hotel: hotel._id }).sort({ price: 1 })
    return res.status(200).json({ success: true, data: rooms })
  } catch (error) {
    if (error.name === "CastError") {
      return res.status(404).json({ success: false, message: "호텔을 찾을 수 없습니다." })
    }
    next(error)
  }
}
