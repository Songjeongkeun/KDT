import Hotel from "../models/Hotel"
import Reservation from "../models/Reservation.js"
import Room from "../models/Room.js"

function getNight(checkIn, checkOut) {
    const start = new Date(`${checkIn}T00:00:00.000Z`)
    const end = new Date(`${checkOut}T00:00:00.000Z`)

    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime)) {
        return 0
    }

    return Math.ceil((end - start) / (1000 * 60 * 60 * 24))
}

export async function createReservation(req, res, next) {
    try {
        const { roomId, checkIn, checkOut, guests } = req.body

        if (!roomId || !checkIn || !checkOut || !guests) {
            return res.status(400).json({
                success: false,
                message: "객실, 체크인, 체크아웃, 인원을 모드 입력해 주세요."
            })
        }

        const nights = getNight(checkIn, checkOut)

        if (nights < 1) {
            return res.status(400).json({
                success: false,
                message: "체크아웃 날짜는 체크인 날짜보다 늦어야 합니다."
            })
        }

        const room = await Room.findById(roomId)

        if (!room || !room.isActive) {
            return res.status(400).json({
                success: false,
                message: "예약 가능한 객실을 찾을 수 없습니다."
            })
        }

        if (Number(guests) > room.capacity) {
            return res.status(400).json({
                success: false,
                message: `이 객실은 최대 ${room.capacity}명까지 예약할 수 있습니다.`
            })
        }

        const hotel = await Hotel.findById(room.hotel)

        if (!hotel) {
            return res.status(404).json({
                success: false,
                message: "호텔을 찾을 수 없습니다."
            })
        }

        const usedRoomCount = await Reservation.countDocuments({
            room: room._id,
            status: "CONFIRMED",
            checkIn: { $lt: new Date(checkOut) },
            checkOut: { $gt: new Date(checkIn) },
        })

        if (usedRoomCount >= room.capacity) {
            return res.status(409).json({
                success: false,
                message: "선택한 기간에는 남은 객실이 없습니다."
            })
        }

        const reservation = await Reservation.create({
            user: req.user._id,
            hotel: hotel._id,
            room: room._id,
            checkIn,
            checkOut,
            guests: Number(guests),
            nights,
            totalPrice: room.price * nights
        })

        return res.status(201).json({
            success: true,
            data: reservation,
            message: "예약이 완료되었습니다."
        })
    } catch (error) {
        next(error)
    }

}

export async function getMyReservation(req, res, next) {
    try {
        // populate: 주로 Mongoose(MongoDB ODM)에서 다른 컬렉션의 객체 아이디(ObjectId)를 실제 데이터로 불러오는 기능을 뜻한다.
        const reservations = await Reservation.find({ user: req.user._id })
            .populate("hotel", "name region address")
            .populate("room", "name price capacity")
            .sort({ createdAt: -1 })

        return res.status(200).json({
            success: true,
            data: reservations,
        })
    } catch (error) {
        next(error)
    }
}

export async function getReservationById(req, res, next) {
    try {
        const reservation = await Reservation.findOne({
            _id: req.params.reservationId,
            user: req.user._id
        })
            .populate("hotel", "name region address")
            .populate("room", "name price capacity amenities")

        if (!reservation) {
            return res.status(400).json({
                success: false,
                message: "예약 정보를 찾을 수 없습니다."
            })
        }

        return res.status(200).json({
            success: true,
            data: reservation
        })
    } catch (error) {
        next(error)
    }
}