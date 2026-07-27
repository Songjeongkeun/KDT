from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

# 정적 파일 (JS, CSS 등) 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML 템플릿 디렉토리
templates = Jinja2Templates(directory="templates")

# HTML 페이지 제공
@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse({"request": request}, "index.html")

# 백엔드 API – JSON 데이터 제공
@app.get("/api/data")
async def get_data():
    return {"message": "FastAPI에서 보내는 데이터입니다"}

users = {
    0: {"userid": "apple", "name": "김사과"},
    1: {"userid": "banana", "name": "반하나"},
    2: {"userid": "orange", "name": "오렌지"}
}

# http://127.0.0.1:8000/users/0
# 사용자 조회
@app.get("/users/{id}")
def find_user(id: int):
    user = users.get(id)
    if user is None:
        return {"error": "해당 id 없음"}
    return user


# http://127.0.0.1:8000/users/0/userid
# 사용자 필드 조회
@app.get("/users/{id}/{key}")
def find_user_by_key(id: int, key: str):
    user = users.get(id)
    if user is None or key not in user:
        return {"error": "잘못된 id 또는 key"}
    return user[key]

# 이름으로 사용자 조회
@app.get("/id-by-name")
def find_user_by_name(name: str):
    for idx, user in users.items():
        if user["name"] == name:
            return user
    return {"error": "데이터를 찾지 못함"}

# 사용자 생성
class User(BaseModel):
    userid: str
    name: str
    
@app.post("/users/{id}")
def create_user(id: int, user: User):
    if id in users:
        return {"error": "이미 존재하는 키"}
    users[id] = user.model_dump()
    return {"success": "ok"}

