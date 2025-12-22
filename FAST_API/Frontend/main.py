# Step 5: 프론트엔드 연동
# 목표: HTML + jQuery와 FastAPI 백엔드 연결하기

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Step 5: TODO with Frontend",
    description="HTML + jQuery 프론트엔드와 연동",
    version="5.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (CSS, JS, 이미지 등)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ============================================
# 데이터 모델
# ============================================
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: str

# ============================================
# 저장소
# ============================================
todos_db = []
next_id = 1

# ============================================
# HTML 페이지 제공
# ============================================
@app.get("/")
def read_index():
    """메인 HTML 페이지 반환"""
    return FileResponse("static/index.html")

# ============================================
# API 엔드포인트
# ============================================

@app.post("/api/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """TODO 추가"""
    global next_id
    
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    todos_db.append(new_todo)
    next_id += 1
    
    print(f"[CREATE] TODO 추가: {new_todo['title']}")
    return new_todo


@app.get("/api/todos", response_model=list[TodoResponse])
def get_all_todos():
    """TODO 목록 조회"""
    print(f"[READ] TODO 조회: {len(todos_db)}개")
    return todos_db


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """특정 TODO 조회"""
    for todo in todos_db:
        if todo["id"] == todo_id:
            return todo
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {todo_id}인 TODO를 찾을 수 없습니다"
    )


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """TODO 수정"""
    for todo in todos_db:
        if todo["id"] == todo_id:
            if todo_update.title is not None:
                todo["title"] = todo_update.title
            if todo_update.description is not None:
                todo["description"] = todo_update.description
            if todo_update.completed is not None:
                todo["completed"] = todo_update.completed
            
            print(f"[UPDATE] TODO 수정: ID={todo_id}")
            return todo
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {todo_id}인 TODO를 찾을 수 없습니다"
    )


@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """TODO 삭제"""
    for index, todo in enumerate(todos_db):
        if todo["id"] == todo_id:
            todos_db.pop(index)
            print(f"[DELETE] TODO 삭제: ID={todo_id}")
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"ID {todo_id}인 TODO를 찾을 수 없습니다"
    )


@app.get("/api/health")
def health_check():
    """서버 상태 및 통계"""
    total = len(todos_db)
    completed = len([t for t in todos_db if t["completed"]])
    pending = total - completed
    
    return {
        "status": "healthy",
        "total": total,
        "completed": completed,
        "pending": pending
    }


# ============================================
# 실행 방법:
# uvicorn main:app --reload
# 
# 브라우저에서:
# http://localhost:8000  ← HTML UI
# http://localhost:8000/docs  ← API 문서
# ============================================