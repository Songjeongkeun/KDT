
window.onload = function(){
    const ssn1 = document.getElementById("ssn1")
    ssn1.addEventListener("keyup", ()=>{
        if(ssn1.value.length >= 6){
            document.getElementById("ssn2").focus()
        }
    })

    const ssn = document.querySelectorAll(".ssn")
    ssn.forEach((s) => {
        // console.log(s)
        s.addEventListener("input", ()=>{
            document.getElementById("ssncheck").value = "n"
        })
    })
    // ssn 배열을 모두 탐색하면서 처리해주는 함수
}

function sample6_execDaumPostcode() {
        new kakao.Postcode({
            oncomplete: function(data) {
                // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

                // 각 주소의 노출 규칙에 따라 주소를 조합한다.
                // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
                var addr = ''; // 주소 변수
                var extraAddr = ''; // 참고항목 변수

                //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
                if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
                    addr = data.roadAddress;
                } else { // 사용자가 지번 주소를 선택했을 경우(J)
                    addr = data.jibunAddress;
                }

                // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
                if(data.userSelectedType === 'R'){
                    // 법정동명이 있을 경우 추가한다. (법정리는 제외)
                    // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
                    if(data.bname !== '' && /[동로가]$/.test(data.bname)){
                        extraAddr += data.bname;
                    }
                    // 건물명이 있고, 공동주택일 경우 추가한다.
                    if(data.buildingName !== '' && data.apartment === 'Y'){
                        extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                    }
                    // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
                    if(extraAddr !== ''){
                        extraAddr = ' (' + extraAddr + ')';
                    }
                    // 조합된 참고항목을 해당 필드에 넣는다.
                    document.getElementById("sample6_extraAddress").value = extraAddr;
                
                } else {
                    document.getElementById("sample6_extraAddress").value = '';
                }

                // 우편번호와 주소 정보를 해당 필드에 넣는다.
                document.getElementById('sample6_postcode').value = data.zonecode;
                document.getElementById("sample6_address").value = addr;
                // 커서를 상세주소 필드로 이동한다.
                document.getElementById("sample6_detailAddress").focus();
            }
        }).open();
    }

function sendit() {
    const userid = document.getElementById("userid")
    const userpw = document.getElementById("userpw")
    const userpw_re = document.getElementById("userpw_re")
    const name = document.getElementById("name")
    const hp = document.getElementById("hp")
    const email = document.getElementById("email")
    const ssncheck = document.getElementById("ssncheck")

    const expIdText = /^[A-Za-z0-9]{4,20}$/ // 정규식은 띄어쓰기를 하면 안된다.
    const expPwText = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$/
    const expNameText = /^[가-힣]+$/
    const expHpText = /^\d{3}-\d{3,4}-\d{4}$/
    const expEmailText = /^[A-Za-z0-9\-\.]+@[A-Za-z0-9\-]+\.[A-Za-z]+$/
    

    /*
        (?=.*) : 어디엔가 원하는 패턴이 하나라도 있어야 함
        (?=.*[A-Za-z]) : 영문자가 최소 한개 이상 있어야 함
        (?=.*\d) : 숫자가 최소 1개 이상 있어야 함
        (?=.*[!@#$%^&*()]) : 제시된 특수 문자가 최소 1개 이상 있어야 함
    */

    if (userid.value === "") {
        alert("아이디를 입력하세요")
        userid.focus()
        return false
    }

    if (!expIdText.test(userid.value)) {
        alert("아이디는 4자이상 20자이하의 영문자 또는 숫자로 입력하세요.")
        userid.focus()
        return false
    }

    if (!expPwText.test(userpw.value)) {
        alert("비밀번호는 8자이상 20자이하의 영문자, 숫자, 특수문자를 한 자이상 꼭 포함해야합니다.")
        userpw.focus()
        return false
    }

    if (userpw.value != userpw_re.value) {
        alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        userpw_re.focus()
        return false
    }

    if (!expNameText.test(name.value)) {
        alert("이름은 한글로 입력하세요.")
        name.focus()
        return false
    }

    if (!expHpText.test(hp.value)) {
        alert("휴대폰 번호 형식이 일치하지 않습니다\n 하이픈을 꼭 입력하세요.")
        hp.focus()
        return false
    }

    if (!expEmailText.test(email.value)) {
        alert("이메일 형식이 일치하지 않습니다..")
        email.focue()
        return false
    }

    if (ssncheck.value == "n"){
        alert("주민등록번호 검증버튼을 눌러주세요.")
        return false
    }

}

function checkSsn() {
    /*
    9 8 0 8 0 8 1 0 4 7 4 2 8
    2 3 4 5 6 7 8 9 2 3 4 5
    18 + 24 + 0 + 40 + 0 + 56 + 8 + 0 + 8 + 21 + 16 + 10 = 201
    201 % 11 = 3
    11 - 3 = 8
    */
    let ssncheck = document.getElementById("ssncheck")
    const ssn1 = document.getElementById("ssn1").value
    const ssn2 = document.getElementById("ssn2").value
    const ssn = ssn1 + ssn2.substring(0,6)
    const cond = Number(ssn2[6])

    const weight = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    let check = 0
    for(let i = 0; i < ssn.length; i++){
        check += (Number(ssn[i]) * weight[i])
    }
    check = (11 - (check % 11)) % 10
    
    if(check != cond){
        alert("유효하지 않은 주민등록 번호입니다.")
    }else{
        alert("유효한 주민등록 번호입니다.")
        ssncheck.value = "y"
    }
}