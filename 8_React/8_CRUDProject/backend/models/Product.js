import mongoose from "mongoose"

const productSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: [true, "상품명은 필수입니다."],    // 꼭 들어가야하나 안들어가도 되냐에 대한 정의 true: 필수로 들어가야 된다.
            trim: true
        },
        price: {
            type: Number,
            requried: [true, "가격은 필수입니다."],
            // create 할때만 적용되는 옵션
            min: [0, "가격은 0원 이상이어야 합니다."]
        }
    },
    {
        // 입력시간, 수정시간을 자동으로 설정
        timestamps: true
    }

)

const Product = mongoose.model("Product", productSchema)

export default Product