# [92일차] PDF 기반 RAG 챗봇과 SQLite, SQLDatabase

PDF에서 찾은 내용을 근거로 답하는 챗봇을 만들고, SQLite 데이터를 Python과 LangChain에서 조회하는 방법을 정리한다.

> 정리 범위는 `2_Retriver.ipynb`의 **SPRi PDF 기반 정책 산업 브리핑 어시스턴트** 셀부터 마지막까지, 그리고 `3_SQL을 작성하는 RAG.ipynb` 전체다. 앞부분의 검색기 구성은 이미 준비되어 있다고 가정한다. API 응답은 노트북에 저장된 실행 기록이며, 원본과 구분이 필요한 보완 예제는 따로 표시했다.

## 1. PDF 검색에서 질의응답으로

검색기는 질문과 관련된 문서를 반환한다. 여기에 질문과 검색 내용을 모델에 함께 전달하면 문서 기반 답변을 생성할 수 있다.

```text
질문 입력
    |
    v
Retriever로 관련 청크 검색
    |
    v
최대 4개 청크 선택
    |
    v
각 청크 앞에 PDF 페이지 번호 추가
    |
    v
질문 + 검색 내용 + 답변 규칙을 모델에 전달
    |
    v
답변과 검색된 PDF 페이지 표시
```

이번 PDF 챗봇에는 Tavily 등의 외부 웹 검색을 연결하지 않는다. 준비된 PDF 검색기를 사용하며, 모델에는 제공된 문서만 근거로 답하도록 요청한다.

단, 프롬프트에 제한을 적는 것만으로 외부 지식 사용이나 잘못된 답변을 완전히 차단할 수 있는 것은 아니다. 답변과 근거의 일치 여부는 별도로 확인해야 한다.

### 챗봇의 요구사항

| 항목 | 내용 |
|---|---|
| 검색 대상 | 준비한 SPRi PDF |
| 검색 결과 수 | 질문마다 관련 청크 최대 4개 |
| 출처 | PDF 페이지 번호 표시 |
| API 키가 없는 경우 | 모델 답변 없이도 검색 페이지 확인 |
| 근거가 부족한 경우 | 추측하지 않고 확인 불가라고 안내 |
| 비교 | 여러 질문과 검색기 변경에 따른 결과 확인 |

원본 설명의 “관련 링크”는 실제 구현에서는 웹 링크가 아니라 PDF 청크와 페이지 번호에 해당한다.

### 앞에서 준비되어 있어야 하는 값

| 이름 | 역할 |
|---|---|
| `pdf_bm25` | PDF 청크를 대상으로 하는 BM25 검색기 |
| `pdf_vector_retriever` | PDF 청크의 벡터 검색기 |
| `OPENAI_API_KEY` | 원본에서는 환경 변수의 존재 여부를 담은 bool |
| `ChatOpenAI` | 답변 모델을 만드는 클래스 |

BM25는 검색 계산 자체에 OpenAI API를 사용하지 않는다. 반면 원본의 벡터 검색기는 OpenAI 임베딩을 사용하므로, 모델 답변을 생략하는 것과 벡터 검색까지 API 없이 할 수 있다는 것은 다르다.

## 2. ChatPromptTemplate로 메시지 구성하기

`ChatPromptTemplate`은 역할이 있는 메시지들과 입력 변수를 템플릿으로 정의하는 도구다.

```python
from langchain_core.prompts import ChatPromptTemplate
```

이 예제에서는 두 종류의 메시지를 사용한다.

| 역할 | 전달할 내용 |
|---|---|
| `system` | 답변 규칙과 참고할 PDF 내용 |
| `human` | 사용자의 질문 |

```python
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "제공된 PDF 내용만 근거로 답변하세요.\nPDF 내용:\n{context}",
    ),
    ("human", "{question}"),
])
```

위 코드는 변수와 역할을 설명하기 위해 짧게 만든 예제다. `{context}`에는 검색한 문서 내용, `{question}`에는 사용자의 질문을 넣는다.

문자열을 직접 연결하는 것과 달리, 템플릿에 어떤 입력이 필요한지 드러나고 메시지의 역할도 구분할 수 있다.

## 3. 질문을 받아 답변하는 함수

