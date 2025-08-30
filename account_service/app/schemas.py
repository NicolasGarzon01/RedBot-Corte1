from pydantic import BaseModel
from datetime import datetime


class AccountBase(BaseModel):
    user_id: int
    platform: str
    handle: str
    token: str

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
