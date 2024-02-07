import json
import uuid
from abc import ABC

from database.models.raw_data_model import RawDataModel
from database.database import session_decorator


class RawDataDbMethods(ABC):

    @staticmethod
    @session_decorator
    def insert_raw_date(session, raw_log: dict) -> None:
        raw_data = RawDataModel(id=str(uuid.uuid4()), data=raw_log)
        session.add(raw_data)
        session.commit()
