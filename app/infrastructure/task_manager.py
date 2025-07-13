# app/infrastructure/task_manager.py
from app.infrastructure.db import SessionLocal
from app.infrastructure.models import TaskORM
from app.domain.task import Task
from typing import List

class TaskManager:
    def add_task(self, task: Task):
        with SessionLocal() as db:
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
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            task_dict = db_task.__dict__.copy()
            task_dict.pop('created_at', None)
            task_dict.pop('_sa_instance_state', None)
            return Task.model_validate(task_dict)

    def update_task(self, task: Task):
        with SessionLocal() as db:
            db_task = db.query(TaskORM).filter(TaskORM.id == task.id).first()
            if db_task:
                setattr(db_task, "title", task.title)
                setattr(db_task, "description", task.description)
                setattr(db_task, "priority", task.priority)
                setattr(db_task, "effort_hours", task.effort_hours)
                setattr(db_task, "status", task.status)
                setattr(db_task, "assigned_to", task.assigned_to)
                setattr(db_task, "category", task.category)
                setattr(db_task, "user_story_id", task.user_story_id)
                setattr(db_task, "risk_analysis", task.risk_analysis)
                setattr(db_task, "risk_mitigation", task.risk_mitigation)
                db.commit()
                db.refresh(db_task)
                task_dict = db_task.__dict__.copy()
                task_dict.pop('created_at', None)
                task_dict.pop('_sa_instance_state', None)
                return Task.model_validate(task_dict)
            return None

    def delete_task(self, task_id: str):
        with SessionLocal() as db:
            db_task = db.query(TaskORM).filter(TaskORM.id == task_id).first()
            if db_task:
                db.delete(db_task)
                db.commit()
                return True
            return None

    def list_tasks(self):
        with SessionLocal() as db:
            db_tasks = db.query(TaskORM).all()
            result = []
            for db_task in db_tasks:
                task_dict = db_task.__dict__.copy()
                task_dict.pop('created_at', None)
                task_dict.pop('_sa_instance_state', None)
                result.append(Task.model_validate(task_dict))
            return result

    def get_task(self, task_id: str) -> Task | None:
        with SessionLocal() as db:
            db_task = db.query(TaskORM).filter(TaskORM.id == task_id).first()
            if db_task:
                task_dict = db_task.__dict__.copy()
                task_dict.pop('created_at', None)
                task_dict.pop('_sa_instance_state', None)
                return Task.model_validate(task_dict)
            return None

    def get_tasks_by_user_story(self, user_story_id: str) -> List[Task]:
        with SessionLocal() as db:
            db_tasks = db.query(TaskORM).filter(TaskORM.user_story_id == user_story_id).all()
            result = []
            for db_task in db_tasks:
                task_dict = db_task.__dict__.copy()
                # Remove SQLAlchemy internal attributes
                task_dict.pop('_sa_instance_state', None)
                result.append(Task.model_validate(task_dict))
            return result