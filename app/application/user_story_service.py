from app.infrastructure.user_story_manager import UserStoryManager
from app.domain.user_story import UserStory

class UserStoryService:
    def __init__(self):
        self.manager = UserStoryManager()

    def create_user_story(self, user_story_data):
        user_story = UserStory(**user_story_data)
        return self.manager.add_user_story(user_story)

    def get_user_story(self, user_story_id):
        return self.manager.get_user_story(user_story_id)

    def update_user_story(self, user_story_id, update_data):
        # Fetch, update fields, and persist
        user_story = self.manager.get_user_story(user_story_id)
        if not user_story:
            return None
        for key, value in update_data.items():
            setattr(user_story, key, value)
        self.manager.update_user_story(user_story)
        return user_story

    def delete_user_story(self, user_story_id):
        result = self.manager.delete_user_story(user_story_id)
        return result is not None

    def list_user_stories(self):
        return self.manager.list_user_stories() 