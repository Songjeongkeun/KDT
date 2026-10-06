# Mac 에 MySQL 과 Workbench 설치 및 설정

Mac (M칩) 컴퓨터에 MySQL 과 Workbench 설치하는 법

## 준비

Mac 에 homebrew 가 설치되어 있어야 한다.

> Homebrew는 맥에서 라이브러리/플러그인 등을 쉽게 설치하게 도와주는 패키징 매니저라고 할 수 있다.

Mac terminal 에서 다음 명령어 입력.

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 

설치가 완료되면 다음 명령어를 입력.

> - echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/"사용자명"/.zprofile
> - eval "$(/opt/homebrew/bin/brew shellenv)"

"사용자명" 은 Mac 의 사용자 이름으로 바꿔주면 된다.

설치가 완료되면 다음 명령어를 쳐서 설치가 잘 됐는지 확인.

> brew -v

homebrew 버전이 출력되면 올바르게 설치된 것이다.



## MySQL 설치

터미널에서 다음 명령어 입력

> brew install mysql

설치가 완료되었으면 제대로 설치되었는지, 그리고 버전을 확인하기 위해 다음 명령어를 입력

> mysql -V

아래 명령어를 입력해서 서버를 켜서 MySQL을 시작
그럼 서버가 켜지고 SUCCESS! 라고 나온다.

> mysql.server start



### MySQL 설정

다음 명령어를 입력해서 기본 설정 시작

> Mysql_secure_installation



**1. 비밀번호 복잡도 검사**

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough.

Would you like to setup VALIDATE PASSWORD component?
Press y|Y for Yes, any other key for No

비밀번호 복잡도 검사를 적용할 것인지 설정하는 과정입니다. 복잡도 검사를 적용하게 된다면 다음과 같은 비밀번호 조건이 붙습니다.
\- 최소 8자리 이상의 비밀번호
\- 최소 1개의 영문자
\- 최소 1개의 특수문자
\- 최소 1개의 숫자

간단하게 비밀번호를 설정해 두실 분들은 No로 진행하면 됩니다.

이후 설정할 비밀번호 입력이 나오는데 입력해도 보이지 않는 것이 정상입니다.

------

**2. 익명의 사용자 삭제**

By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No)

익명의 사용자를 삭제할 것인지 물어봅니다.
설치 과정에서 테스트와 설치를 좀 더 원활하게 진행하기 위해 생성되었던 계정인데 Yes로 삭제해 줍니다.

------

**3. root 계정 원격 접속 차단**

 Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No)

root 계정을 원격(외부)에서의 접속을 차단할 것인지 묻습니다. 일반적인 경우라면 root 계정은 원격 접속은 차단해 두는 것이 권장됩니다. Yes로 차단을 하여 주시면 됩니다. 원격작업이 필요한 경우는 root 말고 db 계정을 따로 생성하여 원격 권한을 주는 것이 가장 바람직합니다.

------

**4. 테스트 데이터베이스 삭제**

By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.

Remove test database and access to it? (Press y|Y for Yes, any other key for No)

테스트 데이터베이스를 삭제할 것인지 물어봅니다.
필요 없으니 과감히 Yes로 버려주셔도 됩니다.

------

**5. 현재까지의 변경사항 즉시 적용**
 
Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.
 
Reload privilege tables now? (Press y|Y for Yes, any other key for No)

 

Yes를 통해 변경사항을 즉시 적용시켜 줍니다.



여기까지 완료되면 All done! 메세지 출력.



### MySQL 사용

다음 명령어 입력 후 비밀번호를 입력하면 MySQL 사용 가능

> mysql -u root -p

MySQL 을 종료하는 명령어는 다음과 같다.

> quit 또는 exit

추가로, 다음 명령어를 입력하면 MySQL 서버가 재부팅 상관없이 항상 켜져있게 한다.

> brew services start mysql



## Wokrbench 설치하기

[Workbench 다운로드 사이트](https://dev.mysql.com/downloads/workbench/)에 접속하여 버전에 맞게 설치하면 됩니다

![img](/Users/songjeong-geun/Desktop/KDT/workbench1 .png)

 Download 버튼을 누르면 페이지가 넘어가며 로그인 혹은 회원가입 버튼이 크게 보이는데,
무시하고 아래 No thanks, just start my download 버튼을 누르면 된다.



### connection 생성

![img](/Users/songjeong-geun/Desktop/KDT/workbench2.png)



![image-20260604103649321](/Users/songjeong-geun/Desktop/KDT/workbench3.png)

**Connection Name** 을 지정해주고 **OK** 눌러준다.