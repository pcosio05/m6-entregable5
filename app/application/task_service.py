# app/application/task_service.py
from app.infrastructure.task_manager import TaskManager
from app.domain.task import Task

class TaskService:
    def __init__(self):
        self.manager = TaskManager()

    def create_task(self, task_data):
        task = Task(**task_data)
        return self.manager.add_task(task)

    def get_task(self, task_id):
        return self.manager.get_task(task_id)

    def update_task(self, task_id, update_data):
        # Fetch, update fields, and persist
        task = self.manager.get_task(task_id)
        if not task:
            return None
        for key, value in update_data.items():
            setattr(task, key, value)
        self.manager.update_task(task)
        return task

    def delete_task(self, task_id):
        return self.manager.delete_task(task_id)

    def list_tasks(self):
        return self.manager.list_tasks()

    def get_tasks_by_user_story(self, user_story_id):
        return self.manager.get_tasks_by_user_story(user_story_id)