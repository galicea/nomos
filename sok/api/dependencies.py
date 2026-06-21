from db.session import SessionLocal, get_db
from services.knservice import DataManager


def get_data_manager():
    db = SessionLocal()
    try:
        yield DataManager(db)
    finally:
        db.close()
