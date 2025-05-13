from sqlalchemy import Column, Enum, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Item(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    frequency = Column(Enum("daily", "weekly", "monthly", "yearly", "other"), default="monthly")
    frequency_value = Column(Integer, nullable=True) # may change how I do this
    last_done = Column(String, default="2023-01-01")
    next_to_do = Column(String, default="2023-01-01")
    
    # TODO: how to set up created_at and updated_at automatically
    
    owner = relationship("User", back_populates="items")
