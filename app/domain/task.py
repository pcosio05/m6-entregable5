from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import datetime

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKING = "blocking"

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    IN_REVIEW = "in review"
    COMPLETED = "completed"

class Category(str, Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    TESTING = "Testing"
    INFRA = "Infra"
    MOBILE = "Mobile"

class Task(BaseModel):
    id: str
    title: str
    description: str
    priority: Priority
    effort_hours: float
    status: Status
    assigned_to: str
    category: Category
    user_story_id: Optional[str] = None
    risk_analysis: Optional[str] = None
    risk_mitigation: Optional[str] = None
    created_at: Optional[datetime] = None

    @field_validator('description')
    @classmethod
    def description_length(cls, v):
        if len(v) > 1000:
            raise ValueError('Description cannot be longer than 1000 characters')
        return v

    class Config:
        use_enum_values = True 