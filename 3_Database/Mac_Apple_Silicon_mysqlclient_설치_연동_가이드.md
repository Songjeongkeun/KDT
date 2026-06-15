# Mac Apple Silicon에서 mysqlclient 설치하고 MySQL 연동하기

`mysqlclient`는 Python에서 MySQL 또는 MariaDB에 연결할 때 사용하는 데이터베이스 드라이버이다.

패키지는 `mysqlclient`라는 이름으로 설치하지만 Python 코드에서는 다음과 같이 불러온다.

```python
import MySQLdb
```

Apple Silicon이 탑재된 Mac에서는 Python, Homebrew, MySQL 클라이언트 라이브러리의 CPU 아키텍처가 모두 일치해야 한다.

```text
Apple Silicon Python
        ↓
mysqlclient
        ↓
MySQL C Client Library
        ↓
MySQL Server
```

이 글에서는 M1, M2, M3, M4 등 Apple Silicon Mac을 기준으로 다음 내용을 정리한다.

- 개발 환경 확인
- Homebrew 설치 확인
- 가상환경 생성
- `mysqlclient` 설치
- MySQL 서버 연결
- Jupyter Notebook 연동
- 자주 발생하는 오류와 해결 방법

---

## 1. mysqlclient가 설치되기까지 필요한 구성

`mysqlclient`는 순수 Python 패키지가 아니다.  
일부 코드가 C로 작성되어 있기 때문에 설치 과정에서 컴파일러와 MySQL 클라이언트 개발 파일을 사용한다.

필요한 구성은 다음과 같다.

| 구성 | 역할 |
| --- | --- |
| Python | Python 프로그램 실행 |
| pip | `mysqlclient` 패키지 설치 |
| C 컴파일러 | C 확장 모듈 빌드 |
| `pkg-config` | MySQL 헤더와 라이브러리 위치 검색 |
| MySQL Client Library | MySQL 서버와 통신 |
| MySQL Server | 실제 데이터 저장 및 SQL 실행 |

설치 흐름은 다음과 같다.

```text
Homebrew로 MySQL Client와 pkg-config 설치
                    ↓
가상환경 활성화
                    ↓
pip install mysqlclient
                    ↓
import MySQLdb
                    ↓
MySQL 서버 연결
```

---

## 2. Apple Silicon 환경 확인

터미널에서 CPU 아키텍처를 확인한다.

```bash
uname -m
```

Apple Silicon을 네이티브로 사용하고 있다면 다음과 같이 출력된다.

```text
arm64
```

`x86_64`가 출력된다면 터미널이나 Python이 Rosetta 환경으로 실행되고 있을 수 있다.

### Homebrew 위치 확인

```bash
which brew
brew --prefix
```

Apple Silicon용 Homebrew의 기본 경로는 다음과 같다.

```text
/opt/homebrew/bin/brew
/opt/homebrew
```

Intel Mac용 Homebrew 경로는 일반적으로 `/usr/local`이다.

```text
Apple Silicon Homebrew: /opt/homebrew
Intel Homebrew:         /usr/local
```

M칩 Mac에서 `/usr/local/bin/brew`를 사용하고 있다면 Intel용 Homebrew가 설치되어 있을 가능성이 있다.

### Python 아키텍처 확인

```bash
python3 -c "import platform; print(platform.machine())"
```

권장 출력:

```text
arm64
```

Python 실행 파일의 위치도 확인한다.

```bash
which python3
python3 --version
```

Homebrew Python은 보통 `/opt/homebrew/bin/python3`에 있고, `pyenv`를 사용한다면 사용자 홈 디렉터리 아래의 `.pyenv` 경로가 나온다.

중요한 점은 경로 자체보다 Python이 `arm64`로 실행되는지 여부이다.

---

## 3. Homebrew 설치

Homebrew가 없다면 공식 설치 명령으로 설치한다.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치 후 Apple Silicon Homebrew를 셸 환경에 추가한다.

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

