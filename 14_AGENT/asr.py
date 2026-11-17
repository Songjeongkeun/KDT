import numpy as np
import os
import torch
from qwen_asr import Qwen3ASRModel
# 관련 정보를 하나의 객체로 묶어 관리하는 decorator 
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TARGET_SR = 16000
ASR_MODE_ENV = os.getenv("ASR_MODE", "auto").strip().lower()
ASR_MODEL_PATH = os.getenv("ASR_MODEL_PATH", "Qwen/Qwen3-ASR-1.7B")
ASR_LANGUAGE = os.getenv("ASR_LANGUAGE", "Korean")
MAX_SECONDS = float(os.getenv("ASR_MAX_SECONDS", 20))
SILENCE_RMS = float(os.getenv("ASR_SILENCE_RMS", 0.01))

MOCK_TRANSCRIPT = (
    "김사과: 이번 주 목표 공유\n"
    "이메론: API 완료 예정\n"
    "김사과: 문서화는 반하나가 담당하세요.\n"
    "반하나: 그럼 김사과가 README 작성 해야 함"
)

_model = None


# 형식을 지정하기 위해서 사용
@dataclass
class AudioFeatures:
    wav: np.ndarray         # 음성 파일 > 음성 샘플 배열
    sample_rate: int        # 샘플링 레이트
    rms: float              # 음성 신호의 전반적인 크기. 정규화된 음성 샘픙을 기준으로 비교, 이유: 목소리 크기(진폭)이 차이가 클 수가 있기 떄문에 정규화 시켜주기 위해 사용
    peak: float             # 음성 신호에서 절댓값이 가장 큰 샘플의 크기
    skipped_silence: bool   # 무음으로 판단하여 음성 인식을 건너뛰었는지 여부를 저장하기 위한 필드 / True: 무음으로 판단해서 건너뜀
    path: str               # 음성 파일의 경로
    
@dataclass
class TranscriptResult:
    text: str               # 인식된 음성 텍스트
    # qwen 인지 mock 인지 선택
    mode: str               # 사용한 인식 방식
    rms: float              # 입력 음성의 RMS
    peak: float             # 입력 음성의 Peak
    skipped_silence: bool   # 무음으로 인한 인식 생략 여부
    detail: str             # 처리 과정에 대한 추가 설명


# 음성 파일을 불러와 모노(단일 채널)로 변환하고, 샘플링 레이트를 16,000Hz로 통일
# 반환값: 음성 샘플 배열, 샘플링 레이트
def load_audio_file(path: str | Path) -> tuple[np.ndarray, int]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"음성 파일 없음: {path}")
    try:
        import soundfile as sf
    except ImportError as e:
        raise ImportError("soundfile 모듈 에러!") from e
    # wav: 음성 샘플 배열 / sr: 기존 샘플링 레이트
    # always_2d=True: 모노, 스테레오와 관계없이 스테레오(2차원 배열)로 반환
    # ex) 5초짜리 44100hz가 있다면 채널당 220500 샘플이 있음(5 x 44100)
    wav, sr = sf.read(str(path), dtype="float32", always_2d=True)
    # 채널별 평균을 계산하여 모노(단일 채널)로 변환
    wav = wav.mean(axis=1)
    # 기존 샘플링 레이트가 목표값(TARGET_SR, 16000Hz)과 다르면 리샘플링
    if sr != TARGET_SR:
        # duration: 전체 음성 길이 계산 (1초 단위)
        # len(wav): 음성 샘플 수
        duration = len(wav) / sr
        # 목표 샘플링 레이트에 맞는 샘플 개수 계산 (최소 1개 <- (round(duration * TARGET_SR))의 최대값을 사용하지만 1보다 작을 시 1 사용)
        new_len = max(1, int(round(duration * TARGET_SR)))
        # interp: 1차원 선형 보간. 기존에 측정한 샘플 사이의 값을 직선으로 연결하여 새로운 위치의 값을 추정
        # 보간(Interpolation): 이미 알고 있는 데이터 사이에서 모르는 값을 추정하는 것
        # 1차원 선형 보간법인 이유: 시간(x축)에 따른 음성 진폭 추정 / 음성의 시간이라는 하나의 독립 변수를 기준으로 값을 측정하기 때문
        # interp(새롭게 값을 구하려는 위치, 기존 데이터의 위치, 기존 위치에 해당하는 실제 값)
        # linspace: 지정한 구간에 일정한 간격으로 숫자를 생성 -> ex) linspace(0, 1, 4)라면 [0, 0.25, 0.5, 0.75]가 생성됨
        # endpoint=False: 마지막 값 생략. 마지막 값: linspace() 두 번째에 오는 값(위 예제라면 0, 1, 4 중 1이 마지막 값임)
        # => 기존 시간과 진폭을 참고하여 새로운 시간 좌표에서 진폭을 계산
        wav = np.interp(
            # 새로운 음성 샘플의 시간 위치
            np.linspace(0, duration, new_len, endpoint=False),
            # 기존 음성 샘플의 시간 위치
            np.arange(len(wav)) / sr,
            # 기존 음성 샘플 값
            wav
        ).astype(np.float32)
        sr = TARGET_SR
    # 최대 음성 처리 시간이 0보다 큰 경우에만 길이 제한
    if MAX_SECONDS > 0:
        # 최대 처리 시간에 해당하는 샘플 개수만큼 음성 데이터 자르기
        wav = wav[: int(MAX_SECONDS * TARGET_SR)]
    # 음성 데이터를 float32 자료형으로 변환하고 샘플링 레이트와 함께 반환
    return wav.astype(np.float32), sr

