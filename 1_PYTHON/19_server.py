import os
from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from fastapi import FastAPI, HTTPException
from pymongo.errors import PyMongoError

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_URL = os.getenv("DB_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

mongo_client = MongoClient(DB_URL, serverSelectionTimeoutMS=5000)

database = mongo_client['ai']
collection = database['ad']

class ProductRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=100, description="광고할 제품 이름")
    details: str = Field(min_length=1, max_length=1000, description="제품의 주요 특징과 설명")
    tone_and_manner: str = Field(min_length=1, max_length=200, description="광고 문구의 분위기와 스타일")

class AdData(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str
    ad: str

class AdResponse(BaseModel):
    ad: str
    datas: List[AdData]

class AdGenerator:
    def __init__(self, model: str = "gpt-5-nano"):
        self.model = model

    def using_llm(self, prompt: str) -> str:
        developer_instruction = """
        당신은 전문 광고 카피라이터입니다.

        사용자가 제공한 제품 이름, 주요 내용, 광고 문구 스타일을 분석하여 자연스럽고 기억하기 쉬운 한국어 광고 문구를 작성하세요.

        다음 규칙을 반드시 지키세요.
        1. 광고 문구는 한 문장으로 작성합니다.
        2. 제품의 특징이 문구에 반영되어야 합니다.
        3. 사용자가 지정한 분위기와 스타일을 반영합니다.
        4. 지나치게 허위이거나 검증되지 않은 효과는 단정하지 않습니다.
        5. 설명, 제목, 따옴표 없이 광고 문구만 출력합니다.
""".strip()

        try:
            response = client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "developer",
                        "content": developer_instruction
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                reasoning={"effort": "low"},
                max_output_tokens=1000
            )
            result = response.output_text.strip()
            if not result:
                raise ValueError("모델이 빈 응답을 반환했습니다.")
            return result

        except Exception as e:
            print(f'API 오류: {e}')
            raise HTTPException(
                status_code=502,
                detail="광고 문구 생성 중 AI 서버 오류가 발생했습니다."
            ) from e


    def generate(self, product_name: str, details: str, tone_and_manner: str) -> str:
        prompt = f"""
        제품 이름: {product_name}
        제품 주요 내용: {details}
        광고 문구 스타일: {tone_and_manner}

        위 정보를 바탕으로 광고 문구를 한 문장으로 작성하세요.
        """.strip()
        return self.using_llm(prompt)
    
ad_generator = AdGenerator()
app = FastAPI(title="AI 광고 문구 생성 API", description="GPT 모델과 MongoDB를 이용한 광고 문구 생성 API", version="1.0.0")

@app.get("/")
def root():
    return { "message": "AI 광고 문구 생성 API가 실행 중입니다." }

@app.post("/create_ad", response_model=AdResponse)
def create_ad(product: ProductRequest):
    generated_ad = ad_generator.generate(
        product_name=product.product_name, 
        details=product.details, 
        tone_and_manner=product.tone_and_manner
    )
    document = {
        "product_name": product.product_name,
        "details": product.details,
        "tone_and_manner": product.tone_and_manner,
        "ad": generated_ad
    }
    try:
        collection.insert_one(document)
        cursor = (
            collection.find({}, {"_id": 0})
            .sort("_id", DESCENDING)
            .limit(20)
        )
        datas = list(cursor)
    
    except PyMongoError as e:
        raise HTTPException(
            status_code=503,
            detail="광고 문구 저장 중 데이터베이스 오류가 발생했습니다."
        ) from e
    
    
    return {
        "ad": generated_ad,
        "datas": datas
    }
