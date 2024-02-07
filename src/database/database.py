import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(os.getenv('DATABASE_URL'))
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
        return cls._instance


def session_decorator(func):
    def wrapper(*args, **kwargs):
        session = DatabaseSingleton().Session()
        try:
            result = func(session, *args, **kwargs)
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
