# 데코레이터 @app.get('/hello') --- 라우터 http://localhost:8000/hello --> 서버 내의 해당 함수를 실행
# @app.get('/hello')
# 함수
# 라우터 역할을 하는게 app.get // 요청한 주소를 보고 요청한 값을 보고 누구를 실행할지 결정해주는 역할 
@app.get('/hello')
def say_hello():
    return {'message': 'Hello World'}

# 경로 파라메터 vs 쿼리 파라메터
# http://localhost:8000/hello/강민지  경로파라메터
@app.get('/hello/{name}')
def say_hello(name:str):
    return{'message':f'Hello {name}'}  # 자동으로 json 형태로 변환 (딕셔너리 형태)

# 쿼리 파라메터
@app.get('/greet') # http://localhost:8000/greet?name=강민지;age=20  // 물음표 전까지는?
def greet(name:str , age:int):
    return