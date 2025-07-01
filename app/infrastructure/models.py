# app/infrastructure/models.py
from sqlalchemy import Column, String, Float, Enum as SAEnum, DateTime, func, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.domain.task import Priority, Status, Category
from app.domain.user_story import UserStoryPriority

Base = declarative_base()

class UserStoryORM(Base):
    __tablename__ = "user_stories"

    id = Column(String(36), primary_key=True)
    project = Column(String(100), nullable=False)
    rol = Column(String(100), nullable=False)
    goal = Column(String(300), nullable=False)
    reason = Column(String(300), nullable=False)
    description = Column(String(300), nullable=False)
    priority = Column(SAEnum(UserStoryPriority), nullable=False)
    story_points = Column(Integer, nullable=False)
    effort_hours = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationship with tasks
    tasks = relationship("TaskORM", back_populates="user_story")

class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    priority = Column(SAEnum(Priority), nullable=False)
    effort_hours = Column(Float, nullable=False)
    status = Column(SAEnum(Status), nullable=False)
    assigned_to = Column(String(255), nullable=False)
    category = Column(SAEnum(Category), nullable=False)
    user_story_id = Column(String(36), ForeignKey('user_stories.id'), nullable=True)
    risk_analysis = Column(String(1024), nullable=True)
    risk_mitigation = Column(String(1024), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationship with user story
    user_story = relationship("UserStoryORM", back_populates="tasks")