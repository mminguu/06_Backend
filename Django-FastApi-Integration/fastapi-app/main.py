from fastapi import FastAPI,Depends,HTTPException,status

app = FastAPI(
    title="Product API",
    description='제품관리'
)

# 라우터 설정
@app.get('/')
def root():
    return {"message":"Welcome to the Product API"}