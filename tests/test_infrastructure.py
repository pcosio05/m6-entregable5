import pytest
from app.infrastructure.task_manager import TaskManager
from app.infrastructure.user_story_manager import UserStoryManager
from app.domain.task import Task, Priority, Status, Category
from app.domain.user_story import UserStory, UserStoryPriority

class TestTaskManager:
    """Test suite for TaskManager."""
    
    def test_add_task_success(self, sample_task):
        """Test successful task addition."""
        manager = TaskManager()
        
        result = manager.add_task(sample_task)
        
        assert result is not None
        assert result.id == sample_task.id
        assert result.title == sample_task.title
        assert result.description == sample_task.description
        assert result.priority == sample_task.priority
        assert result.effort_hours == sample_task.effort_hours
        assert result.status == sample_task.status
        assert result.assigned_to == sample_task.assigned_to
        assert result.category == sample_task.category

    def test_get_task_success(self, sample_task):
        """Test successful task retrieval."""
        manager = TaskManager()
        
        # Add the task first
        added_task = manager.add_task(sample_task)
        
        # Get the task
        result = manager.get_task(sample_task.id)
        
        assert result is not None
        assert result.id == sample_task.id
        assert result.title == sample_task.title

    def test_get_task_not_found(self):
        """Test task retrieval when task doesn't exist."""
        manager = TaskManager()
        
        result = manager.get_task("nonexistent-id")
        
        assert result is None

    def test_list_tasks_empty(self):
        """Test listing tasks when none exist."""
        manager = TaskManager()
        
        result = manager.list_tasks()
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_list_tasks_with_data(self, sample_task):
        """Test listing tasks when tasks exist."""
        manager = TaskManager()
        
        # Add a task
        manager.add_task(sample_task)
        
        # List all tasks
        result = manager.list_tasks()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == sample_task.id

    def test_update_task_success(self, sample_task):
        """Test successful task update."""
        manager = TaskManager()
        
        # Add the task first
        manager.add_task(sample_task)
        
        # Update the task
        updated_task = Task(
            id=sample_task.id,
            title="Updated Title",
            description="Updated description",
            priority=Priority.MEDIUM,
            effort_hours=3.0,
            status=Status.IN_PROGRESS,
            assigned_to="Updated User",
            category=Category.FRONTEND,
            user_story_id=None,  # Don't reference non-existent user story
            risk_analysis="Updated risk analysis",
            risk_mitigation="Updated risk mitigation"
        )
        
        result = manager.update_task(updated_task)
        
        assert result is not None
        assert result.title == "Updated Title"
        assert result.description == "Updated description"
        assert result.priority == Priority.MEDIUM
        assert result.effort_hours == 3.0
        assert result.status == Status.IN_PROGRESS
        assert result.assigned_to == "Updated User"
        assert result.category == Category.FRONTEND
        assert result.user_story_id is None
        assert result.risk_analysis == "Updated risk analysis"
        assert result.risk_mitigation == "Updated risk mitigation"

    def test_update_task_not_found(self, sample_task):
        """Test task update when task doesn't exist."""
        manager = TaskManager()
        
        result = manager.update_task(sample_task)
        
        assert result is None

    def test_delete_task_success(self, sample_task):
        """Test successful task deletion."""
        manager = TaskManager()
        
        # Add the task first
        manager.add_task(sample_task)
        
        # Delete the task
        result = manager.delete_task(sample_task.id)
        
        assert result is True
        
        # Verify task is deleted
        get_result = manager.get_task(sample_task.id)
        assert get_result is None

    def test_delete_task_not_found(self):
        """Test task deletion when task doesn't exist."""
        manager = TaskManager()
        
        result = manager.delete_task("nonexistent-id")
        
        assert result is None

    def test_get_tasks_by_user_story(self, sample_task):
        """Test getting tasks by user story ID."""
        manager = TaskManager()
        user_story_manager = UserStoryManager()
        
        # First create a user story
        user_story = UserStory(
            id="user-story-1",
            project="Test Project",
            rol="Test User",
            goal="test goal",
            reason="to test",
            description="As a test user, I want to test goal so that I can verify.",
            priority=UserStoryPriority.MEDIUM,
            story_points=3,
            effort_hours=4.0
        )
        user_story_manager.add_user_story(user_story)
        
        # Add a task with user story ID
        task_with_user_story = Task(
            id="task-1",
            title="Task 1",
            description="Task 1 description",
            priority=Priority.HIGH,
            effort_hours=2.0,
            status=Status.PENDING,
            assigned_to="Developer 1",
            category=Category.BACKEND,
            user_story_id="user-story-1"
        )
        
        task_without_user_story = Task(
            id="task-2",
            title="Task 2",
            description="Task 2 description",
            priority=Priority.MEDIUM,
            effort_hours=3.0,
            status=Status.PENDING,
            assigned_to="Developer 2",
            category=Category.FRONTEND,
            user_story_id=None
        )
        
        manager.add_task(task_with_user_story)
        manager.add_task(task_without_user_story)
        
        # Get tasks for user story
        result = manager.get_tasks_by_user_story("user-story-1")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == "task-1"
        assert result[0].user_story_id == "user-story-1"

    def test_get_tasks_by_user_story_empty(self):
        """Test getting tasks by user story ID when none exist."""
        manager = TaskManager()
        
        result = manager.get_tasks_by_user_story("nonexistent-user-story")
        
        assert isinstance(result, list)
        assert len(result) == 0

