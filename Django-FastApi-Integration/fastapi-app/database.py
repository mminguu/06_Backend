# DB 연결 정보를 정의하고
# SQLAlchemy Engine 생성
# 세션(서버) 생성 안전한 종료 관리하는 곳 - 각종 로그인 정보 , 캐시라고 보면 됨.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , Session
from contextlib import contextmanager # with문으로 db 세션을 쓰기 위한 임포트

# 데이터 베이스 url 설계
SQLALCHEMY_DATABASE_URL = 'sqlite:///.products.db'


#sqlite 는 기본적으로 단일 스레드 제한
# sqlite + fastapi 조합 시 다중 스레드 문제가 발생하는데 이를 해결하기 위한 옵션 추가한거임.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread':False} # SQLite 특정 옵션
)

# 트랜젝션을 제어 한다. 예외 발생 시 롤백 관리를 하겠다.
SesssionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)


# yield db 가 endpoint 함수에 전달하면 endpoint 함수 종료 시 finally 불록 실행
def get_db():
    db = SesssionLocal()
    try:
        yield db # 빌려주고 회수의 개념
    finally:
        db.close()