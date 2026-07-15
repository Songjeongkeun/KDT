// 데이터베이스 선택 및 생성
use("AIdb")

// db : AIdb
// students : collection(컬렉션이 존재하지 않으면, 생성하면서 삽입)
// insertOne() : 문서를 한개 넣는 메서드
// 일부만 실행시키고 싶을 땐 drag 후 실행
db.students.insertOne({
    userid: "apple",
    name: "김사과",
    age: 20,
    major: "AI",
    score: 88
})

// insertMany(): 여러 문서를 한 번에 넣음 (배열을 사용)
use("AIdb")
db.students.insertMany([
    { name: "김사과", age: 20, major: "AI", score: 88 },
    { name: "반하나", age: 25, major: "Backend", score: 91 },
    { name: "오렌지", age: 30, major: "Frontend", score: 77 },
])

// 전체 조회
// find(): 문서를 조회하는 기본 메서드
// {}: 조건이 없다는 뜻
use("AIdb")
db.students.find({})

/*
    ObjectId   
    - 각 문서의 12바이트(24자리 16진수) 고유한 ID로 사용되는 데이터 타입
    - SQL의 기본키와 비슷한 역할을 함
    - 각 문서의 _id 필드를 기본적으로 생성하며, 특별히 지정하지 않으면 자동으로 ObjectId 형태로 생성
*/
