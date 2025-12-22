# pydantic 데이터 검증하기
# 복잡한 데이터를 안전하게 받고 검증
from fastapi import FastAPI
from pydantic import BaseModel , Field , EmailStr
from typing import Optional
# BaseModel pydantic 의 기본 클래스
# Field 검증 규칙 추가
# name:str = Field ()
# price:int = Field ()
# ... 필수항목

app = FastAPI(
    title='pydantic 데이터 검증',
    description='데이터 모델 정의 및 검증',
    version='0.0.1'
)

class Item(BaseModel):
    '''상품 정보 모델'''
    name : str
    price : int

@app.post('/item/simple')