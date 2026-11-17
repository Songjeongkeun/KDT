# [94일차] LangGraph 회의 파이프라인과 SQLite 저장

회의 제목, 참가자, 회의록을 입력하면 회의 정보와 요약, 할 일을 한 화면에 보여준다. 정상 입력은 처리 결과와 함께 SQLite에 저장한다.

```text
Gradio의 전체 파이프라인 탭
    → POST /pipeline
    → LangGraph: 검증 → 회의 정보 → 요약 → 액션 추출 → 결과 조합
    → SQLite 저장
    → Markdown 결과를 Gradio에 표시
```

| 파일 | 담당하는 일 |
|---|---|
| `4_gradio.py` | 입력값을 서버에 보내고 반환된 Markdown을 표시 |
| `4_fastapi.py` | 서버 시작 시 테이블을 준비하고 `/pipeline` 요청을 처리 |
| `graph.py` | 입력에 따라 실행 경로를 선택하고 회의 결과 생성 |
| `db.py` | SQLite 테이블 생성, 회의 데이터 저장 |

## 1. 서버가 시작될 때 테이블 준비하기

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from db import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="회의 관리 API", lifespan=lifespan)
```

FastAPI는 요청을 받기 전에 `yield` 앞의 `init_db()`를 실행한다. 

## 2. POST /pipeline으로 세 입력값 받기

```python
from pydantic import BaseModel
from graph import run_meeting_pipeline


class PipelineRequest(BaseModel):
    title: str
    people: str
    notes: str


@app.post("/pipeline")
def run_pipeline(request: PipelineRequest):
    return {
        "result": run_meeting_pipeline(
            title=request.title,
            people=request.people,
            notes=request.notes,
        )
    }
```

요청은 제목, 참가자, 회의록을 JSON으로 보낸다. 응답의 `result`는 처리 결과 전체를 담은 **Markdown 문자열**이다.

```json
{
  "title": "주간 회의",
  "people": "김사과, 이메론",
  "notes": "김사과: 목표 공유\n이메론: API 완료 예정"
}
```

검증은 두 곳에서 나뉘어 이루어진다. 요청에서 필수 필드가 빠지면 FastAPI가 `422`를 반환한다. 필드가 있더라도 제목이나 회의록이 공백뿐이면 그래프의 `validate_input()`에서 잡는다. 

 HTTP `200`과 오류 문구가 담긴 `result`를 반환한다.

## 3. 그래프에 전달할 상태

```python
from typing import TypedDict


class MeetingState(TypedDict):
    title: str
    people: str
    notes: str
    error: str
    meeting_info: str
    summary: str
    actions: str
    result: str
```

| 상태 필드 | 내용 |
|---|---|
| `title`, `people`, `notes` | 요청으로 받은 원본 입력 |
| `error` | 검증 실패 이유. 정상이라면 빈 문자열 |
| `meeting_info`, `summary`, `actions` | 각 노드가 만든 중간 결과 |
| `result` | 화면에 표시할 최종 Markdown |

`run_meeting_pipeline()`은 입력값과 빈 중간 결과를 넣어 그래프를 실행한다. 각 노드는 `{**state, "필드": 새_값}` 형태로 기존 상태를 유지하고 해당 필드만 바꾼 딕셔너리를 반환한다.

```python
meeting_app = build_meeting_graph()


def run_meeting_pipeline(title: str, people: str, notes: str) -> str:
    final_state = meeting_app.invoke({
        "title": title,
        "people": people,
        "notes": notes,
        "error": "",
        "meeting_info": "",
        "summary": "",
        "actions": "",
        "result": "",
    })
    return final_state["result"]
```

`meeting_app`은 모듈을 불러올 때 만든 실행 가능한 그래프다. 

요청마다 새 그래프를 조립하지 않고, 새 입력 상태로 `invoke()`를 호출한다.

## 4. 검증 결과에 따라 실행 경로 나누기

```python
def validate_input(state: MeetingState) -> MeetingState:
    title = (state.get("title") or "").strip()
    notes = (state.get("notes") or "").strip()

    if not title:
        return {**state, "error": "제목을 입력하세요."}
    if not notes:
        return {**state, "error": "회의록이 비어 있습니다."}
    return {**state, "error": ""}


def route_after_validate(state: MeetingState) -> str:
    return "error" if state.get("error") else "ok"


def route_after_compose(state: MeetingState) -> str:
    return "error" if state.get("error") else "save"
```

`validate_input()`은 통과 여부를 판단하고 `error`를 채운다. 라우팅 함수는 그 값을 보고 다음 노드를 선택한다. 참가자는 비어 있어도 실행할 수 있고, 회의 정보에는 `(없음)`으로 표시된다.

검증에서 `strip()`을 사용한 것은 공백만 있는지 확인하기 위해서다. 이 함수가 반환하는 상태에는 공백을 정리한 제목이나 회의록을 다시 넣지 않으므로, 저장되는 `title`과 `notes`에는 입력한 원문이 남는다.

### 노드와 연결

```python
from langgraph.graph import START, END, StateGraph


