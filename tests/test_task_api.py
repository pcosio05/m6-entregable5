import json
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from app.domain.task import Priority, Status, Category
from app.domain.user_story import UserStory, UserStoryPriority

@pytest.fixture
def sample_task_data():
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "high",
        "effort_hours": 2.5,
        "status": "pending",
        "assigned_to": "Test User",
        "category": "Frontend"
    }

class TestTaskAPI:
    """Test suite for Task API endpoints."""
    
    def test_create_task_success(self, client, sample_task_data):
        """Test successful task creation."""
        response = client.post('/tasks',
                              data=json.dumps(sample_task_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        # Verify all fields are present and correct
        assert data['title'] == sample_task_data['title']
        assert data['description'] == sample_task_data['description']
        assert data['priority'] == sample_task_data['priority']
        assert data['effort_hours'] == sample_task_data['effort_hours']
        assert data['status'] == sample_task_data['status']
        assert data['assigned_to'] == sample_task_data['assigned_to']
        assert data['category'] == sample_task_data['category']
        assert 'id' in data
        assert data['user_story_id'] is None
        assert data['risk_analysis'] is None
        assert data['risk_mitigation'] is None

    def test_create_task_with_user_story_id(self, client):
        """Test creating a task with a user story ID."""
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
            
            # First create a user story
            user_story_response = client.post('/ai/user-stories',
                                            data=json.dumps({"prompt": "As a user, I want to test functionality"}),
                                            content_type='application/json')
            assert user_story_response.status_code == 201
            user_story_id = json.loads(user_story_response.data)['id']
            
            # Create a task with the user story ID
            task_data = {
                "title": "Test Task with User Story",
                "description": "This is a test task with user story",
                "priority": "medium",
                "effort_hours": 4.0,
                "status": "pending",
                "assigned_to": "Test User",
                "category": "Frontend",
                "user_story_id": user_story_id,
                "risk_analysis": "Sample risk analysis",
                "risk_mitigation": "Sample risk mitigation"
            }
            
            response = client.post('/tasks',
                                data=json.dumps(task_data),
                                content_type='application/json')
            
            if response.status_code != 201:
                print(f"Error response: {response.data}")
                error_data = json.loads(response.data)
                print(f"Error details: {error_data}")
            
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['title'] == "Test Task with User Story"
            assert data['user_story_id'] == user_story_id

    def test_create_task_missing_required_fields(self, client):
        """Test task creation with missing required fields."""
        incomplete_data = {"title": "Incomplete Task"}
        
        response = client.post('/tasks',
                              data=json.dumps(incomplete_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_task_description_too_long(self, client, sample_task_data):
        """Test task creation with description exceeding limit."""
        sample_task_data['description'] = 'x' * 1001
        
        response = client.post('/tasks',
                              data=json.dumps(sample_task_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_task_invalid_priority(self, client, sample_task_data):
        """Test task creation with invalid priority."""
        sample_task_data['priority'] = 'invalid_priority'
        
        response = client.post('/tasks',
                              data=json.dumps(sample_task_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_task_invalid_status(self, client, sample_task_data):
        """Test task creation with invalid status."""
        sample_task_data['status'] = 'invalid_status'
        
        response = client.post('/tasks',
                              data=json.dumps(sample_task_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_task_invalid_category(self, client, sample_task_data):
        """Test task creation with invalid category."""
        sample_task_data['category'] = 'invalid_category'
        
        response = client.post('/tasks',
                              data=json.dumps(sample_task_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_task_negative_effort_hours(self, client, sample_task_data):
        """Test task creation with negative effort hours."""
        sample_task_data['effort_hours'] = -1.0
        
        response = client.post('/tasks',
                              data=json.dumps(sample_task_data),
                              content_type='application/json')
        
        # This should work since validation is handled at the API level
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['effort_hours'] == -1.0

    def test_get_all_tasks_empty(self, client):
        """Test getting all tasks when database is empty."""
        response = client.get('/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # The database should be empty due to clean_database fixture
        assert len(data) == 0

    def test_get_all_tasks_with_data(self, client, sample_task_data):
        """Test getting all tasks when tasks exist."""
        # Create a task first
        create_response = client.post('/tasks',
                                    data=json.dumps(sample_task_data),
                                    content_type='application/json')
        assert create_response.status_code == 201
        
        # Get all tasks
        response = client.get('/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['title'] == sample_task_data['title']

    def test_get_task_by_id_success(self, client, sample_task_data):
        """Test getting a specific task by ID."""
        # Create a task first
        create_response = client.post('/tasks',
                                    data=json.dumps(sample_task_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Get the task by ID
        response = client.get(f'/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == sample_task_data['title']

    def test_get_task_by_id_not_found(self, client):
        """Test getting a task with non-existent ID."""
        response = client.get('/tasks/nonexistent-id')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_task_success(self, client, sample_task_data):
        """Test successful task update."""
        # Create a task first
        create_response = client.post('/tasks',
                                    data=json.dumps(sample_task_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Update the task
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "priority": "medium",
            "effort_hours": 3.0,
            "status": "in progress",
            "assigned_to": "Updated User",
            "category": "Frontend",
            "risk_analysis": "Updated risk analysis",
            "risk_mitigation": "Updated risk mitigation"
        }
        
        response = client.put(f'/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == update_data['title']
        assert data['description'] == update_data['description']
        assert data['priority'] == update_data['priority']
        assert data['effort_hours'] == update_data['effort_hours']
        assert data['status'] == update_data['status']
        assert data['assigned_to'] == update_data['assigned_to']
        assert data['category'] == update_data['category']
        assert data['risk_analysis'] == update_data['risk_analysis']
        assert data['risk_mitigation'] == update_data['risk_mitigation']

    def test_update_task_partial(self, client, sample_task_data):
        """Test partial task update."""
        # Create a task first
        create_response = client.post('/tasks',
                                    data=json.dumps(sample_task_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Update only title
        update_data = {"title": "Partially Updated Title"}
        
        response = client.put(f'/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        # Other fields should remain unchanged
        assert data['description'] == sample_task_data['description']

    def test_update_task_not_found(self, client):
        """Test updating a non-existent task."""
        update_data = {"title": "Updated Title"}
        
        response = client.put('/tasks/nonexistent-id',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_task_invalid_data(self, client, sample_task_data):
        """Test updating a task with invalid data."""
        # Create a task first
        create_response = client.post('/tasks',
                                    data=json.dumps(sample_task_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Try to update with invalid priority
        update_data = {"priority": "invalid_priority"}
        
        response = client.put(f'/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_delete_task_success(self, client, sample_task_data):
        """Test successful task deletion."""
        # Create a task first
        create_response = client.post('/tasks',
                                    data=json.dumps(sample_task_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Delete the task
        response = client.delete(f'/tasks/{task_id}')
        
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f'/tasks/{task_id}')
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task."""
        response = client.delete('/tasks/nonexistent-id')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_task_validation_enum_values(self, client):
        """Test that all enum values are accepted."""
        valid_priorities = ['low', 'medium', 'high', 'blocking']
        valid_statuses = ['pending', 'in progress', 'in review', 'completed']
        valid_categories = ['Frontend', 'Backend', 'Testing', 'Infra', 'Mobile']
        
        for priority in valid_priorities:
            for status in valid_statuses:
                for category in valid_categories:
                    task_data = {
                        "title": f"Test Task {priority} {status} {category}",
                        "description": "Test description",
                        "priority": priority,
                        "effort_hours": 1.0,
                        "status": status,
                        "assigned_to": "Test User",
                        "category": category
                    }
                    
                    response = client.post('/tasks',
                                          data=json.dumps(task_data),
                                          content_type='application/json')
                    
                    assert response.status_code == 201, f"Failed for priority={priority}, status={status}, category={category}" 