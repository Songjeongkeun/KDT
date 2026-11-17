# [96일차] 음성 회의 파이프라인: 전처리, ASR, SQLite 저장

녹음 파일을 올리면 전사 결과만 확인하거나, 전사 내용을 회의록으로 넘겨 요약과 액션 아이템을 저장할 수 있다. 두 기능은 같은 음성 처리 함수를 사용하지만, 회의 DB에 기록하는 것은 음성 파이프라인뿐이다.

```text
Gradio 녹음·파일 선택 → FastAPI 업로드 → asr.py 전처리·전사
    ├─ /transcribe: 전사 텍스트와 진단값 표시
    └─ /pipeline_audio: 전사 텍스트를 회의록으로 전달
                       → graph.py → db.py → 회의 결과와 저장 ID 표시
```

| 파일 | 역할 |
|---|---|
| `4_gradio.py` | 오디오 입력, 파일 전송, 결과 표시 |
| `4_fastapi.py` | 업로드 저장, 전사 API, 회의 파이프라인 호출 |
| `asr.py` | 채널 변환, 리샘플링, 무음 감지, 전사 |
| `graph.py` | 전사 텍스트를 회의록으로 처리하고 회의 ID 반환 |
| `db.py` | 회의록·요약·액션·결과 저장 |

## 1. Gradio에서 오디오 파일 보내기

음성 탭의 `gr.Audio(sources=["microphone", "upload"], type="filepath")`는 녹음 또는 업로드한 오디오의 파일 경로를 콜백에 넘기도록 구성한다.

`_audio_to_path()`는 문자열 경로를 그대로 쓰고, 딕셔너리라면 `path` 또는 `name`을, 리스트나 튜플이라면 첫 항목이 문자열일 때 그 값을 사용한다. 경로를 얻지 못했거나 실제 파일이 없으면 요청을 보내지 않는다.

```python
btn_tr.click(transcribe_audio, inputs=audio, outputs=out_tr)
btn_pipe.click(
    run_audio_pipeline,
    inputs=[a_title, a_people, audio],
    outputs=out_pipe,
)
```

다음은 `run_audio_pipeline()`의 전송 부분이다. `path`는 위에서 검사한 경로이며, `title`과 `people`은 입력란의 값이다.

```python
with open(path, "rb") as f:
    response = requests.post(
        f"{API_URL}/pipeline_audio",
        data={"title": title, "people": people or ""},
        files={"file": (Path(path).name, f, "application/octet-stream")},
        timeout=100,
    )
response.raise_for_status()
```

`files`로 파일 바이트를 전송하고, `data`에는 제목과 참가자를 담는다. 두 값을 함께 보내는 이 요청은 JSON이 아니라 **multipart/form-data**다. `/transcribe`에는 `files`만 보내며, 코드의 타임아웃 설정은 각각 100초와 300초다. [FastAPI 파일과 폼 요청](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/)

두 버튼은 각자 파일을 보내 전사를 실행한다. 먼저 전사 버튼으로 결과를 확인했더라도, 파이프라인 버튼을 누르면 이전 텍스트를 재사용하지 않고 한 번 더 전사한다.

## 2. FastAPI가 업로드를 받는 방식

| API | 입력 | 반환 |
|---|---|---|
| `GET /asr/status` | 없음 | 요청 모드·선택 모드·MPS 등 설정 정보와 표시용 Markdown |
| `POST /transcribe` | `file` | 전사 텍스트, 모드, RMS, Peak, 무음 여부 |
| `POST /pipeline_audio` | `title`, `people`, `file` | 회의 처리 결과, 회의 ID, 전사 텍스트와 진단값 |

```python
@app.post("/pipeline_audio")
async def run_pipeline_audio(
    title: str = Form(...),
    people: str = Form(""),
    file: UploadFile = File(...),
):
    ...
```

