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
def create_item_simple(item:Item):
    '''
    상품추가 api
    ex)
    {
        'name' : '노트북'
        'price' : 1000000
    }
    '''
    return {
        'message':f'{item.name}이(가) 추가되었습니다.',
        'item':item
    }
    
# 검증 규칙이 있는 모델
class Product(BaseModel):
    '''검증 규칙이 포함된 상품 모델'''
    name:str = Field(...,min_length=1 , max_length=100 , description='상품명')
    price:int = Field(...,gt=0 , description='가격이 0원 보다 커야함')
    description:Optional[str] = Field(None , max_length=500 , description='상품설명')
    is_stock:bool = Field(default=True , description='재고여부')
    class Config:
        json_schema_extra = {
            'example':{
                'name' : '아이폰',
                'price' : 2000000,
                'description' : '인체공학적인 디자인',
                'is_stock' :  True
            }
        }

@app.post('/products')
def create_product(product: Product):
    '''검증이 포함된 상품 추가 api
    검증 규칙 : 
    -name : 
    '''
    return {
        'message' : f'{product.name} 이(가) 추가되었습니다.',
        'product' : product
    }