2025.12.29  Django - FastAPI ==================



\* Django 👉 웹 서비스 전체 관리

\* FastAPI 👉 빠른 API / AI·모델 서버

\* 왜 연동하나? 현업 구조가 보통 이래 👇

\[ 사용자 브라우저 ]

&nbsp;       ↓

&nbsp;    Django (메인 서버)

&nbsp;       ↓ (API 요청)

&nbsp;    FastAPI (AI / 모델 서버)







FastAPI : 백엔드 api

\- RESTFull API

\- SQLAIchemyORM 데이터베이스 관리

\- Pydantic 데이터 검증

\- 자동 Swqgger UI 문서



Django : 프론트엔드

\- 웹 인터페이스 제공

\- https 로 FastAPI 호출

\- bootstrap 

\- admin 패널



=====================================



설치

pip install httpx 

pip install -r requirements.txt



=====================================



========================================================

========================================================



conda install django -y

django-admin startproject \[프로젝트명] .    --> 메인

django-admin startapp \[어플리케이션명]    --> 메인에 종속된 app(앱)



서버실행

python manage.py runserver



슈퍼유저

python manage.py migrate                 - 필요한 데이터베이스 구조를자동생성

python manage.py createsuperuser



========================================================

========================================================



1\. 9Django 폴더에

django\_project 와 FastAPI\_app 폴더 생성



2\. 

django\_project에서 config . 프로젝트 설치

django-admin startproject config .



3\.

python manage.py migrate                 - 필요한 데이터베이스 구조를자동생성

python manage.py createsuperuser 



4\. FastAPI\_app 폴더에

main.py 생성 및 작성



uvicorn main:app --reload     ===> 8000번 포트로 연결

http://127.0.0.1:8000/docs    ===> 여러가지 확인 가능함



상기 django도 8000 포트를 이용하기 때문에 FastAPI 포트 변경 필요!



from fastapi.middleware.cors import CORSMiddleware  

\# Django 8000 포트와 FastAPI 8001 포트 연동시 필요. CORS 문제 해결

\# CORS

\- 동일 출처 정책(Same-Origin Policy): 보안을 위해 브라우저는 기본적으로 같은 출처(Origin)에서만 리소스 요청과 응답을 허용합니다.

\- CORS의 역할: 이 정책을 우회하여 서로 다른 출처(Cross-Origin) 간의 데이터 통신을 허용하는 규칙을 정의합니다.





5\. FastAPI\_app 폴더에

\- models.py 생성 및 작성

\- schemas.py 생성 및 작성

\- database.py 생성 및 작성



uvicorn main:app --port 8001 --reload    ===> 8001번 포트로 연결



6\. FastAPI\_app 폴더에

add\_sample\_data.py 파일 생성 및 작성 후

터미널에서 python add\_sample\_data.py

실행하면 products.db 생성됨

&nbsp;

7\.  FastAPI\_app 폴더에

main.py 수정



uvicorn main:app --port 8001 --reload    ===> 8001번 포트로 연결/실행해보기

http://127.0.0.1:8001/docs



==================================================================> FastAPI  백엔드 완성



8\. cd django\_project에서

django-admin startapp products





9\. config/setting.py 수정

INSTALLED\_APPS = \[ 

&nbsp;   'products'



TEMPLATES = \[

&nbsp;       'DIRS': \[BASE\_DIR / 'templates'],

LANGUAGE\_CODE = 'ko-kr'

TIME\_ZONE = 'Asia/Seoul'

STATICFILES\_DIRS = \[BASE\_DIR / 'static']

\# FastAPI URL

FASTAPI\_BASE\_DIR = 'http://127.0.0.1:8001'





10\.

django\_project에 

templates 폴더 만들고 - base.html 만들기

django\_project/templates/products 폴더 만들고 - product\_form.html, product\_list.html 만들기





11\.

django\_project에

static 폴더 만들기

python manage.py migrate

python manage.py runserver





12\.

config/urls.py 

path 추가





13\.

products/urls.py 생성 및 작성



14\. 

products/views.py 작성



====================================================================>



15\. 터미널 2개에 

우선적으로 FastAPI 실행시킨 후에   uvicorn main:app --port 8001 --reload

다른 터미널에서 django 실행시키기 python manage.py runserver



===============================================================



16\.

django\_project/templates 폴더에서

base.html 작성 후 product\_list.html 작성





17\. 제품추가힉

django\_project/products/urls.py  에 path 추가

&nbsp;path('prodcuts/create', views.product\_create, name='product\_create')



18\. 

views.py 에 product\_create 코드 추가

foms.py 생성 및 작성하여 상기 product\_create에 import하기