다음은 원본 함수다. 줄바꿈과 들여쓰기만 읽기 쉽게 정리했다. API 키가 없는 분기의 문제는 다음 절에서 별도로 살펴본다.

```python
def answer_from_spri_pdf(question, retriever):
    docs = retriever.invoke(question)[:4]

    if not docs:
        return {
            "answer": "PDF에서 관련 내용을 확인할 수 없습니다.",
            "sources": [],
        }

    pages = sorted(set(
        doc.metadata.get(
            "page_display",
            doc.metadata.get("page", 0) + 1,
        )
        for doc in docs
    ))

    context = "\n\n".join(
        f"[PDF{doc.metadata.get('page_display', doc.metadata.get('page', 0) + 1)}쪽]\n"
        f"{doc.page_content}"
        for doc in docs
    )

    if not OPENAI_API_KEY:
        return {"answer": "API KEY ERROR!"}

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            당신은 SPRi AI 정책 산업 브리핑 어시스턴트입니다.

            반드시 제공된 PDF 내용만 근거로 답변하세요.
            외부 지식이나 추측을 사용하지 마세요.
            근거가 부족하면 '제공된 PDF에서 확인할 수 없습니다.'라고 답하세요.
            답변에는 근거가 되는 PDF 페이지 번호를 포함하세요.

            PDF 내용:
            {context}
            """,
        ),
        ("human", "{question}"),
    ])

    llm = ChatOpenAI(model="gpt-5.6-luna", temperature=0)
    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})

    return {"answer": response.content, "sources": pages}
```

`gpt-5.6-luna`는 원본에 직접 적힌 모델명이다. 이 함수는 앞에서 생성한 전역 `llm`을 사용하는 대신 내부에서 새 모델 객체를 만든다. 따라서 다른 셀의 `MODEL_NAME`만 바꾸어도 이 함수의 모델명까지 함께 바뀌지는 않는다.

### 함수의 역할 분담

| 코드 | 역할 |
|---|---|
| `retriever.invoke(question)` | 관련 Document 목록 검색 |
| `[:4]` | 반환된 목록에서 앞의 최대 4개 선택 |
| `if not docs` | 검색 결과가 비어 있는 경우 처리 |
| `pages` | 검색된 문서의 페이지 번호 정리 |
| `context` | 모델에 전달할 문서 본문과 페이지 표시 구성 |
| `prompt` | 답변 규칙과 사용자 질문 정의 |
| `prompt \| llm` | 템플릿과 모델을 순서대로 연결 |
| `chain.invoke(...)` | 변수 값을 채워 모델 호출 |

`[:4]`는 검색기가 결과를 반환한 뒤 목록을 자르는 코드다. 검색기 내부의 후보 검색 방식이나 `k` 설정 자체를 바꾸는 것은 아니다.

## 4. 페이지 번호와 context는 어떻게 만들어지는가?

### 페이지 번호 선택

```python
doc.metadata.get(
    "page_display",
    doc.metadata.get("page", 0) + 1,
)
```

| 메타데이터 | 처리 |
|---|---|
| `page_display`가 있음 | 해당 값 사용 |
| `page_display`가 없고 `page`가 있음 | 0부터 시작하는 페이지에 1을 더함 |
| 둘 다 없음 | 기본값으로 1이 나올 수 있으므로 출처 확인 필요 |

페이지 정보가 빠졌는데 1쪽으로 표시되면 잘못된 출처가 될 수 있다. 앞의 문서 준비 단계에서 메타데이터를 보존해야 하는 이유다.

### 중복 페이지 제거와 정렬

```python
# 계산 방식을 보여주는 보완 예제다.
page_numbers = [13, 5, 13, 20]
pages = sorted(set(page_numbers))
print(pages)
```

```text
[5, 13, 20]
```

`set()`은 중복을 없애고, `sorted()`는 페이지 번호를 정렬한다. 따라서 이 목록은 검색 순위가 아니라 페이지 순서다.

또한 **페이지 목록의 중복 제거와 문서 본문의 중복 제거는 다르다.** 같은 페이지의 청크 두 개가 검색되면 `pages`에는 한 번만 표시되지만, `context`에는 두 청크가 모두 들어간다.

### 모델에 전달할 context

```text
[PDF5쪽]
첫 번째 청크의 본문

[PDF20쪽]
두 번째 청크의 본문
```

