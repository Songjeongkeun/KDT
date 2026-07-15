# KDT

KDT 학습 과정에서 작성한 강의 정리, 실습 코드, 과제, 스터디 문제를 모아둔 저장소입니다.

## 폴더 구성

- `1_PYTHON`: Python 기초 문법 및 실습
- `2_DataAnalysis`: 데이터 분석 학습 자료와 실습
- `3_Database`: Database, MySQL 관련 정리와 예제
- `4_HTML_CSS`: HTML, CSS 학습 자료
- `5_Git`: Git 학습 및 실습
- `6_JavaScript`: JavaScript 기초 문법, DOM, 이벤트, TODO 앱 실습
- `7_NODEJS`: Node.js, Express, MongoDB, JWT, Socket.IO 실습
- `8_React`: React 기초, 배열 렌더링, Hooks, Reducer 실습
- `X_Project`: 팀 프로젝트 관련 클라이언트 및 서버 작업
- `강의 정리`: 수업 내용 정리
- `스터디 문제`: 스터디용 문제와 풀이
- `과제`: 과제 제출용 폴더

## 실행 방법

HTML, CSS, JavaScript 파일은 VS Code Live Server 등을 사용해 브라우저에서 확인할 수 있습니다.

JavaScript 학습 파일은 `6_JavaScript` 폴더를 기준으로 실행합니다.

Node.js 또는 React 프로젝트는 실행할 프로젝트 폴더에서 의존성을 설치한 뒤 시작합니다.

```bash
npm install
npm run dev
```

프로젝트에 따라 실행 스크립트가 다를 수 있으므로 각 폴더의 `package.json`을 확인합니다.

Python 예제는 가상환경을 만든 뒤 필요한 패키지를 설치해 실행합니다. 가상환경 폴더는 저장소에 포함하지 않습니다.

## 저장소 관리

- `node_modules`, Python 가상환경, 캐시, 빌드 결과물은 Git에 올리지 않습니다.
- `.env`와 인증서, 개인 키 등 민감한 설정 파일은 커밋하지 않습니다.
- 패키지 버전 재현을 위해 `package.json`과 lock 파일은 함께 관리합니다.
