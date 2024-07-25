from fastapi import Request, Response, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database_url = 'sqlite:///./todo.db'


engine = create_engine(url=database_url,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)


Base = declarative_base()