class TestUserStoryManager:
    """Test suite for UserStoryManager."""
    
    def test_add_user_story_success(self, sample_user_story):
        """Test successful user story addition."""
        manager = UserStoryManager()
        
        result = manager.add_user_story(sample_user_story)
        
        assert result is not None
        assert result.id == sample_user_story.id
        assert result.project == sample_user_story.project
        assert result.rol == sample_user_story.rol
        assert result.goal == sample_user_story.goal
        assert result.reason == sample_user_story.reason
        assert result.description == sample_user_story.description
        assert result.priority == sample_user_story.priority
        assert result.story_points == sample_user_story.story_points
        assert result.effort_hours == sample_user_story.effort_hours

    def test_get_user_story_success(self, sample_user_story):
        """Test successful user story retrieval."""
        manager = UserStoryManager()
        
        # Add the user story first
        manager.add_user_story(sample_user_story)
        
        # Get the user story
        result = manager.get_user_story(sample_user_story.id)
        
        assert result is not None
        assert result.id == sample_user_story.id
        assert result.project == sample_user_story.project

    def test_get_user_story_not_found(self):
        """Test user story retrieval when user story doesn't exist."""
        manager = UserStoryManager()
        
        result = manager.get_user_story("nonexistent-id")
        
        assert result is None

    def test_list_user_stories_empty(self):
        """Test listing user stories when none exist."""
        manager = UserStoryManager()
        
        result = manager.list_user_stories()
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_list_user_stories_with_data(self, sample_user_story):
        """Test listing user stories when user stories exist."""
        manager = UserStoryManager()
        
        # Add a user story
        manager.add_user_story(sample_user_story)
        
        # List all user stories
        result = manager.list_user_stories()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == sample_user_story.id

    def test_update_user_story_success(self, sample_user_story):
        """Test successful user story update."""
        manager = UserStoryManager()
        
        # Add the user story first
        manager.add_user_story(sample_user_story)
        
        # Update the user story
        updated_user_story = UserStory(
            id=sample_user_story.id,
            project="Updated Project",
            rol="Updated User",
            goal="updated goal",
            reason="to test updates",
            description="As an updated user, I want to test updates so that I can verify the system works.",
            priority=UserStoryPriority.HIGH,
            story_points=5,
            effort_hours=6.0
        )
        
        result = manager.update_user_story(updated_user_story)
        
        assert result is not None
        assert result.project == "Updated Project"
        assert result.rol == "Updated User"
        assert result.goal == "updated goal"
        assert result.reason == "to test updates"
        assert result.priority == UserStoryPriority.HIGH
        assert result.story_points == 5
        assert result.effort_hours == 6.0

    def test_update_user_story_not_found(self, sample_user_story):
        """Test user story update when user story doesn't exist."""
        manager = UserStoryManager()
        
        result = manager.update_user_story(sample_user_story)
        
        assert result is None

    def test_delete_user_story_success(self, sample_user_story):
        """Test successful user story deletion."""
        manager = UserStoryManager()
        
        # Add the user story first
        manager.add_user_story(sample_user_story)
        
        # Delete the user story
        result = manager.delete_user_story(sample_user_story.id)
        
        assert result is True
        
        # Verify user story is deleted
        get_result = manager.get_user_story(sample_user_story.id)
        assert get_result is None

    def test_delete_user_story_not_found(self):
        """Test user story deletion when user story doesn't exist."""
        manager = UserStoryManager()
        
        result = manager.delete_user_story("nonexistent-id")
        
        assert result is None 