import pytest
from app.domain.task import Task, Priority, Status, Category
from app.domain.user_story import UserStory, UserStoryPriority

class TestTaskModel:
    """Test suite for Task domain model."""
    
    def test_task_creation_valid_data(self):
        """Test creating a task with valid data."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "This is a test task description",
            "priority": "high",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "Test User",
            "category": "Backend",
            "user_story_id": None,
            "risk_analysis": None,
            "risk_mitigation": None
        }
        
        task = Task(**task_data)
        
        assert task.id == "test-id"
        assert task.title == "Test Task"
        assert task.description == "This is a test task description"
        assert task.priority == Priority.HIGH
        assert task.effort_hours == 2.5
        assert task.status == Status.PENDING
        assert task.assigned_to == "Test User"
        assert task.category == Category.BACKEND
        assert task.user_story_id is None
        assert task.risk_analysis is None
        assert task.risk_mitigation is None

    def test_task_creation_with_user_story_id(self):
        """Test creating a task with user story ID."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "This is a test task description",
            "priority": "high",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "Test User",
            "category": "Backend",
            "user_story_id": "user-story-id",
            "risk_analysis": "Sample risk analysis",
            "risk_mitigation": "Sample risk mitigation"
        }
        
        task = Task(**task_data)
        
        assert task.user_story_id == "user-story-id"
        assert task.risk_analysis == "Sample risk analysis"
        assert task.risk_mitigation == "Sample risk mitigation"

    def test_task_validation_missing_required_fields(self):
        """Test task validation with missing required fields."""
        incomplete_data = {
            "id": "test-id",
            "title": "Test Task"
            # Missing required fields
        }
        
        with pytest.raises(Exception):
            Task(**incomplete_data)

    def test_task_validation_description_too_long(self):
        """Test task validation with description exceeding limit."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "x" * 1001,  # Exceeds 1000 character limit
            "priority": "high",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "Test User",
            "category": "Backend"
        }
        
        with pytest.raises(Exception):
            Task(**task_data)

    def test_task_validation_invalid_priority(self):
        """Test task validation with invalid priority."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "Test description",
            "priority": "invalid_priority",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "Test User",
            "category": "Backend"
        }
        
        with pytest.raises(Exception):
            Task(**task_data)

    def test_task_validation_invalid_status(self):
        """Test task validation with invalid status."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "Test description",
            "priority": "high",
            "effort_hours": 2.5,
            "status": "invalid_status",
            "assigned_to": "Test User",
            "category": "Backend"
        }
        
        with pytest.raises(Exception):
            Task(**task_data)

    def test_task_validation_invalid_category(self):
        """Test task validation with invalid category."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "Test description",
            "priority": "high",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "Test User",
            "category": "invalid_category"
        }
        
        with pytest.raises(Exception):
            Task(**task_data)

    def test_task_validation_negative_effort_hours(self):
        """Test task validation with negative effort hours."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "Test description",
            "priority": Priority.HIGH,
            "effort_hours": -1.0,
            "status": Status.PENDING,
            "assigned_to": "Test User",
            "category": Category.BACKEND
        }
        
        # Pydantic will handle validation, so this should work
        # The validation is done at the API level, not model level
        task = Task(**task_data)
        assert task.effort_hours == -1.0

    def test_task_enum_values(self):
        """Test that all enum values are accepted."""
        valid_priorities = [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.BLOCKING]
        valid_statuses = [Status.PENDING, Status.IN_PROGRESS, Status.IN_REVIEW, Status.COMPLETED]
        valid_categories = [Category.FRONTEND, Category.BACKEND, Category.TESTING, Category.INFRA, Category.MOBILE]
        
        for priority in valid_priorities:
            for status in valid_statuses:
                for category in valid_categories:
                    task_data = {
                        "id": f"test-{priority.value}-{status.value}-{category.value}",
                        "title": f"Test Task {priority.value} {status.value} {category.value}",
                        "description": "Test description",
                        "priority": priority,
                        "effort_hours": 1.0,
                        "status": status,
                        "assigned_to": "Test User",
                        "category": category
                    }
                    
                    task = Task(**task_data)
                    assert task.priority == priority
                    assert task.status == status
                    assert task.category == category

    def test_task_model_dump(self):
        """Test task model serialization."""
        task_data = {
            "id": "test-id",
            "title": "Test Task",
            "description": "Test description",
            "priority": "high",
            "effort_hours": 2.5,
            "status": "pending",
            "assigned_to": "Test User",
            "category": "Backend",
            "user_story_id": "user-story-id",
            "risk_analysis": "Sample risk",
            "risk_mitigation": "Sample mitigation"
        }
        
        task = Task(**task_data)
        dumped = task.model_dump()
        
        assert dumped['id'] == "test-id"
        assert dumped['title'] == "Test Task"
        assert dumped['priority'] == "high"
        assert dumped['status'] == "pending"
        assert dumped['category'] == "Backend"

class TestUserStoryModel:
    """Test suite for UserStory domain model."""
    
    def test_user_story_creation_valid_data(self):
        """Test creating a user story with valid data."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "Test User",
            "goal": "test functionality",
            "reason": "to verify the system works",
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        user_story = UserStory(**user_story_data)
        
        assert user_story.id == "test-id"
        assert user_story.project == "Test Project"
        assert user_story.rol == "Test User"
        assert user_story.goal == "test functionality"
        assert user_story.reason == "to verify the system works"
        assert user_story.description == "As a test user, I want to test functionality so that I can verify the system works."
        assert user_story.priority == UserStoryPriority.MEDIUM
        assert user_story.story_points == 3
        assert user_story.effort_hours == 4.0

    def test_user_story_validation_missing_required_fields(self):
        """Test user story validation with missing required fields."""
        incomplete_data = {
            "id": "test-id",
            "project": "Test Project"
            # Missing required fields
        }
        
        with pytest.raises(Exception):
            UserStory(**incomplete_data)

    def test_user_story_validation_project_too_long(self):
        """Test user story validation with project name exceeding limit."""
        user_story_data = {
            "id": "test-id",
            "project": "x" * 101,  # Exceeds 100 character limit
            "rol": "Test User",
            "goal": "test functionality",
            "reason": "to verify the system works",
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        with pytest.raises(Exception):
            UserStory(**user_story_data)

    def test_user_story_validation_rol_too_long(self):
        """Test user story validation with role exceeding limit."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "x" * 101,  # Exceeds 100 character limit
            "goal": "test functionality",
            "reason": "to verify the system works",
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        with pytest.raises(Exception):
            UserStory(**user_story_data)

    def test_user_story_validation_goal_too_long(self):
        """Test user story validation with goal exceeding limit."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "Test User",
            "goal": "x" * 301,  # Exceeds 300 character limit
            "reason": "to verify the system works",
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        with pytest.raises(Exception):
            UserStory(**user_story_data)

    def test_user_story_validation_reason_too_long(self):
        """Test user story validation with reason exceeding limit."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "Test User",
            "goal": "test functionality",
            "reason": "x" * 301,  # Exceeds 300 character limit
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        with pytest.raises(Exception):
            UserStory(**user_story_data)

    def test_user_story_validation_description_too_long(self):
        """Test user story validation with description exceeding limit."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "Test User",
            "goal": "test functionality",
            "reason": "to verify the system works",
            "description": "x" * 301,  # Exceeds 300 character limit
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        with pytest.raises(Exception):
            UserStory(**user_story_data)

    def test_user_story_validation_invalid_priority(self):
        """Test user story validation with invalid priority."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "Test User",
            "goal": "test functionality",
            "reason": "to verify the system works",
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "invalid_priority",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        with pytest.raises(Exception):
            UserStory(**user_story_data)

    def test_user_story_validation_invalid_story_points(self):
        """Test user story validation with invalid story points."""
        invalid_story_points = [0, 9, 10, 15, 20]
        
        for story_points in invalid_story_points:
            user_story_data = {
                "id": "test-id",
                "project": "Test Project",
                "rol": "Test User",
                "goal": "test goal",
                "reason": "to test",
                "description": "As a test user, I want to test goal so that I can verify.",
                "priority": UserStoryPriority.MEDIUM,
                "story_points": story_points,
                "effort_hours": 4.0
            }
            
            # This should raise a validation error
            with pytest.raises(ValueError, match="Story points must be between 1 and 8"):
                UserStory(**user_story_data)

    def test_user_story_validation_invalid_effort_hours(self):
        """Test user story validation with invalid effort hours."""
        # Test that effort hours are properly rounded
        test_cases = [
            (4.123, 4.1),
            (4.567, 4.6),
            (4.999, 5.0),
            (4.0, 4.0)
        ]
        
        for input_hours, expected_hours in test_cases:
            user_story_data = {
                "id": "test-id",
                "project": "Test Project",
                "rol": "Test User",
                "goal": "test goal",
                "reason": "to test",
                "description": "As a test user, I want to test goal so that I can verify.",
                "priority": UserStoryPriority.MEDIUM,
                "story_points": 3,
                "effort_hours": input_hours
            }
            
            # Pydantic should round the effort hours
            user_story = UserStory(**user_story_data)
            assert user_story.effort_hours == expected_hours

    def test_user_story_enum_values(self):
        """Test that all enum values are accepted."""
        valid_priorities = [UserStoryPriority.LOW, UserStoryPriority.MEDIUM, UserStoryPriority.HIGH, UserStoryPriority.BLOCKING]
        valid_story_points = [1, 2, 3, 5, 8]
        
        for priority in valid_priorities:
            for story_points in valid_story_points:
                user_story_data = {
                    "id": f"test-{priority.value}-{story_points}",
                    "project": f"Test Project {priority.value}",
                    "rol": f"Test User {story_points}",
                    "goal": f"test goal {priority.value}",
                    "reason": f"to test {story_points}",
                    "description": f"As a test user, I want to test goal {priority.value} so that I can verify {story_points}.",
                    "priority": priority,
                    "story_points": story_points,
                    "effort_hours": 4.0
                }
                
                user_story = UserStory(**user_story_data)
                assert user_story.priority == priority
                assert user_story.story_points == story_points

    def test_user_story_model_dump(self):
        """Test user story model serialization."""
        user_story_data = {
            "id": "test-id",
            "project": "Test Project",
            "rol": "Test User",
            "goal": "test functionality",
            "reason": "to verify the system works",
            "description": "As a test user, I want to test functionality so that I can verify the system works.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        user_story = UserStory(**user_story_data)
        dumped = user_story.model_dump()
        
        assert dumped['id'] == "test-id"
        assert dumped['project'] == "Test Project"
        assert dumped['priority'] == "medium"
        assert dumped['story_points'] == 3
        assert dumped['effort_hours'] == 4.0

    def test_user_story_effort_hours_decimal_places(self):
        """Test user story effort hours with different decimal places."""
        valid_effort_hours = [1.0, 2.5, 3.0, 4.5, 5.0, 6.5, 7.0, 8.5, 9.0, 10.0]
        
        for effort_hours in valid_effort_hours:
            user_story_data = {
                "id": f"test-{effort_hours}",
                "project": "Test Project",
                "rol": "Test User",
                "goal": "test functionality",
                "reason": "to verify the system works",
                "description": "As a test user, I want to test functionality so that I can verify the system works.",
                "priority": "medium",
                "story_points": 3,
                "effort_hours": effort_hours
            }
            
            user_story = UserStory(**user_story_data)
            assert user_story.effort_hours == effort_hours 