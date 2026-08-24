import mongoose from "mongoose"
import bcrypt from "bcrypt"

const userSchema = new mongoose.Schema(
  {
    email: {
      type: String,
      required: [true, "이메일은 필수입니다."],
      unique: true,
      trim: true,
      lowercase: true,
    },
    nickname: {
      type: String,
      required: [true, "닉네임은 필수입니다."],
      trim: true,
      minlength: [2, "닉네임은 2자 이상이어야 합니다."],
      maxlength: [20, "닉네임은 20자 이하여야 합니다."],
    },
    password: {
      type: String,
      required: [true, "비밀번호는 필수입니다."],
      minlength: [5, "비밀번호는 5자 이상이어야 합니다."],
    },
    // 일반 사용자는 USER, 호텔·객실을 관리하는 계정은 ADMIN입니다.
    role: {
      type: String,
      enum: ["USER", "ADMIN"],
      default: "USER",
    },
  },
  { timestamps: true }
)

// 이미 해시된 비밀번호를 다시 해시하지 않도록 수정 여부를 먼저 확인합니다.
userSchema.pre("save", async function hashPassword(next) {
  if (!this.isModified("password")) return next()

  this.password = await bcrypt.hash(this.password, 12)
  next()
})

// 로그인 시 입력 비밀번호와 DB의 해시 비밀번호를 안전하게 비교합니다.
userSchema.methods.comparePassword = function comparePassword(password) {
  return bcrypt.compare(password, this.password)
}

export default mongoose.model("User", userSchema)
