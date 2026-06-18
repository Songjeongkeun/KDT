# Git과 GitHub 기초 정리

Git과 GitHub는 개발 과정에서 소스 코드의 변경 이력을 관리하고 다른 개발자와 협업하기 위해 사용하는 대표적인 도구다.

두 용어를 함께 사용하는 경우가 많지만 역할은 서로 다르다.

| 구분 | Git | GitHub |
| --- | --- | --- |
| 종류 | 분산 버전 관리 시스템 | Git 저장소 호스팅 서비스 |
| 주요 역할 | 파일의 변경 이력 관리 | 원격 저장, 공유, 협업 |
| 설치 여부 | 컴퓨터에 설치해야 한다 | 웹사이트 가입 후 사용한다 |
| 인터넷 연결 | 대부분의 작업을 오프라인으로 수행할 수 있다 | 원격 저장소 사용 시 인터넷이 필요하다 |

---

## 1. Git

Git은 소스 코드의 변경 이력을 체계적으로 관리하는 **분산 버전 관리 시스템(Distributed Version Control System)**이다.

Git을 사용하면 다음과 같은 작업을 수행할 수 있다.

- 파일의 변경 내용을 기록한다.
- 과거의 특정 상태로 되돌아간다.
- 여러 작업을 브랜치로 분리한다.
- 여러 개발자의 작업을 하나로 병합한다.
- 로컬 저장소와 원격 저장소를 연결한다.

Git은 대부분의 작업을 로컬 컴퓨터에서 수행한다. 따라서 인터넷에 연결되어 있지 않아도 커밋, 로그 확인, 브랜치 생성 등의 작업을 진행할 수 있다.

### 1.1 버전 관리란?

버전 관리(Version Control)는 소프트웨어나 문서의 변경 이력을 기록하고 관리하는 방법이다.

버전 관리를 사용하면 다음 정보를 확인할 수 있다.

- 언제 변경했는가?
- 누가 변경했는가?
- 어떤 내용을 변경했는가?
- 변경한 이유는 무엇인가?

문제가 발생했을 때 이전 버전으로 되돌리거나 두 버전의 차이를 비교할 수도 있다. 여러 사람이 동시에 작업하는 프로젝트에서는 각자의 변경 내용을 병합하고 충돌을 해결하는 데 활용한다.

대표적인 버전 관리 시스템에는 다음과 같은 도구가 있다.

- Git
- SVN(Subversion)
- Mercurial

현재는 Git이 가장 널리 사용된다.

### 1.2 Git의 장점

#### 분산형 버전 관리

Git은 각 개발자의 컴퓨터에 전체 변경 이력을 포함한 로컬 저장소를 만든다.

- 인터넷 없이도 커밋과 로그 확인이 가능하다.
- 원격 저장소에 문제가 생겨도 로컬 기록을 사용할 수 있다.
- 대부분의 명령을 로컬에서 처리하므로 속도가 빠르다.

#### 강력한 브랜치 기능

브랜치(Branch)는 기존 코드에 영향을 주지 않고 독립적인 작업을 진행할 수 있도록 분리한 작업 공간이다.

- 새로운 기능을 별도로 개발할 수 있다.
- 버그 수정 작업을 안전하게 분리할 수 있다.
- 실험적인 작업을 메인 코드에 영향을 주지 않고 테스트할 수 있다.
- 완료된 작업은 병합(Merge)할 수 있다.

#### 효율적인 협업

GitHub, GitLab 등의 서비스와 연결하면 여러 개발자가 하나의 프로젝트에서 협업할 수 있다.

- 변경 이력을 개발자별로 추적할 수 있다.
- Pull Request를 통해 코드를 검토할 수 있다.
- 충돌이 발생한 부분을 확인하고 해결할 수 있다.
- Issue를 사용해 작업과 오류를 관리할 수 있다.

#### 변경 이력 추적과 복구

Git은 누가 언제 어떤 내용을 변경했는지 기록한다.

문제가 발생하면 과거 커밋을 확인하거나 `revert`, `restore` 등의 명령으로 변경 내용을 되돌릴 수 있다.

#### 오픈소스와 다양한 도구 지원

Git은 무료로 사용할 수 있는 오픈소스 도구다.

다음과 같은 프로그램과 함께 사용할 수 있다.

- Git Bash
- Visual Studio Code
- Sourcetree
- GitHub Desktop

---

## 2. Git 설치