각 청크 앞에 페이지를 붙이면 모델이 본문과 출처를 함께 참고할 수 있다. 다만 모델이 출력한 인용 번호를 코드가 검증하는 단계는 없다.

## 5. 체인 연결: prompt | llm

```python
chain = prompt | llm
response = chain.invoke({"context": context, "question": question})
```

여기서 `|`는 LangChain의 Runnable을 연결하는 문법이다.

```text
입력 딕셔너리
{"context": 검색한 내용, "question": 질문}
    |
    v
prompt: 변수 값을 메시지에 채움
    |
    v
llm: 완성된 메시지를 입력받아 응답 생성
    |
    v
response.content: 답변 본문
```

템플릿을 정의하는 것만으로 모델이 실행되지는 않는다. 실제 모델 호출은 `chain.invoke()`에서 이루어진다.

## 6. API 키가 없을 때의 반환값 보완

원본은 다음과 같이 반환한다.

```json
{"answer": "API KEY ERROR!"}
```

실제 함수에서는 위 딕셔너리를 `return`한다. 그런데 출력 함수는 항상 `result["sources"]`를 읽는다. 이 경로에서는 `sources`가 없어 `KeyError`가 발생할 수 있으며, 검색 페이지를 확인하라는 요구사항도 충족하지 못한다.

### 최소 수정 예시

아래는 **함수 내부 분기만 교체하는 보완 코드**다. 원본 노트북에는 적용하지 않았다.

```diff
 if not OPENAI_API_KEY:
-    return {"answer": "API KEY ERROR!"}
+    return {
+        "answer": "API 키가 없어 답변을 생성하지 않았습니다. 검색된 PDF 페이지를 확인하세요.",
+        "sources": pages,
+    }
```

BM25 검색은 이미 앞에서 수행했으므로 모델을 호출하지 않고도 검색된 페이지를 반환할 수 있다.

또한 검색 결과가 있다는 것만으로 질문에 답할 근거가 있다는 뜻은 아니다. BM25나 벡터 검색은 관련성이 낮아도 후보를 반환할 수 있으므로 `if not docs`는 빈 결과만 처리한다.

## 7. 대화형 챗봇 구성

```python
def spri_chatbot():
    print("SPRi PDF 정책 산업 브리핑 챗봇")
    print("종료하려면 '종료'를 입력하세요.")

    while True:
        question = input("\n질문을 입력하세요.").strip()

        if question.lower() in ["종료", "exit", "quit"]:
            print("챗봇을 종료합니다.")
            break

        if not question:
            continue

        print("\n검색 방법을 선택하세요.")
        print("1. BM25")
        print("2. Vector")
        method = input("선택(1/2): ").strip()

        if method == "2":
            if not OPENAI_API_KEY:
                print("API 키가 없어 BM25로 검색합니다.")
                retriever = pdf_bm25
            else:
                retriever = pdf_vector_retriever
        else:
            retriever = pdf_bm25

        result = answer_from_spri_pdf(question, retriever=retriever)

        print("\n[챗봇 답변]")
        print(result["answer"])
        print("\n[참고 PDF 페이지]")
        print(result["sources"])
```

```python
spri_chatbot()
```

### 입력 처리와 검색기 선택

| 코드 | 의미 |
|---|---|
| `.strip()` | 입력 앞뒤 공백 제거 |
| `.lower()` | 영문 종료 명령의 대소문자 차이 제거 |
| `break` | 반복 종료 |
| `continue` | 빈 질문이면 다음 입력으로 이동 |
| `method == "2"` | 벡터 검색 선택 |
| 그 외 입력 | 원본에서는 BM25 선택 |

`1`, `2` 이외의 입력을 오류로 처리하는 검증은 없다. 또 이전 질문과 답변을 메시지 이력으로 전달하지 않으므로, 반복해서 입력할 수는 있지만 대화 맥락을 기억하는 챗봇은 아니다.

## 8. 노트북에 저장된 답변 결과

저장된 출력에는 질문 입력문과 검색 방법의 실제 선택값이 남아 있지 않다. 아래는 **답변 내용으로 구분한 사례**이며, 질문 원문을 복원한 것은 아니다.