설치 확인:

```bash
brew --version
brew --prefix
```

---

## 4. Command Line Tools 설치

`mysqlclient`를 소스에서 빌드해야 하는 경우 C 컴파일러가 필요하다.

다음 명령으로 Apple Command Line Tools 설치를 시작한다.

```bash
xcode-select --install
```

이미 설치되어 있다면 다음 명령으로 경로를 확인할 수 있다.

```bash
xcode-select -p
clang --version
```

---

## 5. 설치 방식 선택

두 가지 설치 방식 중 하나를 선택한다.

| 방식 | 설치 대상 | 권장 상황 |
| --- | --- | --- |
| 방법 A | MySQL 서버와 클라이언트 | Mac에서 MySQL 서버도 직접 실행할 때 |
| 방법 B | MySQL 클라이언트만 | 원격 DB 또는 별도 MySQL 서버에 연결할 때 |

처음 학습하는 환경이라면 **방법 A**가 가장 단순하다.

---

## 6. 방법 A: MySQL 서버까지 설치

MySQL 서버, 클라이언트 라이브러리와 `pkg-config`를 설치한다.

```bash
brew install mysql pkg-config
```

MySQL 서비스를 실행한다.

```bash
brew services start mysql
```

서비스 상태 확인:

```bash
brew services list
```

직접 실행하고 중지할 수도 있다.

```bash
mysql.server start
mysql.server stop
```

MySQL 접속 확인:

```bash
mysql -u root -p
```

비밀번호가 없는 초기 환경이라면 다음 명령으로 접속될 수도 있다.

```bash
mysql -u root
```

MySQL 기본 보안 설정:

```bash
mysql_secure_installation
```

---

## 7. 방법 B: MySQL Client만 설치

MySQL 서버가 이미 다른 곳에 있거나 클라이언트 라이브러리만 필요하다면 다음처럼 설치한다.

```bash
brew install mysql-client pkg-config
```

Homebrew의 `mysql-client`는 `keg-only` 패키지다.  
다른 프로그램과 충돌하지 않도록 기본 PATH에 자동 연결되지 않는다.

현재 터미널 세션에 경로를 설정한다.

```bash
export PATH="$(brew --prefix mysql-client)/bin:$PATH"
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
```

계속 적용하려면 `~/.zshrc`에 추가한다.

```bash
echo 'export PATH="$(brew --prefix mysql-client)/bin:$PATH"' >> ~/.zshrc
echo 'export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"' >> ~/.zshrc
source ~/.zshrc
```

설정 확인:

```bash
which mysql
pkg-config --cflags mysqlclient
pkg-config --libs mysqlclient
```

Apple Silicon 환경에서는 보통 `/opt/homebrew` 아래의 경로가 출력된다.

---

## 8. Python 가상환경 만들기

프로젝트별로 패키지 버전을 분리하기 위해 가상환경을 사용한다.

```bash
mkdir mysql-python-project
cd mysql-python-project

python3 -m venv .venv
source .venv/bin/activate
```

가상환경이 활성화되면 터미널 앞에 `(.venv)`가 표시된다.

```text
(.venv) user@Mac mysql-python-project %
```

Python과 pip가 가상환경을 가리키는지 확인한다.

```bash
which python
which pip
python --version
python -m pip --version
```

경로 예시:

```text
/프로젝트경로/mysql-python-project/.venv/bin/python
/프로젝트경로/mysql-python-project/.venv/bin/pip
```

pip 관련 도구를 업데이트한다.

```bash
python -m pip install --upgrade pip setuptools wheel
```

---

## 9. mysqlclient 설치

MySQL 서버 전체를 설치한 경우:

```bash
python -m pip install mysqlclient
```

`mysql-client`만 설치한 경우에는 `PKG_CONFIG_PATH`를 확인한 뒤 설치한다.

```bash
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
python -m pip install mysqlclient
```

설치 확인:

```bash
python -m pip show mysqlclient
```