def build_meeting_graph():
    graph = StateGraph(MeetingState)
    graph.add_node("validate", validate_input)
    graph.add_node("create_meeting", create_meeting)
    graph.add_node("summarize", summarize_notes)
    graph.add_node("extract_actions", extract_actions)
    graph.add_node("compose", compose_result)
    graph.add_node("save_to_db", save_to_db)

    graph.add_edge(START, "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validate,
        {"ok": "create_meeting", "error": "compose"},
    )
    graph.add_edge("create_meeting", "summarize")
    graph.add_edge("summarize", "extract_actions")
    graph.add_edge("extract_actions", "compose")
    graph.add_conditional_edges(
        "compose",
        route_after_compose,
        {"save": "save_to_db", "error": END},
    )
    graph.add_edge("compose", END)
    return graph.compile()
```

| 입력 | 실행 경로 |
|---|---|
| 정상 | 검증 → 회의 정보 → 요약 → 액션 추출 → 결과 조합 → 저장 |
| 오류 | 검증 → 오류 문구 조합 → 종료. DB에는 저장하지 않음 |

`compose`는 성공 결과와 오류 문구를 모두 만드는 노드다. 오류 상태라면 `meeting_info`나 `summary`가 만들어지지 않았더라도 먼저 오류 문구를 반환한다.

## 5. 회의록에서 액션 아이템 추출하기

```python
def extract_actions(state: MeetingState) -> MeetingState:
    keywords = ("예정", "할", "todo", "해야", "담당")
    found = []

    for line in state["notes"].splitlines():
        text = line.strip()
        if text and any(k in text.lower() for k in keywords):
            found.append(f"- {text}")

    actions = "\n".join(found) if found else "- (추출된 액션 없음)"
    return {**state, "actions": actions}
```

회의록을 줄 단위로 읽고, 키워드 중 하나라도 포함한 줄을 목록에 넣는다. 문장을 나누거나 담당자와 마감일을 따로 분석하는 기능은 아니다. 

```text
입력:
김사과: 목표 공유
이메론: API 완료 예정

추출 결과:
- 이메론: API 완료 예정
```

`summarize_notes()`는 빈 줄을 빼고 줄 수와 첫 줄의 앞부분을 표시한다. 

### 최종 Markdown 조합

```python
def compose_result(state: MeetingState) -> MeetingState:
    if state.get("error"):
        return {**state, "result": f"### 오류\n{state['error']}"}

    result = (
        "### 회의 파이프라인 결과\n\n"
        f"1. 회의 정보\n{state['meeting_info']}\n\n"
        f"2. 요약\n{state['summary']}\n\n"
        f"3. 액션 아이템\n{state['actions']}"
    )
    return {**state, "result": result}
```

각 노드의 결과를 한 문자열로 묶는다. 저장 노드는 이 문자열을 DB에 넣은 뒤 저장 ID 안내를 붙인다.

## 6. SQLite에 원문과 처리 결과 저장하기

### 파일 위치와 테이블

```python
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "meetings.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            create table if not exists meetings (
                id integer primary key autoincrement,
                title varchar(1000) not null,
                people varchar(1000) not null,
                notes text not null,
                summary text not null,
                actions text not null,
                result text not null,
                created_at varchar(1000) not null
            )
        """)
        conn.commit()
```

 `IF NOT EXISTS`를 사용하므로 서버를 다시 시작해도 이미 있는 테이블을 삭제하거나 비우지 않는다. 기존 테이블의 컬럼을 새 정의에 맞춰 변경하는 구문도 아니다.

`row_factory = sqlite3.Row`는 조회할 때 행을 `row["title"]`처럼 컬럼명으로 읽을 수 있게 하는 설정이다. 

### 삽입 후 ID 반환하기

```python
from datetime import datetime, timezone


def save_meeting(
    title: str,
    people: str,
    notes: str,
    summary: str,
    actions: str,
    result: str,
) -> int:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            insert into meetings (
                title, people, notes, summary, actions, result, created_at
            ) values (?, ?, ?, ?, ?, ?, ?)
            """,
            (title, people, notes, summary, actions, result, created_at),
        )
        conn.commit()

    return int(cursor.lastrowid)