Git은 [Git 공식 홈페이지](https://git-scm.com/)에서 내려받을 수 있다.

### Windows 설치

1. Git 공식 홈페이지에 접속한다.
2. `Downloads`를 선택한다.
3. Windows용 설치 파일을 내려받는다.
4. 일반적인 경우 기본 설정을 유지한 상태로 설치한다.

### macOS 설치

Homebrew가 설치되어 있다면 다음 명령으로 Git을 설치할 수 있다.

```bash
brew install git
```

macOS에서는 다음 명령을 실행했을 때 개발자 도구 설치 안내가 나타날 수도 있다.

```bash
git --version
```

### 설치 확인

터미널 또는 명령 프롬프트에서 다음 명령을 실행한다.

```bash
git --version
```

설치된 Git의 버전이 출력되면 정상적으로 설치된 것이다.

---

## 3. Git의 기본 구조

Git은 파일의 상태를 크게 세 영역으로 나누어 관리한다.

```text
Working Directory  →  Staging Area  →  Repository
   작업 공간            준비 영역          저장소
```

### Working Directory

현재 파일을 작성하거나 수정하는 실제 프로젝트 폴더다.

### Staging Area

다음 커밋에 포함할 변경 사항을 임시로 선택해 두는 영역이다.

### Repository

커밋으로 확정된 변경 이력이 저장되는 영역이다.

기본적인 작업 흐름은 다음과 같다.

```text
파일 작성·수정
      ↓
git add
      ↓
git commit
      ↓
git push
```

---

## 4. Git 기본 명령어

### 4.1 로컬 저장소 생성

현재 프로젝트 폴더를 Git 저장소로 만든다.

```bash
git init
```

명령을 실행하면 현재 폴더에 `.git`이라는 숨김 폴더가 생성된다. 이 폴더에는 Git의 변경 이력과 설정 정보가 저장된다.

> 이미 Git 저장소인 폴더나 저장소 내부의 하위 폴더에서 무분별하게 `git init`을 실행하지 않도록 주의한다.

### 4.2 현재 상태 확인

변경된 파일, 스테이징된 파일과 추적되지 않는 파일을 확인한다.

```bash
git status
```

Git 작업 중에는 `git status`를 자주 실행하는 것이 좋다.

### 4.3 파일을 Staging Area에 추가

특정 파일만 추가한다.

```bash
git add index.html
```

현재 디렉터리의 모든 변경 사항을 추가한다.

```bash
git add .
```

`git add .`에는 파일의 생성, 수정, 삭제 내용이 함께 포함될 수 있으므로 커밋 전에 반드시 상태를 확인한다.

```bash
git status
```

### 4.4 커밋 생성

Staging Area에 있는 변경 내용을 하나의 버전으로 저장한다.

```bash
git commit -m "index.html 작성"
```

여러 파일을 추가한 뒤 하나의 커밋으로 저장할 수도 있다.

```bash
git add .
git commit -m "프로젝트 기본 구조 작성"
```

좋은 커밋 메시지는 무엇을 변경했는지 짧고 명확하게 설명한다.

```bash
git commit -m "README에 실행 방법 추가"
git commit -m "로그인 오류 수정"
git commit -m "맛집 카드 반응형 스타일 적용"
```

### 4.5 사용자 정보 설정

처음 커밋할 때 사용자 정보가 설정되어 있지 않으면 오류가 발생할 수 있다.

전역 사용자 정보를 설정한다.

```bash
git config --global user.name "사용자 이름"
git config --global user.email "example@email.com"
```

설정 내용을 확인한다.

```bash
git config --global --list
```

`--global` 옵션을 사용하면 컴퓨터의 모든 Git 저장소에 같은 사용자 정보를 적용한다.

현재 저장소에만 다른 정보를 사용하려면 `--global`을 제외한다.

```bash
git config user.name "프로젝트 사용자 이름"
git config user.email "project@example.com"
```

### 4.6 커밋 로그 확인

커밋 이력을 확인한다.

```bash
git log
```

커밋 이력을 한 줄씩 간단하게 확인한다.

```bash
git log --oneline
```

브랜치 구조까지 함께 확인한다.

```bash
git log --oneline --graph --all
```

### 4.7 변경 내용 확인

아직 스테이징하지 않은 변경 내용을 확인한다.

```bash
git diff
```

`git add`로 스테이징한 변경 내용을 확인한다.

```bash
git diff --staged
```

---

## 5. README.md

`README.md`는 프로젝트를 소개하는 설명서다. GitHub 저장소에 접속했을 때 가장 먼저 표시되는 문서이므로 프로젝트를 이해하는 데 필요한 핵심 정보를 작성한다.

README는 **Read Me**, 즉 “먼저 읽어 보세요”라는 의미다. `.md`는 Markdown 문법을 사용하는 파일 확장자다.

일반적으로 README에는 다음 내용을 작성한다.

- 프로젝트 이름과 소개
- 프로젝트를 만든 목적
- 주요 기능
- 사용 기술
- 설치 방법
- 실행 방법
- 폴더 구조
- 예제 코드 또는 실행 화면
- 참고 사항

간단한 README 예시는 다음과 같다.

````markdown
# 프로젝트 이름

프로젝트에 대한 간단한 설명

## 주요 기능

- 기능 1
- 기능 2

## 실행 방법

```bash
python3 main.py
```
````

---

## 6. GitHub

GitHub는 Git 저장소를 온라인에 저장하고 공유할 수 있는 코드 호스팅 및 협업 플랫폼이다.

GitHub에서는 다음 기능을 사용할 수 있다.

- 원격 저장소 관리
- 프로젝트 공유
- Pull Request
- 코드 리뷰
- Issue 관리
- 오픈소스 프로젝트 참여
- GitHub Actions를 이용한 자동화
- 포트폴리오 공개

Git이 변경 이력을 관리하는 도구라면, GitHub는 Git 저장소를 인터넷에서 공유하고 협업할 수 있도록 제공하는 서비스다.

---

## 7. GitHub 원격 저장소 연결

### 7.1 GitHub 저장소 생성

1. GitHub에 로그인한다.
2. `New repository` 또는 `Create repository`를 선택한다.
3. 저장소 이름을 입력한다.
4. 공개 범위를 `Public` 또는 `Private`로 설정한다.
5. 저장소를 생성한다.

로컬 프로젝트에 이미 README가 있다면 GitHub에서 README를 추가하지 않고 빈 저장소로 생성하는 편이 충돌을 줄이기 쉽다.

### 7.2 원격 저장소 등록

로컬 저장소에 GitHub 원격 저장소 주소를 등록한다.

```bash
git remote add origin https://github.com/사용자이름/저장소이름.git
```

예시는 다음과 같다.

```bash
git remote add origin https://github.com/Songjeongkeun/mysite.git
```

`origin`은 원격 저장소에 붙이는 기본 별칭이다. 반드시 `origin`을 사용해야 하는 것은 아니지만 일반적으로 사용되는 이름이다.

### 7.3 원격 저장소 확인

```bash
git remote -v
```

등록된 원격 저장소의 가져오기(Fetch) 주소와 보내기(Push) 주소를 확인할 수 있다.

### 7.4 원격 저장소 주소 변경

주소가 잘못되었거나 저장소 주소가 변경되었다면 다음 명령을 사용한다.

```bash
git remote set-url origin 새로운_저장소_URL
```

### 7.5 원격 저장소 연결 삭제

```bash
git remote remove origin
```

이 명령은 로컬 파일이나 GitHub 저장소를 삭제하지 않는다. 로컬 저장소에 등록된 원격 저장소 연결 정보만 삭제한다.

---

## 8. GitHub에 프로젝트 올리기

### 8.1 기본 브랜치 이름 확인

현재 브랜치 이름을 확인한다.

```bash
git branch
```

기본 브랜치 이름을 `main`으로 변경하려면 다음 명령을 사용한다.

```bash
git branch -M main
```

### 8.2 처음 Push하기

로컬 커밋을 GitHub 원격 저장소로 전송한다.

```bash
git push -u origin main
```

`-u`는 현재 로컬 브랜치와 원격 브랜치의 추적 관계를 설정하는 옵션이다.

한 번 추적 관계를 설정하면 이후에는 다음과 같이 간단하게 사용할 수 있다.

```bash
git push
git pull
```

> 과거에는 기본 브랜치 이름으로 `master`를 많이 사용했지만 최근 GitHub 저장소는 일반적으로 `main`을 사용한다. 실제 브랜치 이름은 `git branch`로 확인한다.

### 8.3 전체 업로드 과정

새 프로젝트를 GitHub에 처음 올리는 기본 과정은 다음과 같다.

```bash
git init
git add .
git commit -m "프로젝트 첫 커밋"
git branch -M main
git remote add origin https://github.com/사용자이름/저장소이름.git
git push -u origin main
```

이미 Git 저장소가 생성되어 있다면 `git init`을 다시 실행할 필요가 없다.

---

## 9. 원격 저장소 내용 가져오기

### 9.1 저장소 복제

GitHub에 있는 저장소를 처음 내려받을 때 사용한다.

```bash
git clone 저장소_URL
```

예시는 다음과 같다.

```bash
git clone https://github.com/Songjeongkeun/mysite.git
```

### 9.2 원격 변경 내용 가져오기

원격 저장소의 변경 내용을 내려받고 현재 브랜치에 병합한다.

```bash
git pull
```

원격 저장소의 변경 이력만 내려받고 자동으로 병합하지 않을 때는 다음 명령을 사용한다.

```bash
git fetch
```

---

## 10. 자주 발생하는 오류

### 사용자 정보가 설정되지 않은 경우

```text
Author identity unknown
```

사용자 이름과 이메일을 설정한다.

```bash
git config --global user.name "사용자 이름"
git config --global user.email "example@email.com"
```

### `origin`이 이미 존재하는 경우

```text
remote origin already exists
```

현재 등록된 주소를 확인한다.

```bash
git remote -v
```

주소를 변경한다.

```bash
git remote set-url origin 새로운_저장소_URL
```

또는 기존 연결을 삭제한 뒤 다시 등록한다.

```bash
git remote remove origin
git remote add origin 저장소_URL
```

### Push할 브랜치를 찾지 못하는 경우

```text
src refspec main does not match any
```

커밋이 아직 없거나 현재 브랜치 이름이 `main`이 아닐 때 발생할 수 있다.

```bash
git status
git branch
git add .
git commit -m "프로젝트 첫 커밋"
git branch -M main
git push -u origin main
```

### 원격 저장소에 먼저 생성된 커밋이 있는 경우

GitHub에서 README 등을 먼저 생성한 경우 로컬 저장소와 원격 저장소의 이력이 달라 Push가 거절될 수 있다.

먼저 원격 변경 내용을 가져온다.

```bash
git pull origin main
```

충돌이 발생하면 파일을 수정하고 다시 커밋한 뒤 Push한다.

---

## 11. Git 작업 흐름 정리

### 작업 시작 전

```bash
git pull
git status
```

### 파일 작성 또는 수정 후

```bash
git status
git diff
git add .
git diff --staged
git commit -m "변경 내용을 설명하는 메시지"
```

### GitHub에 업로드

```bash
git push
```

전체 흐름을 정리하면 다음과 같다.

```text
원격 변경 가져오기
       git pull
           ↓
파일 작성 또는 수정
           ↓
변경 상태 확인
       git status
           ↓
커밋할 파일 선택
        git add
           ↓
변경 이력 저장
       git commit
           ↓
GitHub에 업로드
        git push
```

---

## 12. 주요 명령어 요약

| 명령어 | 설명 |
| --- | --- |
| `git init` | 현재 폴더에 Git 저장소를 생성한다 |
| `git status` | 파일의 현재 변경 상태를 확인한다 |
| `git add 파일명` | 특정 파일을 Staging Area에 추가한다 |
| `git add .` | 현재 디렉터리의 모든 변경 사항을 추가한다 |
| `git commit -m "메시지"` | 스테이징된 변경 내용을 커밋한다 |
| `git log --oneline` | 커밋 이력을 간단하게 확인한다 |
| `git diff` | 스테이징 전 변경 내용을 확인한다 |
| `git diff --staged` | 스테이징된 변경 내용을 확인한다 |
| `git branch` | 브랜치 목록과 현재 브랜치를 확인한다 |
| `git remote -v` | 등록된 원격 저장소를 확인한다 |
| `git push` | 로컬 커밋을 원격 저장소로 전송한다 |
| `git pull` | 원격 변경 내용을 가져와 병합한다 |
| `git clone URL` | 원격 저장소를 복제한다 |

## 마무리

Git은 단순히 파일을 GitHub에 올리는 도구가 아니다. 파일의 변경 과정을 하나의 버전으로 기록하고, 필요할 때 과거 상태를 확인하거나 여러 개발자의 작업을 안전하게 병합하기 위한 도구다.

처음에는 다음 네 명령어의 흐름을 정확하게 이해하는 것이 중요하다.

```bash
git status
git add .
git commit -m "커밋 메시지"
git push
```

명령어를 외우는 것보다 **Working Directory → Staging Area → Repository → Remote Repository**로 이어지는 흐름을 이해하면 Git을 더 안전하게 사용할 수 있다.
