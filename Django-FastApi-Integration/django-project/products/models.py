from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''사용자 모델 확장'''
    ROLE_CHOICES = [
        ('user','일반 사용자'),
        ('manager','매니저'),
        ('admin','관리자'),
    ]
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='user',verbose_name='역활')
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
    