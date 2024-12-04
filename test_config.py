import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from company.models import Base
from config.database import get_test_engine
from csv_data_uploader import save_csv_to_db


@pytest.fixture(scope="module")
def test_db():
    engine = get_test_engine()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        connection = engine.connect()
        transaction = connection.begin()
        db.connection = connection
        db.transaction = transaction

        save_csv_to_db(file_path="./company_tag_sample.csv", db=db)

        yield db

    finally:
        db.transaction.rollback()
        db.connection.close()
        db.close()

        # Drop all tables after the tests
        Base.metadata.drop_all(bind=engine)
