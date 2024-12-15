from pydantic import BaseModel
from typing import Optional


class JobBase(BaseModel):
    name: str
    department_id: int
    code: str


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    code: Optional[str] = None


class Job(JobBase):
    id: int

    class Config:
        from_attributes = True