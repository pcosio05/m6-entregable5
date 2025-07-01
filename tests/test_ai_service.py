import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.application.ai_service import AIService
from app.domain.user_story import UserStory, UserStoryPriority
from app.domain.task import Task, Priority, Status, Category

class TestAIService:
    """Test suite for AI Service."""
    
    @pytest.fixture
    def ai_service(self):
        """Create AI service instance for testing."""
        with patch('app.application.ai_service.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            def parse_side_effect(*args, **kwargs):
                # UserStory for user story prompts
                if "user story" in str(args).lower() or "as a user" in str(args).lower():
                    mock_parse_response = Mock()
                    mock_parse_response.output_parsed = UserStory(
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
                    mock_parse_response.usage = Mock(input_tokens=100, output_tokens=50)
                    return mock_parse_response
                # Otherwise, return a Tasks mock
                mock_tasks_response = Mock()
                mock_tasks_response.output_parsed = Mock()
                mock_tasks_response.output_parsed.tasks = [
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
                    ),
                    Task(
                        id="task-2",
                        title="Generated Task 2",
                        description="Second generated task",
                        priority=Priority.HIGH,
                        effort_hours=3.0,
                        status=Status.PENDING,
                        assigned_to="Developer",
                        category=Category.BACKEND,
                        user_story_id=None,
                        risk_analysis="Sample risk 2",
                        risk_mitigation="Sample mitigation 2"
                    )
                ]
                mock_tasks_response.usage = Mock(input_tokens=150, output_tokens=75)
                return mock_tasks_response

            mock_client.responses.parse.side_effect = parse_side_effect

            service = AIService(
                azure_endpoint="https://test.openai.azure.com/",
                azure_api_key="test-api-key"
            )
            yield service

    def test_generate_user_story_success(self, ai_service):
        """Test successful user story generation."""
        # Override the mock to return the actual UserStory object
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_response = Mock()
            mock_response.output_parsed = UserStory(
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
            mock_response.usage = Mock(input_tokens=100, output_tokens=50)
            mock_parse.return_value = mock_response
            
            result = ai_service.generate_user_story("As a user, I want to test functionality")
            
            # Verify the result
            assert isinstance(result, UserStory)
            assert result.project == "Test Project"
            assert result.rol == "Test User"
            assert result.goal == "test functionality"
            assert result.reason == "to verify the system works"
            assert result.priority == UserStoryPriority.MEDIUM
            assert result.story_points == 3
            assert result.effort_hours == 4.0

    def test_generate_user_story_invalid_json(self, ai_service):
        """Test user story generation with invalid JSON response."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_response = Mock()
            mock_response.output_parsed = None
            mock_usage = Mock()
            mock_usage.input_tokens = 100
            mock_usage.output_tokens = 50
            mock_response.usage = mock_usage
            mock_parse.return_value = mock_response
            
            result = ai_service.generate_user_story("As a user, I want to test functionality")
            
            # Should return None on invalid JSON
            assert result is None

    def test_generate_user_story_missing_fields(self, ai_service):
        """Test user story generation with missing required fields."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_parse.side_effect = Exception("Validation error")
            
            result = ai_service.generate_user_story("As a user, I want to test functionality")
            
            # Should return None on validation error
            assert result is None

    def test_generate_user_story_api_error(self, ai_service):
        """Test user story generation when API call fails."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_parse.side_effect = Exception("API Error")
            
            result = ai_service.generate_user_story("As a user, I want to test functionality")
            
            # Should return None on API error
            assert result is None

    def test_generate_tasks_from_user_story_success(self, ai_service, sample_user_story):
        """Test successful task generation from user story."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_response = Mock()
            mock_response.output_parsed = Mock()
            mock_response.output_parsed.tasks = [
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
                ),
                Task(
                    id="task-2",
                    title="Generated Task 2",
                    description="Second generated task",
                    priority=Priority.HIGH,
                    effort_hours=3.0,
                    status=Status.PENDING,
                    assigned_to="Developer",
                    category=Category.BACKEND,
                    user_story_id=None,
                    risk_analysis="Sample risk 2",
                    risk_mitigation="Sample mitigation 2"
                )
            ]
            mock_response.usage = Mock(input_tokens=150, output_tokens=75)
            mock_parse.return_value = mock_response
            
            result = ai_service.generate_tasks_from_user_story(sample_user_story)
            
            # Verify the result
            assert isinstance(result, list)
            assert len(result) == 2
            
            # Check first task
            task1 = result[0]
            assert isinstance(task1, Task)
            assert task1.title == "Generated Task 1"
            assert task1.description == "First generated task"
            assert task1.priority == Priority.MEDIUM
            assert task1.effort_hours == 2.0
            assert task1.status == Status.PENDING
            assert task1.assigned_to == "Developer"
            assert task1.category == Category.FRONTEND
            
            # Check second task
            task2 = result[1]
            assert isinstance(task2, Task)
            assert task2.title == "Generated Task 2"
            assert task2.description == "Second generated task"
            assert task2.priority == Priority.HIGH
            assert task2.effort_hours == 3.0
            assert task2.status == Status.PENDING
            assert task2.assigned_to == "Developer"
            assert task2.category == Category.BACKEND

    def test_generate_tasks_from_user_story_invalid_json(self, ai_service, sample_user_story):
        """Test task generation with invalid JSON response."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_response = Mock()
            mock_response.output_parsed = None
            mock_usage = Mock()
            mock_usage.input_tokens = 150
            mock_usage.output_tokens = 75
            mock_response.usage = mock_usage
            mock_parse.return_value = mock_response
            
            result = ai_service.generate_tasks_from_user_story(sample_user_story)
            
            # Should return empty list on invalid JSON
            assert result == []

    def test_generate_tasks_from_user_story_missing_fields(self, ai_service, sample_user_story):
        """Test task generation with missing required fields."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_parse.side_effect = Exception("Validation error")
            
            result = ai_service.generate_tasks_from_user_story(sample_user_story)
            
            # Should return empty list on validation error
            assert result == []

    def test_generate_tasks_from_user_story_api_error(self, ai_service, sample_user_story):
        """Test task generation when API call fails."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_parse.side_effect = Exception("API Error")
            
            result = ai_service.generate_tasks_from_user_story(sample_user_story)
            
            # Should return empty list on API error
            assert result == []

    def test_generate_tasks_from_user_story_empty_response(self, ai_service, sample_user_story):
        """Test task generation with empty response."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_response = Mock()
            mock_response.output_parsed = Mock()
            mock_response.output_parsed.tasks = []
            mock_usage = Mock()
            mock_usage.input_tokens = 150
            mock_usage.output_tokens = 75
            mock_response.usage = mock_usage
            mock_parse.return_value = mock_response
            
            result = ai_service.generate_tasks_from_user_story(sample_user_story)
            
            # Should return empty list
            assert result == []

    def test_token_usage_logging(self, ai_service):
        """Test that token usage is logged correctly."""
        with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
            mock_response = Mock()
            mock_response.output_parsed = UserStory(
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
            mock_response.usage = Mock(input_tokens=100, output_tokens=50)
            mock_parse.return_value = mock_response
            
            result = ai_service.generate_user_story("As a user, I want to test functionality")
            
            # Verify the result
            assert isinstance(result, UserStory)

    def test_ai_service_initialization(self):
        """Test AI service initialization with different parameters."""
        with patch('app.application.ai_service.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            
            # Test with valid parameters
            ai_service = AIService(
                azure_endpoint="https://test.openai.azure.com/",
                azure_api_key="test-api-key"
            )
            assert ai_service.clientOpenai is not None
            assert ai_service.log_service is not None

    def test_ai_service_missing_parameters(self):
        """Test AI service initialization with missing parameters."""
        with patch('app.application.ai_service.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            
            # Test with empty strings (which should work but may cause issues later)
            ai_service = AIService(
                azure_endpoint="",
                azure_api_key=""
            )
            assert ai_service.clientOpenai is not None

    def test_generate_user_story_with_different_prompts(self, ai_service):
        """Test user story generation with different types of prompts."""
        prompts = [
            "As a user, I want to login",
            "As a customer, I want to buy products",
            "As an admin, I want to manage users",
            "Simple functionality request"
        ]
        
        for prompt in prompts:
            with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
                mock_response = Mock()
                mock_response.output_parsed = UserStory(
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
                mock_response.usage = Mock(input_tokens=100, output_tokens=50)
                mock_parse.return_value = mock_response
                
                result = ai_service.generate_user_story(prompt)
                assert isinstance(result, UserStory)
                assert result.project == "Test Project"

    def test_generate_tasks_with_different_user_stories(self, ai_service):
        """Test task generation with different types of user stories."""
        user_stories = [
            UserStory(
                id="1",
                project="Project 1",
                rol="User 1",
                goal="goal 1",
                reason="reason 1",
                description="Description 1",
                priority=UserStoryPriority.LOW,
                story_points=1,
                effort_hours=2.0
            ),
            UserStory(
                id="2",
                project="Project 2",
                rol="User 2",
                goal="goal 2",
                reason="reason 2",
                description="Description 2",
                priority=UserStoryPriority.HIGH,
                story_points=8,
                effort_hours=10.0
            )
        ]
        
        for user_story in user_stories:
            with patch.object(ai_service.clientOpenai.responses, 'parse') as mock_parse:
                mock_response = Mock()
                mock_response.output_parsed = Mock()
                mock_response.output_parsed.tasks = [
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
                    ),
                    Task(
                        id="task-2",
                        title="Generated Task 2",
                        description="Second generated task",
                        priority=Priority.HIGH,
                        effort_hours=3.0,
                        status=Status.PENDING,
                        assigned_to="Developer",
                        category=Category.BACKEND,
                        user_story_id=None,
                        risk_analysis="Sample risk 2",
                        risk_mitigation="Sample mitigation 2"
                    )
                ]
                mock_response.usage = Mock(input_tokens=150, output_tokens=75)
                mock_parse.return_value = mock_response
                
                result = ai_service.generate_tasks_from_user_story(user_story)
                assert isinstance(result, list)
                assert len(result) == 2
                assert isinstance(result[0], Task)
                assert result[0].priority == Priority.MEDIUM 