Python import 확인:

```bash
python -c "import MySQLdb; print('mysqlclient 설치 성공')"
```

출력:

```text
mysqlclient 설치 성공
```

---

## 10. MySQL 데이터베이스와 계정 준비

root 계정 대신 애플리케이션 전용 계정을 사용하는 것이 좋다.

MySQL에 관리자 계정으로 접속한다.

```bash
mysql -u root -p
```

데이터베이스를 생성한다.

```sql
CREATE DATABASE ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

학습용 사용자를 생성한다.

```sql
CREATE USER 'python_app'@'localhost'
IDENTIFIED BY '안전한_비밀번호';
```

`ai` 데이터베이스 권한을 부여한다.

```sql
GRANT ALL PRIVILEGES
ON ai.*
TO 'python_app'@'localhost';
```

계정 확인:

```sql
SELECT user, host, plugin
FROM mysql.user
WHERE user = 'python_app';
```

MySQL 8 이상의 기본 인증 플러그인은 일반적으로 `caching_sha2_password`이다.

---

## 11. Python에서 연결 테스트

비밀번호를 코드에 직접 넣지 않고 환경변수를 사용한다.

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=python_app
export DB_PASSWORD='안전한_비밀번호'
export DB_NAME=ai
```

연결 테스트 코드:

```python
import os
import MySQLdb


db = MySQLdb.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    charset="utf8mb4",
)

cur = db.cursor()

try:
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("MySQL 연결 성공")
    print("MySQL 버전:", version[0])
finally:
    cur.close()
    db.close()
```

출력 예시:

```text
MySQL 연결 성공
MySQL 버전: 8.x.x
```

---

## 12. 테이블 생성과 CRUD 테스트

```python
import os
import MySQLdb


db = MySQLdb.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    charset="utf8mb4",
)

cur = db.cursor(MySQLdb.cursors.DictCursor)

try:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS voca (
            eng VARCHAR(50) PRIMARY KEY,
            kor VARCHAR(100) NOT NULL,
            lev INT NOT NULL DEFAULT 1
        )
        """
    )

    cur.execute(
        """
        INSERT INTO voca (eng, kor, lev)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            kor = VALUES(kor),
            lev = VALUES(lev)
        """,
        ("apple", "사과", 1),
    )

    db.commit()

    cur.execute(
        """
        SELECT eng, kor, lev
        FROM voca
        ORDER BY eng
        """
    )

    for word in cur.fetchall():
        print(word)
except Exception:
    db.rollback()
    raise
finally:
    cur.close()
    db.close()
```

출력 예시:

```text
{'eng': 'apple', 'kor': '사과', 'lev': 1}
```

---

## 13. Jupyter Notebook에서 사용하기

터미널에서는 import가 되는데 Jupyter에서 `ModuleNotFoundError`가 발생하는 경우가 많다.  
대부분 Jupyter 커널과 `mysqlclient`를 설치한 Python 환경이 다르기 때문이다.

가상환경을 활성화한다.

```bash
source .venv/bin/activate
```

Jupyter와 커널 패키지를 설치한다.

```bash
python -m pip install jupyter ipykernel
```

가상환경을 Jupyter 커널로 등록한다.

```bash
python -m ipykernel install \
    --user \
    --name mysql-python \
    --display-name "Python (mysqlclient)"
```

Jupyter Notebook을 실행한다.

```bash
jupyter notebook
```

Notebook 메뉴에서 다음 커널을 선택한다.

```text
Kernel
  → Change Kernel
  → Python (mysqlclient)
```

Notebook에서 현재 Python 경로 확인:

```python
import sys

print(sys.executable)
```

가상환경 경로가 출력되어야 한다.

```text
/프로젝트경로/.venv/bin/python
```

Notebook 안에서 설치할 때는 현재 커널의 Python을 명시한다.

```ipython
import sys

!{sys.executable} -m pip install mysqlclient
```

---

