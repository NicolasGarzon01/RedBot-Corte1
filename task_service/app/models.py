from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, func
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)   # reply | schedule | moderate
    config_json = Column(JSON, nullable=False)  # reglas en JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending", nullable=False) # Estados: pending, running, completed, failed
