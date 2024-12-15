try:
    from pydantic import BaseModel
    from typing import Optional
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)


class UserBase(BaseModel):
    login: str
    passw: str
    employee_id: Optional[int]


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    login: Optional[str] = None
    passw: Optional[str] = None
    employee_id: Optional[int] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True