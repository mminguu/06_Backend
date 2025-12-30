from sqlalchemy import Column, Integer, String, Float,DateTime,Text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    '''사용자 모델'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String(50),unique=True, nullable=False,index=True)
    email = Column(String(100),unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default='user')  # user, manager, admin
    is_active = Column(Integer, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now() ,server_default=func.now())

    # 실제 db에 생성되지않고 객체수준에 처리 - 내부적으로 sql orm 이 join 처리
    products = relationship('Product', back_populates='owner')

class Product(Base):
    '''제품 모델'''
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(200), nullable=False,index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now() ,server_default=func.now())

    owner = relationship('User', back_populates='products')