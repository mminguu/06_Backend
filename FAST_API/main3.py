from fastapi import FastAPI , HTTPException , status
from pydantic import BaseModel , Field
from typing import Optional
from datetime import datetime

app = FastAPI(
    title='todo crud basic',
    description="",
    version='1.0.0'
)

# 데이터 모델 정의
class TodoCreate(BaseModel):
    '''기본 모델 정보'''
    title:str = Field(...,min_length=1 , max_length=100 , description='할일 제목')
    class Config:
        json_schema_extra = {
            'example':{
                'title' : '할일 제목 넣기'
            }
        }
class TodoResponse(BaseModel):
    '''
    서버가 반환하는 정보
    '''
    id : int
    title : str
    completed : bool
    create_at : str
    class Config:
        json_schema_extra = {
            'example':{
                'id':'1',
                'title':'제목',
                'completed':False,
                'create_at':'2025-12-22 14:30:00'
            }
        }
        
# 글로별 변수
todo = []
next_id = 1

# 라우터
# 라우터 역할을 하는게 app.get // 요청한 주소를 보고 요청한 값을 보고 누구를 실행할지 결정해주는 역할 

@app.get('/')
def index():
    '''메인페이지'''
    return {'message': '메인페이지'}

