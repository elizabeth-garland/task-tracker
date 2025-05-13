from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base_class import TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    frequency = Column(
        Enum("daily", "weekly", "monthly", "yearly", "other", name="frequency_type"), default="monthly"
    )
    frequency_value = Column(Integer, nullable=True)  # may change how I do this
    last_done = Column(DateTime, nullable=True)
    next_to_do = Column(String, nullable=True)

    # TODO: how to set up created_at and updated_at automatically

    owner = relationship("User", back_populates="tasks")  # backward relationship
