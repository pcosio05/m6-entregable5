import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock

# Set test environment variables before importing app modules
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://test.openai.azure.com/'
os.environ['AZURE_OPENAI_API_KEY'] = 'test-api-key'

from app import create_app
from app.domain.task import Task, Priority, Status, Category
from app.domain.user_story import UserStory, UserStoryPriority
from app.infrastructure.models import Base
from app.infrastructure.db import engine, SessionLocal
from uuid import uuid4

@pytest.fixture(scope="function")
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def clean_database():
    """Clean the database before and after each test."""
    # Clean up before test
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
    
    yield
    
    # Clean up after test
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())

@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
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

@pytest.fixture
def sample_user_story_data():
    """Sample user story data for testing."""
    return {
        "project": "Test Project",
        "rol": "Test User",
        "goal": "test functionality",
        "reason": "to verify the system works",
        "description": "As a test user, I want to test functionality so that I can verify the system works.",
        "priority": "medium",
        "story_points": 3,
        "effort_hours": 4.0
    }

@pytest.fixture
def sample_task():
    """Create a sample Task domain object."""
    return Task(
        id=str(uuid4()),
        title="Sample Task",
        description="A sample task for testing",
        priority=Priority.HIGH,
        effort_hours=3.0,
        status=Status.PENDING,
        assigned_to="Test Developer",
        category=Category.BACKEND,
        user_story_id=None,
        risk_analysis="Sample risk analysis",
        risk_mitigation="Sample risk mitigation"
    )

@pytest.fixture
def sample_user_story():
    """Create a sample UserStory domain object."""
    return UserStory(
        id=str(uuid4()),
        project="Sample Project",
        rol="Sample User",
        goal="sample goal",
        reason="to test the system",
        description="As a sample user, I want to achieve a sample goal so that I can test the system.",
        priority=UserStoryPriority.MEDIUM,
        story_points=5,
        effort_hours=6.0
    )

@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing."""
    mock_service = Mock()
    
    # Mock generate_user_story method
    mock_user_story = UserStory(
        id=str(uuid4()),
        project="AI Generated Project",
        rol="AI User",
        goal="ai generated goal",
        reason="to test AI generation",
        description="As an AI user, I want to achieve an AI generated goal so that I can test AI generation.",
        priority=UserStoryPriority.MEDIUM,
        story_points=3,
        effort_hours=4.0
    )
    mock_service.generate_user_story.return_value = mock_user_story
    
    # Mock generate_tasks_from_user_story method
    mock_tasks = [
        Task(
            id=str(uuid4()),
            title="AI Generated Task 1",
            description="First AI generated task",
            priority=Priority.MEDIUM,
            effort_hours=2.0,
            status=Status.PENDING,
            assigned_to="AI Developer",
            category=Category.FRONTEND,
            user_story_id=None,
            risk_analysis="AI risk analysis",
            risk_mitigation="AI risk mitigation"
        ),
        Task(
            id=str(uuid4()),
            title="AI Generated Task 2",
            description="Second AI generated task",
            priority=Priority.HIGH,
            effort_hours=3.0,
            status=Status.PENDING,
            assigned_to="AI Developer",
            category=Category.BACKEND,
            user_story_id=None,
            risk_analysis="AI risk analysis 2",
            risk_mitigation="AI risk mitigation 2"
        )
    ]
    mock_service.generate_tasks_from_user_story.return_value = mock_tasks
    
    return mock_service

@pytest.fixture
def mock_environment_variables():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-api-key',
        'DATABASE_URL': 'sqlite:///:memory:'
    }):
        yield 