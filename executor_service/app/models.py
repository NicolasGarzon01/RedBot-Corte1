from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from .database import Base

class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    account_id = Column(String, nullable=False)
    task_id = Column(Integer, nullable=True)
    task_type = Column(String(50), nullable=False)     # reply | schedule | moderate
    status = Column(String(20), nullable=False)        # success | error
    detail = Column(JSON, nullable=True)               # payload/result de la ejecución
    created_at = Column(DateTime(timezone=True), server_default=func.now())
