from app.infrastructure.db import SessionLocal
from app.infrastructure.models import UserStoryORM
from app.domain.user_story import UserStory, UserStoryPriority

class UserStoryManager:
    def add_user_story(self, user_story: UserStory):
        with SessionLocal() as db:
            db_user_story = UserStoryORM(
                id=user_story.id,
                project=str(user_story.project),
                rol=str(user_story.rol),
                goal=str(user_story.goal),
                reason=str(user_story.reason),
                description=str(user_story.description),
                priority=UserStoryPriority(user_story.priority),
                story_points=int(user_story.story_points),
                effort_hours=float(user_story.effort_hours)
            )
            db.add(db_user_story)
            db.commit()
            db.refresh(db_user_story)
            return UserStory.model_validate(db_user_story.__dict__)

    def update_user_story(self, user_story: UserStory):
        with SessionLocal() as db:
            db_user_story = db.query(UserStoryORM).filter(UserStoryORM.id == user_story.id).first()
            if db_user_story:
                setattr(db_user_story, "project", str(user_story.project))
                setattr(db_user_story, "rol", str(user_story.rol))
                setattr(db_user_story, "goal", str(user_story.goal))
                setattr(db_user_story, "reason", str(user_story.reason))
                setattr(db_user_story, "description", str(user_story.description))
                setattr(db_user_story, "priority", UserStoryPriority(user_story.priority))
                setattr(db_user_story, "story_points", int(user_story.story_points))
                setattr(db_user_story, "effort_hours", float(user_story.effort_hours))
                db.commit()
                db.refresh(db_user_story)
                return UserStory.model_validate(db_user_story.__dict__)
            return None

    def delete_user_story(self, user_story_id: str):
        with SessionLocal() as db:
            db_user_story = db.query(UserStoryORM).filter(UserStoryORM.id == user_story_id).first()
            if db_user_story:
                db.delete(db_user_story)
                db.commit()
                return True
            return None

    def list_user_stories(self):
        with SessionLocal() as db:
            db_user_stories = db.query(UserStoryORM).all()
            return [UserStory.model_validate(db_user_story.__dict__) for db_user_story in db_user_stories]

    def get_user_story(self, user_story_id: str) -> UserStory | None:
        with SessionLocal() as db:
            db_user_story = db.query(UserStoryORM).filter(UserStoryORM.id == user_story_id).first()
            if db_user_story:
                return UserStory.model_validate(db_user_story.__dict__)
            return None 