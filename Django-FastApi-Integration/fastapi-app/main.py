from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware # Django(8000) 와 FastAPI(8001) 연동 시 필요 CORS 문제 해결 / 다른 도메인의 접근 허용하게 해줌
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine , get_db


models.Base.metadata.create_all(bind=engine) # data에 접근하려면 이게 필요함

app = FastAPI(
    title="Product API",
    description='제품관리',
    version='1.0.0'
)


# CROS 설정 - Django 와 FastAPI 연동 시 필요
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","http:///127.0.0.1:8000"], # 모든 출처 허용
    allow_credentials=True, # 쿠키 , 인증 정보 허용
    allow_methods=[""], # 모든 메서드 허용 GET , POST , PUT , DELETE 
    allow_headers=[""], # 모든 헤더 허용 Authorization , content-Type
)


# 라우터 설정
@app.get('/')
def root():
    return {
        "message" : "Product API",
        "docs" : "/docs",
        "endpoints" : {
            'products' : '/api/products',
            'product' : '/api/products/{id}'
        }
    }
# 제품 목록 조회
# response_Model 은 반환 데이터를 자동 검증하고 orm 모델을 json으로 변환해줌.
# response_Model 은 Swagger 문서 자동 생성해줌

# -- 전체 제품을 조회 -- 
@app.get("/api/products",response_model=List[schemas.Product])
def get_products(
    skip:int=0, # 0개일경우 skip하겠다.
    limit:int=100, # 한번에 100개씩 가져오겠다.
    db:Session=Depends(get_db) # 항상 넣어줘야하는 구문 / 함수 실행이 끝나면 db 세션을 자동 종료하겠다는것. (중요) 이거 안 쓰면 일일히 다 구현해줘야함
):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

# -- 제품을 상세 조회 --
@app.get("/api/products/{product_id}" , response_model=schemas.Product)
def get_product(product_id:int , db:Session=Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first() # 여러개의 값이 나왔을때 제일 첫번째꺼 조회하여 추출하겠다 (.first() 쓰는 이유는 pk 가 중복 될 가능성이 있기때문에)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {product_id}"
        )
    return product


# -- 제품을 생성 하는 --
# 성공하면 HTTP_201_CREATED  상태 코드
# 제품 생성하는 것 = POST 
# 제품 목록 보는 것 = GET
@app.post("/api/products",response_model=schemas.Product , status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate , db:Session=Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)# 생성한걸 db에 저장
    db.commit() # 실제 db에 insert 하는 것.
    return db_product

# -- 제품 수정 --
@app.put("/api/products/{product_id}" , response_model=schemas.Product)
def update_product(product_id:int , product: schemas.ProductUpdate , db:Session=Depends(get_db)):
    product_put = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product_put is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {product_id}"
        )
    update_product = product.model_dump(exclude_unset=True) # 전달 된 필드만 업데이트 되고 , 이걸 안 쓰면 수정된 거 외에는 모두 None으로 나옴.
    for key,value in update_product.items():
        setattr(product_put,key,value) # 변경 감지 기능이 있어서 업데이트 된 필드만 실제 db에 반영하겠다는 뜻.
    db.commit()
    db.refresh(product_put)
    return product_put

@app.delete("/api/products/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {product_id}"
        )
    db.delete(product)
    db.commit()
    return None