## 14. 설치 진단 명령 모음

오류가 발생하면 다음 명령부터 확인한다.

```bash
uname -m
python -c "import platform; print(platform.machine())"

which brew
brew --prefix

which python
python --version
python -m pip --version

which pkg-config
pkg-config --version
pkg-config --cflags mysqlclient
pkg-config --libs mysqlclient

brew list --versions mysql mysql-client pkg-config
```

정상적인 Apple Silicon 환경은 대체로 다음 조건을 만족한다.

```text
CPU:          arm64
Python:       arm64
Homebrew:     /opt/homebrew
mysql-client: /opt/homebrew/opt/mysql-client
```

---

# 자주 발생하는 오류와 해결 방법

## 오류 1. `ModuleNotFoundError: No module named 'MySQLdb'`

오류:

```text
ModuleNotFoundError: No module named 'MySQLdb'
```

### 원인

- 현재 Python 환경에 `mysqlclient`가 설치되지 않았다.
- 다른 Python 또는 다른 가상환경에 설치했다.
- Jupyter가 다른 커널을 사용하고 있다.

### 해결

현재 Python 경로를 확인한다.

```bash
which python
python -m pip --version
```

같은 Python을 이용해 설치한다.

```bash
python -m pip install mysqlclient
```

설치 확인:

```bash
python -m pip show mysqlclient
python -c "import MySQLdb; print(MySQLdb)"
```

Jupyter에서는 다음 코드를 확인한다.

```python
import sys

print(sys.executable)
```

---

## 오류 2. `pkg-config: command not found`

오류 예시:

```text
pkg-config: command not found
```

### 원인

`mysqlclient`가 MySQL 헤더와 라이브러리 위치를 찾을 때 사용하는 `pkg-config`가 설치되지 않았다.

### 해결

```bash
brew install pkg-config
```

설치 확인:

```bash
which pkg-config
pkg-config --version
```

그다음 다시 설치한다.

```bash
python -m pip install mysqlclient
```

---

## 오류 3. `Can not find valid pkg-config name`

오류 예시:

```text
Exception: Can not find valid pkg-config name.
Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually
```

또는:

```text
Package mysqlclient was not found in the pkg-config search path
```

### 원인

- `mysql-client`가 설치되지 않았다.
- `mysql-client`가 keg-only라서 `pkg-config` 검색 경로에 포함되지 않았다.

### 해결

```bash
brew install mysql-client pkg-config
```

`PKG_CONFIG_PATH`를 설정한다.

```bash
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
```

정상 확인:

```bash
pkg-config --cflags mysqlclient
pkg-config --libs mysqlclient
```

다시 설치한다.

```bash
python -m pip install mysqlclient
```

---

## 오류 4. `mysql.h file not found`

오류 예시:

```text
fatal error: 'mysql.h' file not found
```

### 원인

컴파일러가 MySQL 헤더 파일을 찾지 못했다.

### 해결 방법 1

MySQL 클라이언트와 `pkg-config`를 설치하고 경로를 설정한다.

```bash
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
python -m pip install mysqlclient
```

### 해결 방법 2

공식 `mysqlclient` 빌드 설정 방식으로 컴파일 옵션을 직접 전달한다.

```bash
export MYSQLCLIENT_CFLAGS="$(pkg-config mysqlclient --cflags)"
export MYSQLCLIENT_LDFLAGS="$(pkg-config mysqlclient --libs)"

python -m pip install mysqlclient
```

---

## 오류 5. `ld: library 'mysqlclient' not found`

오류 예시:

```text
ld: library 'mysqlclient' not found
clang: error: linker command failed
```

### 원인

헤더는 찾았지만 링커가 MySQL 클라이언트 라이브러리를 찾지 못했다.

### 해결

```bash
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
export MYSQLCLIENT_CFLAGS="$(pkg-config mysqlclient --cflags)"
export MYSQLCLIENT_LDFLAGS="$(pkg-config mysqlclient --libs)"

python -m pip install --no-cache-dir mysqlclient
```

