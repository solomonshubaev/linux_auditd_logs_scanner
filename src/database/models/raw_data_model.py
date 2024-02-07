from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class RawDataModel(Base):
    __tablename__ = 'raw_data'

    id = Column(String(36), primary_key=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
