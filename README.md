# KDT 학습 기록

KDT 과정에서 작성한 강의 노트, 실습 코드, 스터디 문제와 시험 자료를 모아둔 저장소입니다. 하나의 애플리케이션이 아니라 주제별로 독립적인 예제를 담고 있습니다.

## 학습 자료

| 폴더 | 내용 |
| --- | --- |
| [1_PYTHON](./1_PYTHON/) | Python 기초 문법, 객체지향, 예외 처리, FastAPI 및 API 실습 |
| [2_DataAnalysis](./2_DataAnalysis/) | NumPy, pandas, 웹 크롤링, Selenium, 시각화와 데이터 분석 |
| [3_Database](./3_Database/) | MySQL DDL·DML, 정규화, 서브쿼리, 뷰와 Python 연동 |
| [4_HTML_CSS](./4_HTML_CSS/) | HTML 요소, CSS 레이아웃, 반응형 디자인과 애니메이션 |
| [5_Git](./5_Git/) | Git과 GitHub 기초 |
| [6_JavaScript](./6_JavaScript/) | JavaScript 문법, DOM·이벤트, 브라우저 저장소와 비동기 처리 |
| [7_NODEJS](./7_NODEJS/) | Node.js, Express, MongoDB, JWT와 Socket.IO 실습 |
| [8_React](./8_React/) | React 컴포넌트, Hooks, Context, Router, TODO 및 CRUD 예제 |
| [9_NextJs.Js](./9_NextJs.Js/) | Next.js 앱 실습 |
| [10_MLDL](./10_MLDL/) | 머신러닝, scikit-learn, PyTorch, 퍼셉트론과 CNN 노트북 |
| [11_CV](./11_CV/) | 컴퓨터 비전, 객체 탐지와 세그멘테이션 노트북 |
| [12_NLP](./12_NLP/) | 자연어 처리, RNN, LSTM·GRU, 트랜스포머와 생성 모델 노트북 |

## 기타 자료

- [강의 정리](./강의%20정리/): 수업별 학습 내용과 개념 정리
- [스터디 문제](./스터디%20문제/): 연습 문제, 풀이 및 별도 프로젝트
- [시험](./시험/): Python, 머신러닝, 딥러닝 관련 자료
- [과제](./과제/): 과제용 폴더

## 실행 방법

실행 환경과 명령은 예제마다 다릅니다. 먼저 원하는 폴더의 파일과 `package.json` 또는 `requirements.txt`를 확인하세요.

- `.ipynb` 파일: Jupyter Notebook 또는 VS Code의 노트북 기능으로 엽니다. 필요한 패키지와 데이터 파일은 해당 예제에 맞춰 준비합니다.
- HTML/CSS/JavaScript 예제: 해당 `.html` 파일을 브라우저에서 열거나 VS Code Live Server로 실행합니다.
- Python 예제: 해당 폴더에 `requirements.txt`가 있으면 가상환경에서 `python -m pip install -r requirements.txt`로 설치할 수 있습니다.
- Node.js/React/Next.js 예제: 실행할 프로젝트의 `package.json`이 있는 폴더에서 `npm install` 후 그 파일에 정의된 스크립트로 실행합니다.

예를 들어 [Next.js 실습 앱](./9_NextJs.Js/cursor-app/)은 다음과 같이 시작합니다.

```bash
cd 9_NextJs.Js/cursor-app
npm install
npm run dev
```

서버, 데이터베이스 또는 외부 API를 사용하는 예제는 별도 설정이 필요할 수 있습니다. 설정값은 코드와 각 예제의 안내 파일을 확인하세요.

## 저장소 이용 시 참고

이 저장소에는 학습용 코드와 자료가 함께 있어 폴더마다 의존성과 실행 방식이 다릅니다. `node_modules`, Python 가상환경, 빌드 결과물과 API 키·비밀번호가 담긴 설정 파일은 커밋하지 마세요.