`Form(...)`과 `File(...)`로 선언한 제목과 파일은 필수다. 참가자를 생략하면 빈 문자열을 사용한다. FastAPI에서 이 방식의 요청 본문을 처리하려면 `python-multipart`가 필요하다.

두 업로드 API는 `_save_upload()`로 들어온 파일을 `uploads/`에 저장한 뒤, 해당 경로를 `transcribe_file()`에 넘긴다. `shutil.copyfileobj(file.file, out)`은 업로드 파일의 내용을 열린 출력 파일로 복사한다.

> 원본의 `suffix = Path(file.filename or "audio.wav")`는 확장자만 뽑는 코드가 아니다. 일반 파일명이라면 UUID 뒤에 파일명 전체가 붙는다. 실제 서비스에서는 서버가 파일명을 생성하고 허용 형식·파일 크기·보관 기간을 별도로 제한해야 한다. 현재는 요청이 끝나도 복사본을 삭제하지 않는다.

## 3. 음성 입력을 전사에 맞게 전처리하기

```text
오디오 읽기 → 모노 변환 → 16 kHz 리샘플링 → 길이 제한
            → RMS로 무음 확인 → 필요한 경우 진폭 확대
```

### 모노와 16 kHz로 맞추기

아래 코드는 `load_audio_file()`에서 파일을 읽은 뒤 배열을 가공하는 부분이다.

```python
wav, sr = sf.read(str(path), dtype="float32", always_2d=True)
wav = wav.mean(axis=1)

if sr != TARGET_SR:
    duration = len(wav) / sr
    new_len = max(1, int(round(duration * TARGET_SR)))

    wav = np.interp(
        np.linspace(0, duration, new_len, endpoint=False),
        np.arange(len(wav)) / sr,
        wav,
    ).astype(np.float32)
    sr = TARGET_SR

if MAX_SECONDS > 0:
    wav = wav[: int(MAX_SECONDS * TARGET_SR)]
```

`always_2d=True`는 모노 파일도 `(프레임 수, 1)`로 읽게 하는 옵션이다. 모노를 스테레오로 바꾸는 옵션은 아니다. `mean(axis=1)`은 각 시간의 채널 값만 평균 내므로 프레임 수를 그대로 유지한다.

