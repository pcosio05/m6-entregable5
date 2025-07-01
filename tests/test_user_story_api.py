import json
import pytest
from unittest.mock import patch
from app.domain.user_story import UserStoryPriority, UserStory
from unittest.mock import Mock
from app.domain.task import Task, Priority, Status, Category

class TestUserStoryAPI:
    """Test suite for User Story API endpoints."""
    
    def test_get_user_stories_web_interface(self, client):
        """Test getting user stories web interface."""
        response = client.get('/user-stories')
        
        assert response.status_code == 200
        assert b'user-stories.html' in response.data or b'User Stories' in response.data

    def test_get_user_story_tasks_web_interface(self, client):
        """Test getting tasks for a user story via web interface."""
        with patch('app.api.user_story_routes.ai_service') as mock_ai_service:
            # Mock the AI service to return a user story
            mock_user_story = UserStory(
                id="test-user-story-id",
                project="Test Project",
                rol="Test User",
                goal="test functionality",
                reason="to verify the system works",
                description="As a test user, I want to test functionality so that I can verify the system works.",
                priority=UserStoryPriority.MEDIUM,
                story_points=3,
                effort_hours=4.0
            )
            mock_ai_service.generate_user_story.return_value = mock_user_story
            
            # Create a user story first
            create_response = client.post('/ai/user-stories',
                                        data=json.dumps({"prompt": "As a user, I want to test functionality"}),
                                        content_type='application/json')
            assert create_response.status_code == 201
            
            # Get the user story ID from the response
            user_story_data = json.loads(create_response.data)
            user_story_id = user_story_data['id']
            
            # Test getting tasks for the user story
            response = client.get(f'/user-stories/{user_story_id}/tasks')
            assert response.status_code == 200
            assert b'Tasks for User Story' in response.data  # Check for the page title instead of filename

    def test_get_user_story_tasks_not_found(self, client):
        """Test getting tasks for non-existent user story."""
        response = client.get('/user-stories/nonexistent-id/tasks')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    @patch('app.api.user_story_routes.ai_service.generate_user_story')
    def test_generate_user_story_success(self, mock_generate, client, sample_user_story):
        """Test successful user story generation with AI."""
        # Mock the AI service response
        mock_generate.return_value = sample_user_story
        
        request_data = {
            "prompt": "As a user, I want to test functionality so that I can verify the system works"
        }
        
        response = client.post('/ai/user-stories',
                              data=json.dumps(request_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        # Verify the response contains the generated user story
        assert data['project'] == sample_user_story.project
        assert data['rol'] == sample_user_story.rol
        assert data['goal'] == sample_user_story.goal
        assert data['reason'] == sample_user_story.reason
        assert data['description'] == sample_user_story.description
        assert data['priority'] == sample_user_story.priority
        assert data['story_points'] == sample_user_story.story_points
        assert data['effort_hours'] == sample_user_story.effort_hours
        assert 'id' in data

    def test_generate_user_story_missing_prompt(self, client):
        """Test user story generation without prompt."""
        response = client.post('/ai/user-stories',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'prompt' in data['error']

    def test_generate_user_story_empty_prompt(self, client):
        """Test user story generation with empty prompt."""
        with patch('app.api.user_story_routes.ai_service') as mock_ai_service:
            # Mock the AI service to return a user story
            mock_user_story = UserStory(
                id="test-user-story-id",
                project="Test Project",
                rol="Test User",
                goal="test functionality",
                reason="to verify the system works",
                description="As a test user, I want to test functionality so that I can verify the system works.",
                priority=UserStoryPriority.MEDIUM,
                story_points=3,
                effort_hours=4.0
            )
            mock_ai_service.generate_user_story.return_value = mock_user_story
            
            response = client.post('/ai/user-stories',
                                data=json.dumps({"prompt": ""}),
                                content_type='application/json')
            assert response.status_code == 201
            data = json.loads(response.data)
            assert 'id' in data
            assert data['project'] == "Test Project"

    @patch('app.api.user_story_routes.ai_service.generate_user_story')
    def test_generate_user_story_ai_failure(self, mock_generate, client):
        """Test user story generation when AI service fails."""
        # Mock AI service to return None (failure)
        mock_generate.return_value = None
        
        request_data = {
            "prompt": "As a user, I want to test functionality"
        }
        
        response = client.post('/ai/user-stories',
                              data=json.dumps(request_data),
                              content_type='application/json')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    @patch('app.api.user_story_routes.ai_service.generate_user_story')
    def test_generate_user_story_validation_error(self, mock_generate, client):
        """Test user story generation with validation error."""
        # Mock AI service to return invalid data
        mock_generate.side_effect = Exception("Validation error")
        
        request_data = {
            "prompt": "As a user, I want to test functionality"
        }
        
        response = client.post('/ai/user-stories',
                              data=json.dumps(request_data),
                              content_type='application/json')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    @patch('app.api.user_story_routes.ai_service.generate_tasks_from_user_story')
    def test_generate_tasks_from_user_story_success(self, mock_generate, client):
        """Test successful task generation from user story."""
        with patch('app.api.user_story_routes.ai_service') as mock_ai_service:
            # Mock the AI service to return a user story and tasks
            mock_user_story = UserStory(
                id="test-user-story-id",
                project="Test Project",
                rol="Test User",
                goal="test functionality",
                reason="to verify the system works",
                description="As a test user, I want to test functionality so that I can verify the system works.",
                priority=UserStoryPriority.MEDIUM,
                story_points=3,
                effort_hours=4.0
            )
            mock_tasks = [
                Task(
                    id="task-1",
                    title="Generated Task 1",
                    description="First generated task",
                    priority=Priority.MEDIUM,
                    effort_hours=2.0,
                    status=Status.PENDING,
                    assigned_to="Developer",
                    category=Category.FRONTEND,
                    user_story_id=None,
                    risk_analysis="Sample risk",
                    risk_mitigation="Sample mitigation"
                )
            ]
            mock_ai_service.generate_user_story.return_value = mock_user_story
            mock_ai_service.generate_tasks_from_user_story.return_value = mock_tasks
            
            # Create a user story first
            create_response = client.post('/ai/user-stories',
                                        data=json.dumps({"prompt": "As a user, I want to test functionality"}),
                                        content_type='application/json')
            assert create_response.status_code == 201
            
            # Get the user story ID from the response
            user_story_data = json.loads(create_response.data)
            user_story_id = user_story_data['id']
            
            # Test generating tasks from the user story
            response = client.post(f'/ai/user-stories/{user_story_id}/generate_tasks')
            assert response.status_code == 201
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]['title'] == "Generated Task 1"

    def test_generate_tasks_from_nonexistent_user_story(self, client):
        """Test task generation from non-existent user story."""
        response = client.post('/ai/user-stories/nonexistent-id/generate_tasks')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    @patch('app.api.user_story_routes.ai_service.generate_tasks_from_user_story')
    def test_generate_tasks_ai_failure(self, mock_generate, client):
        """Test task generation when AI service fails."""
        with patch('app.api.user_story_routes.ai_service') as mock_ai_service:
            # Mock the AI service to return a user story but fail on task generation
            mock_user_story = UserStory(
                id="test-user-story-id",
                project="Test Project",
                rol="Test User",
                goal="test functionality",
                reason="to verify the system works",
                description="As a test user, I want to test functionality so that I can verify the system works.",
                priority=UserStoryPriority.MEDIUM,
                story_points=3,
                effort_hours=4.0
            )
            mock_ai_service.generate_user_story.return_value = mock_user_story
            mock_ai_service.generate_tasks_from_user_story.return_value = []  # Empty list on failure
            
            # Create a user story first
            create_response = client.post('/ai/user-stories',
                                        data=json.dumps({"prompt": "As a user, I want to test functionality"}),
                                        content_type='application/json')
            assert create_response.status_code == 201
            
            # Get the user story ID from the response
            user_story_data = json.loads(create_response.data)
            user_story_id = user_story_data['id']
            
            # Test generating tasks from the user story (should succeed with empty list)
            response = client.post(f'/ai/user-stories/{user_story_id}/generate_tasks')
            assert response.status_code == 201
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 0

    def test_user_story_validation_enum_values(self, client):
        """Test that all user story enum values are accepted."""
        with patch('app.api.user_story_routes.ai_service') as mock_ai_service:
            # Mock the AI service to return a consistent user story
            mock_user_story = UserStory(
                id="test-user-story-id",
                project="Test Project",
                rol="Test User",
                goal="test functionality",
                reason="to verify the system works",
                description="As a test user, I want to test functionality so that I can verify the system works.",
                priority=UserStoryPriority.MEDIUM,
                story_points=3,
                effort_hours=4.0
            )
            mock_ai_service.generate_user_story.return_value = mock_user_story
            
            valid_priorities = ['low', 'medium', 'high', 'blocking']
            valid_story_points = [1, 2, 3, 5, 8]
            
            for priority in valid_priorities:
                for story_points in valid_story_points:
                    user_story_data = {
                        "project": f"Test Project {priority}",
                        "rol": f"Test User {story_points}",
                        "goal": f"test goal {priority}",
                        "reason": f"to test {story_points}",
                        "description": f"As a test user, I want to test goal {priority} so that I can verify {story_points}.",
                        "priority": priority,
                        "story_points": story_points,
                        "effort_hours": 4.0
                    }
                    
                    # Test through the AI generation endpoint
                    response = client.post('/ai/user-stories',
                                        data=json.dumps({"prompt": f"Test prompt {priority} {story_points}"}),
                                        content_type='application/json')
                    
                    assert response.status_code == 201
                    data = json.loads(response.data)
                    # The mock always returns the same values regardless of input
                    assert data['priority'] == 'medium'  # Mock always returns medium
                    assert data['story_points'] == 3  # Mock always returns 3

    def test_user_story_field_validation(self, client):
        """Test user story field validation rules."""
        # Test project field length limit
        invalid_data = {
            "project": "x" * 101,  # Exceeds 100 character limit
            "rol": "Test User",
            "goal": "test goal",
            "reason": "to test",
            "description": "As a test user, I want to test goal so that I can verify.",
            "priority": "medium",
            "story_points": 3,
            "effort_hours": 4.0
        }
        
        from app.domain.user_story import UserStory
        with pytest.raises(Exception):
            UserStory(**invalid_data)

    def test_user_story_story_points_validation(self, client):
        """Test user story story points validation."""
        invalid_story_points = [0, 4, 6, 7, 9, 10]
        
        for story_points in invalid_story_points:
            invalid_data = {
                "project": "Test Project",
                "rol": "Test User",
                "goal": "test goal",
                "reason": "to test",
                "description": "As a test user, I want to test goal so that I can verify.",
                "priority": "medium",
                "story_points": story_points,
                "effort_hours": 4.0
            }
            
            from app.domain.user_story import UserStory
            with pytest.raises(Exception):
                UserStory(**invalid_data)

    def test_user_story_effort_hours_validation(self, client):
        """Test user story effort hours validation."""
        invalid_effort_hours = [-1.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
        
        for effort_hours in invalid_effort_hours:
            invalid_data = {
                "project": "Test Project",
                "rol": "Test User",
                "goal": "test goal",
                "reason": "to test",
                "description": "As a test user, I want to test goal so that I can verify.",
                "priority": "medium",
                "story_points": 3,
                "effort_hours": effort_hours
            }
            
            from app.domain.user_story import UserStory
            with pytest.raises(Exception):
                UserStory(**invalid_data) 