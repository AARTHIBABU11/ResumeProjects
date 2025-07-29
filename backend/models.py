from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel

# SQLAlchemy model
class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    due_date = Column(String)
    description = Column(String)

# Pydantic model for input
class DeadlineCreate(BaseModel):
    title: str
    due_date: str
    description: str

# Pydantic model for output
class DeadlineResponse(DeadlineCreate):
    id: int

    class Config:
        orm_mode = True
