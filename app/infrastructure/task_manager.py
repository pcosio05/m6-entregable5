# app/infrastructure/task_manager.py
from app.infrastructure.db import SessionLocal
from app.infrastructure.models import TaskORM
from app.domain.task import Task
from typing import List

class TaskManager:
    def __init__(self):
        self.db = SessionLocal()

    def add_task(self, task: Task):
        db_task = TaskORM(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            effort_hours=task.effort_hours,
            status=task.status,
            assigned_to=task.assigned_to,
            category=task.category,
            user_story_id=task.user_story_id,
            risk_analysis=task.risk_analysis,
            risk_mitigation=task.risk_mitigation
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        task_dict = db_task.__dict__.copy()
        task_dict.pop('created_at', None)
        task_dict.pop('_sa_instance_state', None)
        return Task.model_validate(task_dict)

    def update_task(self, task: Task):
        db_task = self.db.query(TaskORM).filter(TaskORM.id == task.id).first()
        if db_task:
            db_task.title = task.title  # type: ignore
            db_task.description = task.description  # type: ignore
            db_task.priority = task.priority  # type: ignore
            db_task.effort_hours = task.effort_hours  # type: ignore
            db_task.status = task.status  # type: ignore
            db_task.assigned_to = task.assigned_to  # type: ignore
            db_task.category = task.category  # type: ignore
            db_task.user_story_id = task.user_story_id  # type: ignore
            db_task.risk_analysis = task.risk_analysis  # type: ignore
            db_task.risk_mitigation = task.risk_mitigation  # type: ignore
            self.db.commit()
            self.db.refresh(db_task)
            
            task_dict = db_task.__dict__.copy()
            task_dict.pop('created_at', None)
            task_dict.pop('_sa_instance_state', None)
            return Task.model_validate(task_dict)
        return None

    def delete_task(self, task_id: str):
        db_task = self.db.query(TaskORM).filter(TaskORM.id == task_id).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            return True
        return None

    def list_tasks(self):
        db_tasks = self.db.query(TaskORM).all()
        result = []
        for db_task in db_tasks:
            task_dict = db_task.__dict__.copy()
            task_dict.pop('created_at', None)
            task_dict.pop('_sa_instance_state', None)
            result.append(Task.model_validate(task_dict))
        return result

    def get_task(self, task_id: str) -> Task | None:
        db_task = self.db.query(TaskORM).filter(TaskORM.id == task_id).first()
        if db_task:
            task_dict = db_task.__dict__.copy()
            task_dict.pop('created_at', None)
            task_dict.pop('_sa_instance_state', None)
            return Task.model_validate(task_dict)
        return None

    def get_tasks_by_user_story(self, user_story_id: str) -> List[Task]:
        db_tasks = self.db.query(TaskORM).filter(TaskORM.user_story_id == user_story_id).all()
        result = []
        for db_task in db_tasks:
            task_dict = db_task.__dict__.copy()
            # Remove SQLAlchemy internal attributes
            task_dict.pop('_sa_instance_state', None)
            result.append(Task.model_validate(task_dict))
        return result