`np.interp()`는 기존 샘플 사이를 직선으로 이어 새 시간 위치의 값을 계산한다. 예를 들어 32 kHz로 기록한 1초 음성은 채널을 합친 뒤에도 32,000개 샘플이지만, 16 kHz로 변환하면 약 16,000개가 된다. 이 코드는 선형 보간을 사용하는 간단한 리샘플링이며, 다운샘플링용 저역통과 필터는 별도로 적용하지 않는다. [NumPy 선형 보간](https://numpy.org/doc/stable/reference/generated/numpy.interp.html)

기본값 `MAX_SECONDS=20`이면 16 kHz 기준 앞의 최대 320,000개 샘플만 남긴다. **파일을 먼저 읽고 변환한 뒤 자르는 코드**라서, 업로드 크기나 전체 디코딩 작업을 제한하는 설정은 아니다.

### RMS와 Peak로 크기 확인하기

```python
def compute_rms(wav: np.ndarray) -> float:
    if wav.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(wav**2)))


def peak_normalize(wav: np.ndarray, target: float = 0.9) -> np.ndarray:
    peak = float(np.max(np.abs(wav))) if wav.size else 0.0
    if 1e-6 <= peak < target:
        return (wav * (target / peak)).astype(np.float32)
    return wav.astype(np.float32)
```

| 값 | 계산 | 어떤 차이를 보여주는가? |
|---|---|---|
| RMS | 각 샘플 제곱 → 평균 → 제곱근 | 구간 전체의 신호 크기 |
| Peak | 샘플 절댓값의 최댓값 | 가장 크게 튄 지점의 크기 |

예를 들어 `[0.0, 0.3, -0.3, 0.0]`의 Peak는 `0.3`이고 RMS는 약 `0.2121`이다. Peak를 `0.9`까지 올리면 전체 배열에 `0.9 / 0.3 = 3`을 곱한다. 원본 함수는 **작은 진폭만 키우며** Peak가 이미 목표 이상이면 낮추지 않는다.

무음 여부는 정규화 **전** RMS가 `SILENCE_RMS`보다 작은지로 판단한다. 먼저 작은 신호를 키우면 무음에 가까운 잡음도 큰 신호처럼 보일 수 있기 때문이다. 무음이 아닌 경우에만 정규화한 뒤 RMS와 Peak를 다시 계산한다. 따라서 정상 결과의 진단값은 모델에 전달되는 배열 기준이다. 이 판단은 신호 세기를 보는 것이지, 실제 발화 구간을 검출하는 것은 아니다.

`AudioFeatures`는 배열·샘플링 레이트·진단값을 묶고, `TranscriptResult`는 전사 텍스트·모드·진단값·처리 설명을 묶는다.

## 4. Qwen 전사와 Mock 전사

| 설정 | 기본값 | 역할 |
|---|---|---|
| `ASR_MODE` | `auto` | MPS 사용 가능 시 `qwen`, 아니면 `mock` 선택 |
| `ASR_MODEL_PATH` | `Qwen/Qwen3-ASR-1.7B` | 사용할 모델이나 로컬 경로 |
| `ASR_LANGUAGE` | `Korean` | 전사 언어 |
| `ASR_MAX_SECONDS` | `20` | 전처리 뒤 남길 최대 길이(0 이하면 이 제한을 적용하지 않음) |
| `ASR_SILENCE_RMS` | `0.01` | 무음 판정 기준 |
| `ASR_DTYPE` | `bfloat16` | `float16`을 명시하면 FP16, 아니면 BF16으로 로딩 |

```python
def transcribe_file(path: str | Path) -> TranscriptResult:
    features = preprocess_audio_file(path)
    return transcribe_features(features)
```

- 무음이면 모델을 불러오지 않고 빈 텍스트와 `skipped_silence=True`를 반환한다.
- `qwen`은 `model.transcribe(audio=(features.wav, features.sample_rate), language=ASR_LANGUAGE)`로 음성을 텍스트로 변환한다.
- `mock`은 음성 내용과 관계없이 코드에 적힌 고정 회의록을 반환한다. 업로드와 DB 저장 흐름을 시험하기 위한 모드다.

Qwen 모델은 `_get_qwen_model()`에서 처음 필요할 때 MPS에 로딩한다. 이후 같은 프로세스에서는 `_model`에 보관한 객체를 재사용한다. `auto`는 모드를 고르는 규칙일 뿐, 모델 로딩이나 추론에 실패하면 자동으로 Mock으로 재시도하는 기능은 아니다. 상태 API가 `qwen`을 표시해도 모델이 이미 로딩됐거나 추론이 성공했다는 뜻은 아니다.

`mock`을 선택해도 현재 파일은 상단에서 `torch`와 `qwen_asr`를 import한다. **모델 로딩을 건너뛰는 것과 라이브러리 설치가 필요 없는 것은 다르다.**

## 5. 전사 텍스트로 회의 파이프라인 실행하기

`/transcribe`는 전사 결과를 반환하는 데서 끝난다. `/pipeline_audio`는 전사 텍스트를 `notes`로 넣어 회의 처리 함수를 실행한다. 다음은 음성 라우트의 성공 경로다.

```python
result = run_meeting_pipeline(
    title=title,
    people=people,
    notes=tr.text,
    audio_path=str(path),
)
result["transcript"] = tr.text
result["asr_mode"] = tr.mode
result["audio_rms"] = tr.rms
result["audio_peak"] = tr.peak
```

라우트는 이렇게 구성한 `result`를 JSON 응답으로 반환한다. 실제 전사는 **FastAPI 라우트에서 먼저** 실행한다. 그래프에는 모델을 호출하는 노드가 없다. 그래프는 받은 `notes`로 줄 수를 세고, 키워드가 들어간 줄을 액션 아이템으로 뽑는다. ASR 결과에 화자 라벨을 자동으로 붙이는 단계도 없다. Mock 회의록의 이름은 미리 작성한 문자열이다.

### 저장 ID를 JSON에서 읽기

```python
def run_meeting_pipeline(
    title: str, people: str, notes: str = "", audio_path: str = ""
) -> dict:
    final_state = meeting_app.invoke(
        _initial_state(
            title=title, people=people, notes=notes, audio_path=audio_path
        )
    )
    return {
        "result": final_state["result"],
        "meeting_id": final_state.get("meeting_id") or 0,
        "asr_mode": final_state.get("asr_mode") or "",
        "transcript": final_state.get("transcript") or "",
        "notes": final_state.get("notes") or "",
        "audio_rms": final_state.get("audio_rms") or 0.0,
    }
```

`save_meeting()`이 반환한 삽입 ID가 `MeetingState.meeting_id`에 남고, API도 이 값을 별도 필드로 반환한다. Gradio는 `result`를 표시하고 `meeting_id`가 있으면 안내를 덧붙인다. 그래프 결과 문자열에 이미 DB 저장 안내가 있어 화면에서 ID가 두 번 보일 수 있다.

| 데이터 | 실제 위치 |
|---|---|
| 전사 텍스트 | API의 `transcript`·`notes`, DB의 `notes` |
| 요약·액션·회의 결과 | 기존 `meetings` 테이블의 컬럼 |
| ASR 모드·RMS·Peak | 음성 API의 응답. DB에는 전용 컬럼이 없음 |
| 원본 오디오 | `uploads/`의 파일. 경로를 그래프 초기 상태에 넘기지만 DB에는 저장하지 않음 |

## 6. Mock 모드로 확인한 결과

별도의 임시 DB에서 32 kHz 스테레오 테스트 파형을 보냈다. 고정 텍스트를 반환하는 Mock 모드라서 **이 파형에서 실제로 발화를 인식했다는 뜻은 아니다.**

| 요청 | 결과 |
|---|---|
| `GET /asr/status` | `mode: "mock"` |
| `POST /transcribe` | HTTP 200, RMS 약 `0.6364`, Peak 약 `0.9000`, DB에 새 행 없음 |
| `POST /pipeline_audio` | HTTP 200, `meeting_id: 1`, Mock 회의록이 DB의 `notes`에 저장 |
| 무음으로 `POST /transcribe` | HTTP 200, 빈 텍스트, `skipped_silence: true` |
| 무음으로 `POST /pipeline_audio` | HTTP 500, `음성 파이프라인 처리 오류` |

음성 파이프라인의 응답에는 다음 결과가 포함된다.

```text
발화 4줄 / 앞부분: 김사과: 이번 주 목표 공유

- 이메론: API 완료 예정
- 김사과: 문서화는 반하나가 담당하세요.
- 반하나: 그럼 김사과가 README 작성 해야 함

DB 저장됨 - meetings.id = 1
```

### 무음 업로드가 400이 아니라 500인 이유

음성 파이프라인은 빈 전사 결과에서 `HTTPException(400, ...)`을 발생시키지만, 바로 바깥의 `except Exception`이 그것까지 잡아 `500`으로 다시 반환한다. 의도한 응답 코드를 유지하려면 `except HTTPException: raise`를 일반 예외 처리보다 앞에 두거나, 빈 결과 확인을 해당 `try` 블록 밖으로 옮겨야 한다.

무음 결과의 `peak`에 실제 Peak가 아닌 `features.rms`를 넣는 부분도 있다. 완전한 무음에서는 둘 다 0이라 드러나지 않지만, 작은 소리가 들어온 경우 화면의 Peak가 실제 최댓값과 다를 수 있다.
