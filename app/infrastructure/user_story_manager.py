from app.infrastructure.db import SessionLocal
from app.infrastructure.models import UserStoryORM
from app.domain.user_story import UserStory

class UserStoryManager:
    def __init__(self):
        self.db = SessionLocal()

    def add_user_story(self, user_story: UserStory):
        db_user_story = UserStoryORM(
            id=user_story.id,
            project=user_story.project,
            rol=user_story.rol,
            goal=user_story.goal,
            reason=user_story.reason,
            description=user_story.description,
            priority=user_story.priority,
            story_points=user_story.story_points,
            effort_hours=user_story.effort_hours
        )
        self.db.add(db_user_story)
        self.db.commit()
        self.db.refresh(db_user_story)
        return UserStory.model_validate(db_user_story.__dict__)

    def update_user_story(self, user_story: UserStory):
        db_user_story = self.db.query(UserStoryORM).filter(UserStoryORM.id == user_story.id).first()
        if db_user_story:
            db_user_story.project = user_story.project
            db_user_story.rol = user_story.rol
            db_user_story.goal = user_story.goal
            db_user_story.reason = user_story.reason
            db_user_story.description = user_story.description
            db_user_story.priority = user_story.priority
            db_user_story.story_points = user_story.story_points
            db_user_story.effort_hours = user_story.effort_hours
            self.db.commit()
            self.db.refresh(db_user_story)
            return UserStory.model_validate(db_user_story.__dict__)
        return None

    def delete_user_story(self, user_story_id: str):
        db_user_story = self.db.query(UserStoryORM).filter(UserStoryORM.id == user_story_id).first()
        if db_user_story:
            self.db.delete(db_user_story)
            self.db.commit()
            return True
        return None

    def list_user_stories(self):
        db_user_stories = self.db.query(UserStoryORM).all()
        return [UserStory.model_validate(db_user_story.__dict__) for db_user_story in db_user_stories]

    def get_user_story(self, user_story_id: str) -> UserStory | None:
        db_user_story = self.db.query(UserStoryORM).filter(UserStoryORM.id == user_story_id).first()
        if db_user_story:
            return UserStory.model_validate(db_user_story.__dict__)
        return None 