`mysql` 전체 패키지를 설치했다면 다음 경로도 확인한다.

```bash
brew --prefix mysql
pkg-config --libs mysqlclient
```

---

## 오류 6. `clang: error` 또는 컴파일러 관련 오류

오류 예시:

```text
error: command 'clang' failed
```

### 원인

- Command Line Tools가 설치되지 않았다.
- Command Line Tools 설치가 손상되었다.
- 빌드에 필요한 헤더 또는 라이브러리가 없다.

### 해결

```bash
xcode-select --install
```

설치 상태 확인:

```bash
xcode-select -p
clang --version
```

필요한 Homebrew 패키지도 확인한다.

```bash
brew install mysql-client pkg-config
```

---

## 오류 7. `mach-o file, but is an incompatible architecture`

오류 예시:

```text
mach-o file, but is an incompatible architecture
have 'x86_64', need 'arm64'
```

또는:

```text
building for macOS-arm64 but attempting to link with file built for macOS-x86_64
```

### 원인

Python, Homebrew 또는 MySQL 라이브러리 중 일부는 Intel용이고 나머지는 Apple Silicon용이다.

### 진단

```bash
uname -m
python -c "import platform; print(platform.machine())"
which brew
brew --prefix
```

권장 결과:

```text
arm64
arm64
/opt/homebrew/bin/brew
/opt/homebrew
```

Python 바이너리 확인:

```bash
file "$(which python)"
```

MySQL 라이브러리 확인:

```bash
file "$(brew --prefix mysql-client)/lib/libmysqlclient.dylib"
```

### 해결

Apple Silicon 네이티브 터미널에서 작업한다.

```bash
arch
```

출력이 `arm64`여야 한다.

기존 가상환경은 삭제하고 네이티브 Python으로 다시 만든다.

```bash
deactivate 2>/dev/null || true
rm -rf .venv

/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
python -m pip install mysqlclient
```

`pyenv`를 사용한다면 해당 Python도 `arm64`로 설치되었는지 확인해야 한다.

---

## 오류 8. `Library not loaded: libmysqlclient...dylib`

오류 예시:

```text
ImportError: dlopen(..._mysql...so):
Library not loaded: libmysqlclient.XX.dylib
```

### 원인

- `mysqlclient` 설치 후 Homebrew의 MySQL 버전이 변경되었다.
- 기존 MySQL 클라이언트 라이브러리가 삭제되었다.
- 가상환경에 빌드된 확장 모듈이 이전 라이브러리 경로를 참조한다.

### 해결

Homebrew 패키지를 확인한다.

```bash
brew list --versions mysql mysql-client
brew doctor
```

라이브러리를 다시 설치한다.

```bash
brew reinstall mysql-client
```

가상환경에서 `mysqlclient`를 다시 빌드한다.

```bash
source .venv/bin/activate

python -m pip uninstall -y mysqlclient
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
python -m pip install --no-cache-dir mysqlclient
```

Homebrew 업그레이드 후 발생했다면 재설치가 가장 안전한 해결책이다.

---

## 오류 9. `Access denied for user`

오류 예시:

```text
MySQLdb.OperationalError:
(1045, "Access denied for user 'python_app'@'localhost'")
```

### 원인

- 사용자 이름 또는 비밀번호가 틀렸다.
- `'python_app'@'localhost'` 계정이 없다.
- 해당 데이터베이스 권한이 없다.
- 접속 host와 MySQL 계정의 host 조건이 다르다.

### 확인

터미널에서 같은 계정으로 접속해본다.

```bash
mysql -h 127.0.0.1 -u python_app -p
```

관리자 계정으로 사용자 정보를 확인한다.

```sql
SELECT user, host, plugin
FROM mysql.user
WHERE user = 'python_app';
```

권한 확인:

```sql
SHOW GRANTS FOR 'python_app'@'localhost';
```

### 해결

