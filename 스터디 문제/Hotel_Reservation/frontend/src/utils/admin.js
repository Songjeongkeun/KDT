export const emptyHotel = {
  name: "",
  region: "",
  address: "",
  description: "",
  minPrice: "",
  amenities: "",
}

export const emptyRoom = {
  name: "",
  description: "",
  price: "",
  capacity: "2",
  quantity: "1",
  amenities: "",
  isActive: true,
}

export const priceFormatter = new Intl.NumberFormat("ko-KR")

function parseAmenities(value) {
  return value.split(",").map((item) => item.trim()).filter(Boolean)
}

export function toHotelPayload(form) {
  return {
    ...form,
    minPrice: Number(form.minPrice),
    amenities: parseAmenities(form.amenities),
  }
}

export function toRoomPayload(form) {
  return {
    ...form,
    price: Number(form.price),
    capacity: Number(form.capacity),
    quantity: Number(form.quantity),
    amenities: parseAmenities(form.amenities),
  }
}

export function toHotelForm(hotel) {
  return {
    name: hotel.name,
    region: hotel.region,
    address: hotel.address,
    description: hotel.description,
    minPrice: String(hotel.minPrice),
    amenities: hotel.amenities.join(", "),
  }
}

export function toRoomForm(room) {
  return {
    name: room.name,
    description: room.description,
    price: String(room.price),
    capacity: String(room.capacity),
    quantity: String(room.quantity ?? 1),
    amenities: room.amenities.join(", "),
    isActive: room.isActive,
  }
}
