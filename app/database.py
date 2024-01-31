from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

'''For connection to DB without Alchemy'''
import time
import psycopg2
from psycopg2.extras import RealDictCursor


SQLALCHEMY_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True :
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = 'FastApi',user = 'postgres',
#                                 password = 'admin', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Sucessful connection")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error : ", error)
#         time.sleep(3)