| 사례 | 답변의 핵심 | 반환된 `sources` |
|---|---|---|
| EU AI 법 관련 | 보고서에 설명된 투명성 의무를 요약하고 PDF 5쪽 인용 | `[5, 20]` |
| 2035년 규제 관련 | 제공된 PDF에서 확정된 내용을 확인할 수 없다고 응답 | `[2, 5, 7]` |
| Muse 관련 | 이메일 발송·여행 예약·양식 작성·계획 수립·상품 구매 등을 보고서 내용으로 안내 | `[13]` |

위 내용은 모델의 저장된 응답을 요약한 것이다. 보고서의 법률·제품 관련 주장을 이 문서에서 별도로 검증한 것은 아니다.

### 검색된 페이지와 답변의 인용은 구분해야 한다

첫 사례에서 답변은 5쪽을 인용하지만 `sources`에는 5쪽과 20쪽이 있다. `sources`는 모델이 실제 사용한 근거만 추린 목록이 아니라 **검색해 전달한 모든 청크의 페이지 목록**이기 때문이다.

두 번째 사례에서는 답변이 `PDF 4~6쪽`을 언급했지만, 반환된 검색 페이지는 `[2, 5, 7]`이다. 이 번호들은 일치하지 않는다. 원문을 확인하고 답변의 출처 표시가 적절한지 검토해야 한다.

“확인할 수 없다”는 답변을 했다고 해서 그 안의 모든 부연 설명과 페이지 인용까지 정확하다고 판단하면 안 된다.

### 자동 테스트 구현 여부

원본에는 대화형 실행 결과 세 건이 있지만, 여러 질문을 자동 반복하고 BM25·벡터 결과를 평가하는 테스트 코드는 없다.

아래는 비교를 시작할 때 사용할 수 있는 **보완 예제**다. 위의 API 키 없는 분기를 보완하고, 필요한 검색기를 준비한 상태를 전제로 한다. 모델·임베딩 API를 사용할 수 있으므로 이 문서 작성 중에는 실행하지 않았다.

```python
questions = [
    "EU AI 법의 투명성 의무는 무엇인가요?",
    "Muse는 어떤 업무를 수행하나요?",
]

retrievers = {"BM25": pdf_bm25}
if OPENAI_API_KEY:
    retrievers["Vector"] = pdf_vector_retriever

for question in questions:
    print("\n질문:", question)
    for name, retriever in retrievers.items():
        result = answer_from_spri_pdf(question, retriever)
        print(name, "검색 페이지:", result["sources"])
        print(result["answer"])
```

결과를 출력하는 것과 성능을 평가하는 것은 다르다. 비교 시에는 같은 질문을 사용하고, 사람이 확인한 정답 페이지와 답변의 사실성·근거 일치 여부를 별도로 살펴봐야 한다.

## 9. SQLite란?