```sql
CREATE USER IF NOT EXISTS 'python_app'@'localhost'
IDENTIFIED BY '안전한_비밀번호';

GRANT ALL PRIVILEGES
ON ai.*
TO 'python_app'@'localhost';
```

원격 접속 계정은 실제 접속 위치에 맞는 host를 사용해야 한다.

---

## 오류 10. `(2002) Can't connect ... through socket`

오류 예시:

```text
Can't connect to local MySQL server through socket
```

### 원인

- MySQL 서버가 실행 중이 아니다.
- Python 클라이언트와 서버가 서로 다른 Unix socket 경로를 사용한다.
- `localhost`가 TCP가 아닌 Unix socket 연결로 처리되었다.

MySQL 문서에 따르면 Unix 계열에서 `localhost`는 일반적으로 Unix socket 연결을 사용한다.

### 해결 방법 1: 서버 실행

```bash
brew services start mysql
brew services list
```

### 해결 방법 2: TCP 연결 사용

`localhost` 대신 `127.0.0.1`을 사용한다.

```python
db = MySQLdb.connect(
    host="127.0.0.1",
    port=3306,
    user="python_app",
    password="비밀번호",
    db="ai",
)
```

### 해결 방법 3: socket 경로 확인

```bash
mysql_config --socket
```

또는 MySQL 안에서 확인한다.

```sql
SHOW VARIABLES LIKE 'socket';
```

필요하다면 Python 연결에 socket 경로를 지정한다.

```python
db = MySQLdb.connect(
    unix_socket="/실제/mysql.sock",
    user="python_app",
    password="비밀번호",
    db="ai",
)
```

---

## 오류 11. `(2003) Can't connect to MySQL server`

오류 예시:

```text
Can't connect to MySQL server on '127.0.0.1'
```

### 원인

- MySQL 서버가 실행되지 않았다.
- 포트 번호가 다르다.
- 원격 서버의 방화벽이 연결을 차단한다.
- MySQL 서버가 해당 네트워크 인터페이스에서 대기하지 않는다.

### 확인

```bash
brew services list
mysqladmin -h 127.0.0.1 -u root -p ping
```

포트 확인:

```bash
lsof -nP -iTCP:3306 -sTCP:LISTEN
```

연결 코드의 host와 port도 확인한다.

```python
host="127.0.0.1"
port=3306
```

---

## 오류 12. `(1049) Unknown database`

오류 예시:

```text
MySQLdb.OperationalError:
(1049, "Unknown database 'ai'")
```

### 원인

연결 코드에 지정한 데이터베이스가 존재하지 않는다.

### 해결

MySQL에 접속해서 데이터베이스 목록을 확인한다.

```sql
SHOW DATABASES;
```

데이터베이스를 생성한다.

```sql
CREATE DATABASE ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## 오류 13. 한글이 깨지거나 인코딩 오류 발생

오류 예시:

```text
Incorrect string value
UnicodeEncodeError
한글이 물음표로 저장됨
```

### 원인

- Connection 문자 집합이 올바르지 않다.
- 데이터베이스 또는 테이블 문자 집합이 `utf8mb4`가 아니다.

### Python 설정

```python
db = MySQLdb.connect(
    host="127.0.0.1",
    user="python_app",
    password="비밀번호",
    db="ai",
    charset="utf8mb4",
)
```

### 데이터베이스 설정 확인

```sql
SHOW CREATE DATABASE ai;
SHOW CREATE TABLE voca;
```

문자 집합 변경 예시:

```sql
ALTER DATABASE ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

ALTER TABLE voca
CONVERT TO CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## 오류 14. Jupyter에서만 import 실패

오류:

```text
ModuleNotFoundError: No module named 'MySQLdb'
```

터미널에서는 import가 되지만 Notebook에서만 실패한다.

### 원인

Jupyter 커널이 `mysqlclient`를 설치한 가상환경과 다른 Python을 사용한다.

### 확인

터미널:

