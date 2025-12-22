from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional
from datetime import datetime

app =FastAPI()
#CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 모든 도메인 허용
    allow_credentials=True,  # 쿠키/인증정보 포함 요청
    allow_methods=['*'],  # 모든 http method  (get post delete put ...)
    allow_headers=['*'] # 모든 헤더
)
# 정적파일 서빙(css, js, html, 이미지 등)
app.mount('/static',StaticFiles(directory='static'),name='static')

# 데이터 모델
class TodoCreate(BaseModel):
    title:str = Field(...,min_length=1,max_length=200)
    description:Optional[str]=None

class TodoIpdate(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
    completed:Optional[bool] = None

class TodoResponse(BaseModel):
    id:int
    title:str
    description:str
    completed:bool
    created_at:Optional[str] = None
    updated_at:Optional[str] = None 
    

# DB
todo_db=[]
next_id = 0


# 메인페이지
@app.get('/')
def index():
    return FileResponse('static/index.html')

# 데이터추가
@app.post('/api/todos',response_model=TodoResponse,status_code=status.HTTP_201_CREATED )
def create_todo(todo:TodoCreate):
    global next_id
    next_id += 1
    new_data = TodoResponse(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
    )
    todo_db.append(new_data)
    return new_data

@app.get('/api/todos',response_model=list[TodoResponse])
def read_todos():
    return todo_db