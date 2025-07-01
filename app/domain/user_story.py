from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class UserStoryPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKING = "blocking"

class UserStory(BaseModel):
    id: str
    project: str
    rol: str
    goal: str
    reason: str
    description: str
    priority: UserStoryPriority
    story_points: int
    effort_hours: float
    created_at: Optional[datetime] = None

    @field_validator('project')
    @classmethod
    def project_length(cls, v):
        if len(v) > 100:
            raise ValueError('Project cannot be longer than 100 characters')
        return v

    @field_validator('rol')
    @classmethod
    def rol_length(cls, v):
        if len(v) > 100:
            raise ValueError('Rol cannot be longer than 100 characters')
        return v

    @field_validator('goal')
    @classmethod
    def goal_length(cls, v):
        if len(v) > 300:
            raise ValueError('Goal cannot be longer than 300 characters')
        return v

    @field_validator('reason')
    @classmethod
    def reason_length(cls, v):
        if len(v) > 300:
            raise ValueError('Reason cannot be longer than 300 characters')
        return v

    @field_validator('description')
    @classmethod
    def description_length(cls, v):
        if len(v) > 300:
            raise ValueError('Description cannot be longer than 300 characters')
        return v

    @field_validator('story_points')
    @classmethod
    def story_points_range(cls, v):
        if not 1 <= v <= 8:
            raise ValueError('Story points must be between 1 and 8')
        return v

    @field_validator('effort_hours')
    @classmethod
    def effort_hours_decimal(cls, v):
        # Round to one decimal place
        return round(v, 1)

    class Config:
        use_enum_values = True 