def compute_rms(wav: np.ndarray) -> float:
    if wav.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(wav**2)))

def peak_normalize(wav: np.ndarray, target: float = 0.9) -> np.ndarray:
    peak = float(np.max(np.abs(wav))) if wav.size else 0.0
    if 1e-6 <= peak < target:
        return (wav * (target / peak)).astype(np.float32)
    return wav.astype(np.float32)

    
# RMS: 음성 신호의 평균적인 크기를 측정
# Peak: 음성 신호에서 가장 큰 진폭을 측정
# Peak Normalization: 가장 큰 진폭을 기준으로 음성 전체의 크기를 조절
# 같은 사람이 같은 문장을 녹음하더라도 녹음 환경에 따라 음성 신호의 크기가 달라짐 > 정규화
def preprocess_audio_file(path: str | Path) -> AudioFeatures:
    wav, sr = load_audio_file(path)
    rms = compute_rms(wav)
    peak = float(np.max(np.abs(wav))) if wav.size else 0.0
    skipped = rms < SILENCE_RMS
    if not skipped:
        wav = peak_normalize(wav)
        peak = float(np.max(np.abs(wav))) if wav.size else 0.0
        rms = compute_rms(wav)
    return AudioFeatures(
        wav = wav,
        sample_rate=sr,
        rms=rms,
        peak=peak,
        skipped_silence=skipped,
        path=str(path)
    )
    
def _get_qwen_model():
    global _model
    if _model is not None:
        return _model
    # if not torch.cuda.is_available():
    #     raise RuntimeError("GPU가 필요!")
    if not torch.backends.mps.is_available():
        raise RuntimeError("GPUT가 필요!")
    dtype = (torch.float16 if os.getenv("ASR_DTYPE", "bfloat16").lower() == "float16" else torch.bfloat16)
    _model = Qwen3ASRModel.from_pretrained(
        ASR_MODEL_PATH, dtype=dtype, device_map="mps", max_inference_batch_size=1, max_new_tokens=256
    )
    return _model

def transcribe_features(features: AudioFeatures, mode: str | None = None) -> TranscriptResult:
    mode = mode or resolve_asr_mode()
    if features.skipped_silence:
        return TranscriptResult(
            text="",
            mode=mode,
            rms=features.rms,
            peak=features.rms,
            skipped_silence=True,
            detail=f"무음으로 건너뜀 (RMS={features.rms:.4f} < {SILENCE_RMS})"
        )
        
    if mode == "qwen":
        model = _get_qwen_model()
        result = model.transcribe(audio=(features.wav, features.sample_rate), language=ASR_LANGUAGE)
        text = (getattr(result[0], "text", "") or "").strip()
        return TranscriptResult(
            text=text,
            mode="qwen",
            rms=features.rms,
            peak=features.peak,
            skipped_silence=False,
            detail="Qwen3-ASR 실전사"
        )
        
    return TranscriptResult(
        text=MOCK_TRANSCRIPT,
        mode="mock",
        rms=features.rms,
        peak=features.peak,
        skipped_silence=False,
        detail=f"mock 전사"
    )
        
def resolve_asr_mode() -> str:
    if ASR_MODE_ENV in {"qwen", "mock"}:
        return ASR_MODE_ENV
    try:
        if torch.backends.mps.is_available():
            return "qwen"
    except Exception:
        pass
    return "mock"

def asr_status() -> dict:
    mode = resolve_asr_mode()
    # cuda = False
    mps = False
    qwen = False
    try:
        import torch
        # cuda = bool(torch.cuda.is_available())
        mps = bool(torch.backends.mps.is_available())
    except Exception: 
        # cuda = False
        mps = False
    try:
        import qwen_asr
        qwen = True
    except Exception:
        qwen = False
    return {
        "mode": mode,
        "requested": ASR_MODE_ENV,
        # "cuda": cuda,
        "mps": mps,
        "qwen_asr_installed": qwen,
        "model_path": ASR_MODEL_PATH,
        "silence_rms": SILENCE_RMS,
        "max_seconds": MAX_SECONDS,
        "markdown": (
            f"### ASR 상태\n\n"
            f"- 사용 모드: {mode}\n"
            f"- 요청 모드: {ASR_MODE_ENV}\n"
            # f"- CUDA: {cuda}\n"
            f"- MPS: {mps}\n"
            f"- qwen_asr: {qwen}\n"
            f"- 모델: {ASR_MODEL_PATH}\n"
            f"- 무음 RMS 임계값: {SILENCE_RMS}\n\n"
        )
    }
    
def transcribe_file(path: str | Path) -> TranscriptResult:
    features = preprocess_audio_file(path)
    return transcribe_features(features)