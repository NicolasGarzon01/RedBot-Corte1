from pydantic import BaseModel
from typing import Any, Dict

class TaskBase(BaseModel):
    type: str
    config_json: Dict[str, Any]

class TaskCreate(TaskBase):
    account_id: int

class Task(TaskBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True
