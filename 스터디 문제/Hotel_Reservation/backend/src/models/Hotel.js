import mongoose from "mongoose"

const hotelSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "호텔명은 필수입니다."],
      trim: true,
    },
    region: {
      type: String,
      required: [true, "지역은 필수입니다."],
      trim: true,
    },
    address: {
      type: String,
      required: [true, "주소는 필수입니다."],
      trim: true,
    },
    description: {
      type: String,
      required: [true, "호텔 소개는 필수입니다."],
      trim: true,
      maxlength: [500, "호텔 소개는 500자 이하여야 합니다."],
    },
    // 객실을 추가할 때 가장 저렴한 객실 가격으로 갱신할 값입니다.
    minPrice: {
      type: Number,
      required: [true, "최저 가격은 필수입니다."],
      min: [0, "가격은 0 이상이어야 합니다."],
    },
    imageUrl: {
      type: String,
      default: "",
      trim: true,
    },
    amenities: {
      type: [String],
      default: [],
    },
    // 후기 기능 구현 시 이 두 값을 갱신해 평점순 정렬에 사용합니다.
    ratingAverage: {
      type: Number,
      default: 0,
      min: 0,
      max: 5,
    },
    ratingCount: {
      type: Number,
      default: 0,
      min: 0,
    },
  },
  { timestamps: true }
)

// 지역 검색과 가격/평점 정렬을 빠르게 처리할 수 있도록 인덱스를 둡니다.
hotelSchema.index({ region: 1 })
hotelSchema.index({ minPrice: 1 })
hotelSchema.index({ ratingAverage: -1 })

export default mongoose.model("Hotel", hotelSchema)

