from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [    
    # http://127.0.0.1:800/blog/
    path('', views.index),   # http://127.0.0.1:8000/blog/
    path('<int:question_id>/', views.detail,name='detail'),  # alies 별칭 name = 이름  상세페이지
    path('register/answer/<int:question_id>/', views.answer_create, name='answer_create'),
]
