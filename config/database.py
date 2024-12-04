from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = environ.get("DB_USER", "root")
DB_PW = environ.get("DB_PW", "")
DB_HOST = environ.get("DB_HOST", "127.0.0.1")
DB_PORT = environ.get("DB_PORT", 3306)
DB_NAME = environ.get("DB_NAME", "wanted_lab")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
TEST_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/test_db?charset=utf8"
)

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_test_engine():
    return create_engine(TEST_DATABASE_URL)


def get_test_session():
    engine = get_test_engine()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