```bash
which python
```

Notebook:

```python
import sys

print(sys.executable)
```

두 경로가 다르면 커널이 다른 것이다.

### 해결

```bash
source .venv/bin/activate
python -m pip install ipykernel

python -m ipykernel install \
    --user \
    --name mysql-python \
    --display-name "Python (mysqlclient)"
```

Notebook에서 `Python (mysqlclient)` 커널을 선택한다.

---

## 오류 15. `pip install`은 성공했는데 import 시 실패

### 원인

- 설치 중 사용한 Python과 실행 중인 Python이 다르다.
- Homebrew 업그레이드로 동적 라이브러리 연결이 깨졌다.
- 이전 빌드 캐시가 남아 있다.

### 해결 순서

```bash
which python
python -m pip --version
python -m pip show mysqlclient
```

재설치:

```bash
python -m pip uninstall -y mysqlclient
python -m pip cache purge

export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
python -m pip install --no-cache-dir mysqlclient
```

---

## 오류 16. Python 버전에 맞는 wheel이 없음

오류 예시:

```text
Failed building wheel for mysqlclient
```

### 의미

현재 Python 버전에 사용할 수 있는 사전 빌드 wheel이 없으면 pip가 소스 빌드를 시도한다.  
소스 빌드에는 컴파일러와 MySQL 개발 라이브러리가 필요하다.

### 해결

```bash
xcode-select --install
brew install mysql-client pkg-config

export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"

python -m pip install --upgrade pip setuptools wheel
python -m pip install mysqlclient
```

너무 최신인 Python에서 호환 문제가 발생한다면 프로젝트가 지원하는 안정적인 Python 버전으로 가상환경을 만드는 것도 방법이다.

---

## 15. 권장 설치 명령 요약

MySQL 서버도 이 Mac에서 실행하는 경우:

```bash
brew install mysql pkg-config
brew services start mysql

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install mysqlclient

python -c "import MySQLdb; print('설치 성공')"
```

MySQL Client만 필요한 경우:

```bash
brew install mysql-client pkg-config

export PATH="$(brew --prefix mysql-client)/bin:$PATH"
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install mysqlclient

python -c "import MySQLdb; print('설치 성공')"
```

---

## 16. 최종 체크리스트

설치가 되지 않을 때는 다음 순서로 확인한다.

```text
1. uname -m이 arm64인가?
2. Python도 arm64인가?
3. Homebrew 경로가 /opt/homebrew인가?
4. Command Line Tools가 설치되어 있는가?
5. mysql 또는 mysql-client가 설치되어 있는가?
6. pkg-config가 설치되어 있는가?
7. PKG_CONFIG_PATH가 올바른가?
8. 가상환경이 활성화되어 있는가?
9. python -m pip로 설치했는가?
10. Jupyter가 같은 Python 커널을 사용하는가?
11. MySQL 서버가 실행 중인가?
12. 사용자, 비밀번호, host, 권한이 올바른가?
```

Apple Silicon에서 `mysqlclient` 설치 문제는 대부분 다음 세 가지 중 하나이다.

```text
Python과 라이브러리의 아키텍처 불일치
pkg-config가 MySQL 라이브러리를 찾지 못함
설치한 Python과 실행하는 Python 환경이 다름
```

환경을 하나씩 확인하면 무작정 재설치하는 것보다 빠르게 원인을 찾을 수 있다.

---

## 참고 자료

- [mysqlclient 공식 GitHub](https://github.com/PyMySQL/mysqlclient)
- [Homebrew mysql-client Formula](https://formulae.brew.sh/formula/mysql-client)
- [MySQL 연결 전송 방식](https://dev.mysql.com/doc/refman/8.4/en/transport-protocols.html)
- [MySQL 연결 문제 해결](https://dev.mysql.com/doc/refman/en/problems-connecting.html)
- [MySQL 암호화 연결](https://dev.mysql.com/doc/refman/en/encrypted-connections.html)
