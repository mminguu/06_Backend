from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models
import secrets
# 보안 설정

SECRET_KEY = secrets.token_urlsafe(64)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/auth/token") 
# 실제 로그인 api endpoint를 지정하고 아이디와 패스워드를 보내서 토큰을 받음

def verify_password(plain_password:str, hashed_password:str) -> bool:
    '''패스워드 검증'''
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str)->str:
    '''패스워드 해시 생성'''
    return pwd_context.hash(password)


def create_access_token(data:dict, expires_delta:Optional[timedelta]=None):
    '''액세스 토큰 생성'''
    to_encode = data.copy()
    if expires_delta:        
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    print("SECRET_KEY:" , SECRET_KEY)