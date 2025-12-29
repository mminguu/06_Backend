from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware # Django(8000) 와 FastAPI(8001) 연동 시 필요 CORS 문제 해결 / 다른 도메인의 접근 허용하게 해줌
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine , get_db


app = FastAPI(
    title="Product API",
    description='제품관리'
)

# 라우터 설정
@app.get('/')
def root():
    return {"message":"Welcome to the Product API"}