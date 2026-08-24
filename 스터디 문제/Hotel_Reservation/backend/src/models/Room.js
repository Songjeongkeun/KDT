import mongoose from "mongoose"

const roomSchema = new mongoose.Schema(
  {
    // 객실이 어느 호텔 소속인지 저장합니다.
    hotel: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Hotel",
      required: [true, "호텔 ID는 필수입니다."],
      index: true,
    },
    name: {
      type: String,
      required: [true, "객실명은 필수입니다."],
      trim: true,
    },
    description: {
      type: String,
      required: [true, "객실 소개는 필수입니다."],
      trim: true,
      maxlength: [500, "객실 소개는 500자 이하여야 합니다."],
    },
    price: {
      type: Number,
      required: [true, "객실 가격은 필수입니다."],
      min: [0, "객실 가격은 0 이상이어야 합니다."],
    },
    capacity: {
      type: Number,
      required: [true, "최대 인원은 필수입니다."],
      min: [1, "최대 인원은 1명 이상이어야 합니다."],
    },
    // 같은 등급 객실을 여러 개 보유할 수 있도록 수량을 저장합니다.
    // 예약 기능에서는 날짜별 예약 건수와 이 값을 비교해 남은 객실 수를 계산합니다.
    quantity: {
      type: Number,
      required: [true, "객실 수는 필수입니다."],
      min: [1, "객실 수는 1개 이상이어야 합니다."],
      default: 1,
    },
    amenities: {
      type: [String],
      default: [],
    },
    imageUrl: {
      type: String,
      default: "",
      trim: true,
    },

    isActive: {
      type: Boolean,
      default: true,
    },
  },
  { timestamps: true }
)

roomSchema.index({ hotel: 1, name: 1 }, { unique: true })
roomSchema.index({ hotel: 1, price: 1 })

export default mongoose.model("Room", roomSchema)
