# app/db/base_class.py

from sqlalchemy import Column, DateTime
from datetime import datetime


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
