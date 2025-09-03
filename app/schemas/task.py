import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

StatusType = Literal["pending", "completed"]

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    status: StatusType = "pending"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[StatusType] = None

class TaskOut(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime  
    
    model_config = ConfigDict(from_attributes=True)