SQLite는 별도의 데이터베이스 서버 프로세스를 띄우지 않고 사용할 수 있는 데이터베이스다. 이번 예제에서는 데이터를 `.db` 파일에 저장하고, Python의 `sqlite3` 모듈로 SQL을 실행한다. [Python sqlite3 문서](https://docs.python.org/3/library/sqlite3.html)

| 구성요소 | 이번 예제에서의 역할 |
|---|---|
| SQLite | 테이블과 데이터를 저장하고 SQL 실행 |
| `sqlite3` | Python에서 SQLite 연결·실행 |
| pandas | 조회 결과를 DataFrame으로 확인 |
| `SQLDatabase` | LangChain에서 DB 구조 정보를 다루기 위한 연결 |

SQLite 실습은 PDF 챗봇과 별도다. 이 DB 조회가 PDF 챗봇의 검색 도구로 연결되어 있지는 않다.

## 10. 데이터 폴더와 DB 연결

```python
import sqlite3
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
simple_path = DATA_DIR / "hello.db"

conn_simple = sqlite3.connect(simple_path)
print("연결 성공", simple_path.resolve())
```

| 코드 | 의미 |
|---|---|
| `Path("data")` | 현재 작업 폴더 기준 `data` 경로 |
| `.mkdir(exist_ok=True)` | 폴더가 있으면 오류 없이 사용 |
| `DATA_DIR / "hello.db"` | DB 파일 경로 구성 |
| `sqlite3.connect(...)` | 파일을 열고 연결 객체 반환. 파일이 없으면 새 DB 생성 |
| `.resolve()` | 절대 경로로 확인 |

원본 실행에서는 `14_AGENT/data/hello.db`에 연결되었다. 실제 절대 경로는 실행 환경에 따라 달라진다.

연결했다고 테이블까지 자동으로 만들어지는 것은 아니다. 테이블 생성은 다음 SQL에서 수행한다.

## 11. 학생 테이블 만들기

```python
conn_simple.execute("""
create table students(
    id integer primary key,
    name varchar(20) not null,
    score integer not null
)
""")
```

| 컬럼 | 선언 | 의미 |
|---|---|---|
| `id` | `integer primary key` | 학생 식별자 |
| `name` | `varchar(20) not null` | 이름. NULL 허용 안 함 |
| `score` | `integer not null` | 점수. NULL 허용 안 함 |

`execute()`는 SQL 한 문장을 실행한다. Jupyter에서 마지막 줄의 반환값을 표시하면 `<sqlite3.Cursor ...>`가 보일 수 있다. 이것은 조회된 학생 데이터가 아니라 SQL 실행에 사용하는 커서 객체다.

원본 코드는 새 DB에서 처음 실행하는 것을 전제로 한다. 같은 DB에서 생성 셀을 다시 실행하면 이미 테이블이 있다는 오류가 날 수 있다. 문서에는 테이블을 삭제하거나 초기화하는 코드를 추가하지 않았다.

## 12. 여러 행 삽입하기: executemany()

```python
students = [
    (1, "김사과", 90),
    (2, "반하나", 85),
    (3, "오렌지", 95),
]

conn_simple.executemany(
    "insert into students (id, name, score) values (?, ?, ?)",
    students,
)

conn_simple.commit()
print("학생 데이터 저장 완료")
```

```text
학생 데이터 저장 완료
```

| 표현 | 역할 |
|---|---|
| `students` | 삽입할 행을 담은 튜플 목록 |
| `executemany()` | 같은 SQL에 여러 행의 값을 바인딩해 실행 |
| `?` | 값을 전달할 자리인 placeholder |
| `commit()` | 이 예제의 삽입 변경사항 확정 |

```text
첫 행  (1, 김사과, 90) -> (?, ?, ?)에 바인딩
둘째 행(2, 반하나, 85) -> (?, ?, ?)에 바인딩
셋째 행(3, 오렌지, 95) -> (?, ?, ?)에 바인딩
```

값을 SQL 문자열에 직접 이어 붙이지 않고 placeholder로 전달한다. 이렇게 SQL 코드와 데이터를 분리하는 것이 중요하다. 단, placeholder는 테이블명 같은 SQL 식별자를 대신하는 용도가 아니다.

같은 삽입 셀을 다시 실행하면 이미 존재하는 기본키 값 때문에 오류가 날 수 있다. `commit()`은 중복 데이터를 무시하거나 덮어쓰는 명령이 아니다.

## 13. 조건 조회와 fetchall()

```python
rows = conn_simple.execute(
    "select name, score from students where score >= ? order by score desc",
    (90,),
).fetchall()

for name, score in rows:
    print(name, score)
```

```text
오렌지 95
김사과 90
```

### 조회 조건

```sql
select name, score
from students
where score >= ?
order by score desc
```

| 절 | 역할 |
|---|---|
| `select name, score` | 이름과 점수 선택 |
| `where score >= ?` | 전달한 기준값 이상인 행 선택 |
| `order by score desc` | 점수 내림차순 정렬 |

### 왜 `(90,)`처럼 쉼표가 있는가?

매개변수가 한 개여도 값 목록을 전달해야 한다. `(90,)`은 원소가 하나인 튜플이지만 `(90)`은 정수 `90`과 같다.

```python
print(type((90,)).__name__)
print(type((90)).__name__)
```

```text
tuple
int
```

`fetchall()`은 남은 조회 결과를 모두 가져온다. 이번 예제의 결과 구조는 다음과 같다.

```python
[("오렌지", 95), ("김사과", 90)]
```

반환된 각 튜플을 `for name, score in rows`에서 이름과 점수로 나누어 사용한다.

## 14. pandas로 SQL 결과 확인하기

```python
import pandas as pd


pd.read_sql_query(
    "SELECT * FROM students ORDER BY score DESC",
    conn_simple,
)
```

저장된 DataFrame 출력이다.

| DataFrame 인덱스 | id | name | score |
|---:|---:|---|---:|
| 0 | 3 | 오렌지 | 95 |
| 1 | 1 | 김사과 | 90 |
| 2 | 2 | 반하나 | 85 |

맨 왼쪽 인덱스는 pandas가 붙인 행 번호이고, DB의 기본키 `id`와는 다르다.

| 방식 | 결과 형태 |
|---|---|
| `execute(...).fetchall()` | 기본 설정에서 튜플 목록 |
| `pd.read_sql_query(...)` | DataFrame |

### 사용한 연결 종료

```python
conn_simple.close()
print("연습용 DB 연결 종료")
```

```text
연습용 DB 연결 종료
```

`close()`로 연결을 닫아도 저장한 `.db` 파일이 삭제되지는 않는다. 닫은 연결로 다시 조회하려면 새 연결이 필요하다.

## 15. Chinook 샘플 DB 불러오기

Chinook은 디지털 미디어 판매 데이터를 다루는 샘플 DB다. 고객·판매·음원처럼 관계가 있는 여러 테이블로 JOIN과 집계를 연습할 수 있다.

```python
import requests


path = DATA_DIR / "Chinook.db"

if not path.exists():
    url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    path.write_bytes(response.content)

print("DB 파일:", path.resolve())
conn = sqlite3.connect(path)
print("연결 성공")
```

| 코드 | 역할 |
|---|---|
| `if not path.exists()` | DB가 있으면 다운로드 생략 |
| `requests.get(..., timeout=30)` | 다운로드 요청 |
| `raise_for_status()` | HTTP 오류 상태 확인 |
| `response.content` | 응답의 바이트 데이터 |
| `path.write_bytes(...)` | DB 파일로 저장 |
| `sqlite3.connect(path)` | 저장한 DB 연결 |

여기서 `.db` 파일을 다운로드하는 것은 웹 검색 Agent를 실행하는 것과 다르다. 데이터 파일을 한 번 가져와 로컬 SQLite에 연결하는 과정이다.

## 16. 테이블 목록 확인하기

```python
tables = conn.execute(
    "select name from sqlite_master where type='table' order by name"
).fetchall()

print([name for (name,) in tables])
```

```text
['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
```

`sqlite_master`는 SQLite의 테이블 등 스키마 정보를 조회할 때 사용하는 내부 스키마 테이블 이름이다.

```text
fetchall() 결과: [('Album',), ('Artist',), ...]
리스트 변환:     ['Album', 'Artist', ...]
```

`(name,)`은 한 항목 튜플에서 이름만 꺼내는 표현이다.

### 주요 테이블 관계

| 테이블 | 담는 정보 |
|---|---|
| `Customer` | 고객 |
| `Invoice` | 고객의 판매 전표와 총액 |
| `InvoiceLine` | 전표의 개별 판매 항목 |
| `Track` | 음원 |
| `Album` | 앨범 |
| `Artist` | 아티스트 |

```text
Customer
    | 연결 키: CustomerId
Invoice
    | 연결 키: InvoiceId
InvoiceLine
    | 연결 키: TrackId
Track
```

한 고객에게 여러 전표가 연결될 수 있고, 한 전표에는 여러 판매 항목이 연결될 수 있다.

## 17. 고객 데이터와 JOIN 조회

### 고객 다섯 명 조회

```python
pd.read_sql_query("select * from customer limit 5", conn)
```

원본은 전체 컬럼을 출력한다. 아래 표는 그중 고객 ID·이름·국가만 발췌했다.

| CustomerId | FirstName | LastName | Country |
|---:|---|---|---|
| 1 | Luís | Gonçalves | Brazil |
| 2 | Leonie | Köhler | Germany |
| 3 | François | Tremblay | Canada |
| 4 | Bjørn | Hansen | Norway |
| 5 | František | Wichterlová | Czech Republic |

### 고객 이름과 판매 전표 총액 조회

```python
pd.read_sql_query("""
    select c.firstname, c.lastname, i.total
    from customer as c
    join invoice as i on c.customerid = i.customerid
    limit 10
""", conn)
```

저장된 조회 결과다.

| FirstName | LastName | Total |
|---|---|---:|
| Leonie | Köhler | 1.98 |
| Bjørn | Hansen | 3.96 |
| Daan | Peeters | 5.94 |
| Mark | Philips | 8.91 |
| John | Gordon | 13.86 |
| Fynn | Zimmermann | 0.99 |
| Niklas | Schröder | 1.98 |
| Dominique | Lefebvre | 1.98 |
| Wyatt | Girard | 3.96 |
| Hugh | O'Reilly | 5.94 |

| 표현 | 의미 |
|---|---|
| `customer as c` | 고객 테이블에 짧은 이름 `c` 부여 |
| `invoice as i` | 전표 테이블에 짧은 이름 `i` 부여 |
| `on c.customerid = i.customerid` | 같은 고객 ID로 두 테이블 연결 |
| `i.total` | 개별 전표의 총액 |
| `limit 10` | 최대 10개 행 반환 |

고객별 합계를 계산한 쿼리는 아니다. 고객이 여러 전표를 가지고 있으면 이름이 여러 행에 나올 수 있다. 또 `ORDER BY`가 없어 이 결과의 출력 순서를 일반적인 보장으로 생각하면 안 된다.

## 18. 국가별 판매 총액 상위 5개

```python
pd.read_sql_query("""
    select billingcountry, round(sum(total), 2) as revenue
    from invoice
    group by billingcountry
    order by revenue desc
    limit 5
""", conn)
```

| BillingCountry | revenue |
|---|---:|
| USA | 523.06 |
| Canada | 303.96 |
| France | 195.10 |
| Brazil | 190.10 |
| Germany | 156.48 |

### SQL을 단계별로 읽기

| 단계 | 코드 | 의미 |
|---:|---|---|
| 1 | `from invoice` | 판매 전표 사용 |
| 2 | `group by billingcountry` | 청구 국가별로 묶기 |
| 3 | `sum(total)` | 국가별 전표 총액 합산 |
| 4 | `round(..., 2)` | 소수 둘째 자리로 반올림 |
| 5 | `as revenue` | 계산 결과에 이름 부여 |
| 6 | `order by revenue desc` | 총액 내림차순 정렬 |
| 7 | `limit 5` | 상위 다섯 국가만 반환 |

기준은 고객 테이블의 현재 주소가 아니라 전표에 기록된 `BillingCountry`다. 이 결과는 샘플 DB의 판매 총액이며 실제 시장 통계가 아니다.

## 19. LangChain SQLDatabase로 연결하기

```python
from langchain_community.utilities import SQLDatabase


db = SQLDatabase.from_uri(
    f"sqlite:///{path.resolve().as_posix()}"
)

print("DB 종류:", db.dialect)
print("테이블:", db.get_usable_table_names())
print("\nInvoice 테이블 구조 일부:")
print(db.get_table_info(["Invoice"])[:1200])
```

원본 노트북에는 이 셀의 저장된 출력이 없다. 아래 설명은 함수의 역할과 실제 SQLite 파일의 구조를 기준으로 한 것이며, 저장된 실행 결과처럼 꾸민 것은 아니다.

| 코드 | 역할 |
|---|---|
| `SQLDatabase.from_uri(...)` | SQLAlchemy URI로 DB 연결 객체 구성 |
| `path.resolve()` | DB 파일 절대 경로 구성 |
| `.as_posix()` | 경로 구분자를 `/` 형태로 표현 |
| `db.dialect` | DB 방언 이름. 이 경우 `sqlite` |
| `get_usable_table_names()` | 연결 설정에서 사용 가능한 테이블 이름 목록 |
| `get_table_info(["Invoice"])` | 지정한 테이블의 구조 등 정보 조회 |
| `[:1200]` | 반환 문자열 앞 1,200자만 표시 |

`SQLDatabase`는 DB에 접근하는 도구이지, 그 자체가 질문을 이해하거나 SQL을 만드는 언어 모델은 아니다.

### SQLite URI 읽기

```text
sqlite:/// + 절대 파일 경로

예시:
sqlite:////Users/example/project/data/Chinook.db
```

예시 경로는 설명용이다. macOS의 절대 경로는 `/`로 시작하므로 `sqlite:///` 뒤에 붙이면 연속된 슬래시가 네 개 보일 수 있다.

### 테이블 구조가 필요한 이유

`Invoice`에는 `InvoiceId`, `CustomerId`, `InvoiceDate`, `BillingCountry`, `Total` 등의 컬럼이 있다. 모델이 나중에 SQL을 작성하려면 실제 테이블명과 컬럼명, 연결 관계를 알아야 한다.

```text
질문: 국가별 판매 총액 상위 5개를 보여줘
    |
    v
필요한 구조 확인
Invoice.BillingCountry: 묶을 기준
Invoice.Total: 합산할 금액
    |
    v
GROUP BY + SUM + ORDER BY + LIMIT가 필요함을 판단
```

다만 현재 예제에서는 사람이 SQL을 직접 작성했다. 위의 자연어 질문에서 SQL을 생성하는 모델 호출은 아직 없다.

## 20. PDF RAG와 SQL 기반 질의응답 비교

| 구분 | PDF 기반 RAG | SQL 기반 질의응답 |
|---|---|---|
| 데이터 형태 | 문단과 보고서 본문 | 테이블의 행·컬럼·관계 |
| 정보를 찾는 방법 | 관련 청크 검색 | 조건·JOIN·집계로 조회 |
| 모델에 필요한 정보 | 검색된 문서와 출처 | DB 구조와 질문, 실행 결과 |
| 출처 확인 | PDF 페이지와 청크 | 사용한 SQL과 조회 결과 |
| 이번 구현 | 문서 검색 후 모델 답변까지 구현 | 수동 SQL 조회와 SQLDatabase 연결 코드까지 작성 |

SQL 질의응답이 반드시 벡터 검색을 사용하는 것은 아니다. 스키마를 참고해 SQL을 만들고 실행하는 Text-to-SQL 구조와, 문서 청크를 찾는 RAG는 역할을 구분해 이해해야 한다.

LangChain의 SQL Agent 예제도 테이블·스키마 확인, 쿼리 생성, 검토, 실행, 결과 설명을 구분한다. 모델이 생성한 SQL을 실행할 때는 필요한 최소 DB 권한과 검증이 필요하다. **DB에 연결했다는 사실이 읽기 전용을 보장하지는 않는다.** [LangChain SQL Agent 설명](https://docs.langchain.com/oss/python/langchain/sql-agent)

## 21. 구현 범위 정리

| 항목 | 현재 상태 |
|---|---|
| PDF 검색 결과 최대 4개 선택 | 구현 |
| 검색 청크에 PDF 페이지 표시 | 구현 |
| PDF 내용을 넣어 모델 답변 생성 | 구현 및 저장된 답변 있음 |
| BM25·벡터 검색기 선택 | 대화형 메뉴로 구현 |
| API 키 없이 검색 페이지 출력 | 원본 반환값에 `sources` 누락. 문서에 보완 예시 제시 |
| 답변의 인용 페이지 검증 | 구현되지 않음 |
| 질문·검색기 조합 자동 평가 | 원본에는 없음. 문서에 출력 비교 예시만 추가 |
| 이전 대화 맥락 기억 | 구현되지 않음 |
| SQLite 학생 DB 생성·삽입·조회 | 구현 및 저장된 출력 있음 |
| Chinook JOIN·국가별 집계 | 구현 및 저장된 출력 있음 |
| LangChain SQLDatabase 연결 | 코드 작성됨. 원본 셀의 저장된 출력은 없음 |
| LLM의 SQL 자동 생성·검증·실행 | 아직 없음 |

## 22. 핵심 정리

1. PDF 기반 답변은 검색한 문서와 질문을 모델에 함께 전달해 생성한다.
2. `sources`는 검색된 페이지 목록이다. 실제 답변에 사용된 근거와 일치하는지는 따로 확인해야 한다.
3. 반환값의 구조는 정상 응답·검색 결과 없음·API 키 없음 경로에서 일관되게 유지하는 것이 좋다.
4. SQLite는 파일 기반 DB로 사용할 수 있고, Python의 `sqlite3`로 SQL을 실행할 수 있다.
5. `?` placeholder로 값을 바인딩하고, `fetchall()`이나 pandas로 조회 결과를 확인한다.
6. JOIN은 테이블 관계를 연결하고, GROUP BY와 집계 함수는 묶음별 결과를 계산한다.
7. `SQLDatabase` 연결과 SQL 자동 생성은 다르다. 이번 SQL 예제는 구조 확인과 수동 조회 단계까지다.
