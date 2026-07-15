import React from "react"

function User({ user }) {
    return (
        <div>
            <b>{user.userid}</b> <span>({user.name})</span>
        </div>
    )
}

function UserList() {
    const users = [
        {
            id: 1,
            userid: "apple",
            name: "김사과",
            email: "apple@apple.com"
        },
        {
            id: 2,
            userid: "banana",
            name: "반하나",
            email: "banana@banana.com"
        },
        {
            id: 3,
            userid: "orange",
            name: "오렌지",
            email: "orange@orange.com"
        }
    ]

    return (
        <div>
            <div>
                <b>{users[0].userid}</b> <span>({users[0].name})</span>
            </div>
            <div>
                <b>{users[1].userid}</b> <span>({users[1].name})</span>
            </div>
            <div>
                <b>{users[2].userid}</b> <span>({users[2].name})</span>
            </div>

            <User user={users[0]}/> {/* apple (김사과) */}
            <User user={users[1]}/> {/* banana (반하나) */}
            <User user={users[2]}/> {/* orange (오렌지) */}
            
            {/* React에서 () => ()는 화살표 함수의 암시적 반환(Implicit Return) 문법으로, 함수 실행 결과로 소괄호 () 안의 값을 즉시 반환(return)할 때 사용 */}
            {
                users.map((user) => (
                    <User user={user} key={user.id}/>
                ))
            }
        </div>
    )
}

export default UserList