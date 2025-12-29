from pydantic import BaseModel # 모든 스키마의 기본 클래스
from typing import Optional # 선택필드
from datetime import datetime

# 공통필드
class ProductBase(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    stock : int

# 생성용 스키마
# 관리자 전용으로 만들꺼임. 클라이언트가 입력 불가함.
class ProductCrate(ProductBase): # 제품을 생성하는거니까 생성시에만 필요한거임.
    pass # 현재 상태 동일

# 업데이트
# 수정용 스키마 - 전달된 필드만 업데이트하는것임. 내부적으로 PATCH 나 PUT 을 지원
# product.model_dump(exclude_unset=True) 이런 형태로 전달이 됨
class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    price : Optional[float] = None
    stock : Optional[int] = None
    
# 응답 스키마가 필요하여 만들꺼임
class Product(ProductBase):
    id:int
    created_at:datetime
    updated_at:datetime
    class Config:   # 내장 클래스    
        from_atributes = True # ORM 모델을 Pydantic 모델로 변환
        