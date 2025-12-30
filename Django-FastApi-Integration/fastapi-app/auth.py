from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models
import secrets
# 보안 설정
# secrets.token_urlsafe(64) 이 값을 한번 생성해서 .evn에 등록하고 사용해야 함(release 모드)
SECRET_KEY = secrets.token_urlsafe(64)  # 서버실행시 기준 키를 재 발행.. 모든사용자 토큰 무효화 -> 강제 로그아웃
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")  # 로그인 api 앤드포인트 지정, 아이디/패스워드를 보내서 토큰을 받음


def get_password_hash(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return ph.verify(hashed_password, plain_password)


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

def authenticate_user(db:Session, username:str, password:str):
    '''사용자 인증'''
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    '''현재 사용자 정보 가져오기'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user:models.User = Depends(get_current_user)):
    '''활성화된 현재 사용자 정보 가져오기'''
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def check_permission(user:models.User, required_role:str)->bool:
    '''사용자 권한 확인'''
    # 숫자 클수록 권한이 높다
    role_hierarchy = {
        "admin": 3,
        "manager": 2,
        "user": 1
    }
    user_level = role_hierarchy.get(user.role,0)
    required_level = role_hierarchy.get(required_role,0)
    return user_level >= required_level


if __name__ == "__main__":
    print("SECRET_KEY:", SECRET_KEY)