```

입력 원문과 계산한 결과를 함께 저장한다. 예를 들어 `people` 컬럼에는 쉼표를 포함한 참가자 문자열을, `result`에는 사용자에게 보여줄 회의 정보·요약·액션 목록을 담는다.

- `created_at`은 저장 시각을 UTC ISO 8601 문자열로 남긴다. `+00:00`은 UTC 오프셋이다.
- SQL의 `?`에는 제목과 회의록 등 입력값을 순서대로 바인딩한다.
- `cursor.lastrowid`로 이번에 삽입한 행의 ID를 확인한다.

`with get_connection() as conn`은 트랜잭션의 완료·롤백을 관리하지만 연결을 자동으로 닫지는 않는다. 연결을 명시적으로 관리해야 할 때는 `close()`나 `contextlib.closing()`을 사용한다. [sqlite3 연결 컨텍스트 매니저](https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager)

### 저장 ID는 어디에 들어가는가?

```python
def save_to_db(state: MeetingState) -> MeetingState:
    meeting_id = save_meeting(
        title=state["title"],
        people=(state.get("people") or "").strip(),
        notes=state["notes"],
        summary=state["summary"],
        actions=state["actions"],
        result=state["result"],
    )
    result = state["result"] + f"\n\nDB 저장됨 - meetings.id = {meeting_id}"
    return {**state, "meeting_id": meeting_id, "result": result}
```

`save_meeting()`에 전달한 `result`는 저장 안내가 붙기 전 문자열이다. 따라서 **DB의 result 컬럼에는 저장 안내가 없고, 응답 Markdown에는 저장 ID가 붙는다.**

노드는 `meeting_id`도 반환하지만 `MeetingState`에 그 필드가 없어, 실제 최종 상태에는 별도 키로 남지 않았다. API도 `result`만 응답하므로 ID를 구조화된 필드로 사용하려면 상태와 응답에 각각 추가해야 한다.

## 7. Gradio에서 전체 파이프라인 실행하기

### 공통 API 호출 함수

```python
import requests

API_URL = "http://127.0.0.1:8000"


def call_api(path: str, payload: dict) -> str:
    try:
        response = requests.post(
            f"{API_URL}{path}",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["result"]
    except (requests.RequestException, ValueError, KeyError) as e:
        return f"서버 통신 오류: {e}"


def run_pipeline(title: str, people: str, notes: str) -> str:
    return call_api(
        "/pipeline",
        {"title": title, "people": people, "notes": notes},
    )
```

각 버튼의 콜백은 경로와 요청 데이터를 정하고, HTTP 전송과 응답 처리는 `call_api()`가 맡는다. `raise_for_status()`는 HTTP 오류를 확인한다. 응답이 `200`이고 `result`에 오류 문구가 담긴 경우에는 그대로 화면에 보여준다.

### 세 번째 탭 연결

```python
with gr.Tab("3. 전체 파이프라인"):
    p_title = gr.Textbox(label="제목", value="주간 회의")
    p_people = gr.Textbox(label="참가자(쉼표)", value="김사과, 이메론")
    p_notes = gr.Textbox(
        label="회의록",
        lines=6,
        value="김사과: 목표 공유\n이메론: API 완료 예정",
    )
    btn3 = gr.Button("파이프라인 실행", variant="primary")
    out3 = gr.Markdown()

    btn3.click(
        run_pipeline,
        inputs=[p_title, p_people, p_notes],
        outputs=out3,
    )
```

제목·참가자·회의록을 한 요청에 담아 보낸다. 서버가 그래프를 실행하고 반환한 Markdown을 `out3`에 표시한다.

**저장된 회의 탭:** 목록 새로고침 버튼, 회의 ID 입력란, 상세 조회 버튼은 화면에 있다. 두 버튼의 콜백이 주석 처리되어 있고 서버에 조회 라우트도 없다. 현재는 파이프라인의 **저장까지** 동작하며, 저장 목록과 상세 결과를 UI에서 불러오는 기능은 연결되지 않았다.

## 8. 실행과 결과 확인

파일이 있는 폴더에서 FastAPI와 Gradio를 각 터미널에서 실행한다.

```bash
python -m uvicorn 4_fastapi:app --reload --port 8000
```

```bash
python 4_gradio.py
```

Gradio 화면은 `http://127.0.0.1:9999`에서 열린다. 세 번째 탭의 기본 입력을 임시 DB로 실행하면 다음과 같은 Markdown이 반환된다. DB가 비어 있을 때 첫 ID는 `1`이며, 기존 DB에서는 저장 ID가 달라진다.

```text
### 회의 파이프라인 결과

1. 회의 정보
### 회의 생성됨
- 제목: 주간 회의
- 참가자: 김사과,이메론

2. 요약
발화 2줄 / 앞부분: 김사과: 목표 공유

3. 액션 아이템
- 이메론: API 완료 예정

DB 저장됨 - meetings.id = 1
```

| 확인한 입력 | 응답 | DB 저장 |
|---|---|---|
| 기본 입력 | 회의 정보, 요약, 액션 아이템, 저장 ID | 새 행 추가 |
| 공백만 있는 제목 | `제목을 입력하세요.` | 없음 |
| 공백만 있는 회의록 | `회의록이 비어 있습니다.` | 없음 |
| `notes` 필드 누락 | HTTP `422` | 없음 |
