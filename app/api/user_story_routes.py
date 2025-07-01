from flask import Blueprint, request, jsonify, render_template
from app.application.user_story_service import UserStoryService
from app.application.task_service import TaskService
from app.application.ai_service import AIService
from uuid import uuid4
from app.domain.user_story import UserStory
from app.domain.task import Task
from pydantic import ValidationError
import os
from dotenv import load_dotenv

load_dotenv()

user_story_bp = Blueprint('user_stories', __name__)
user_story_service = UserStoryService()
task_service = TaskService()

# Get required environment variables
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Validate required environment variables
if not azure_endpoint or not azure_api_key:
    raise ValueError("Missing required environment variables: AZURE_OPENAI_ENDPOINT and/or AZURE_OPENAI_API_KEY")

ai_service = AIService(azure_endpoint=azure_endpoint, azure_api_key=azure_api_key)

@user_story_bp.route('/user-stories', methods=['GET'])
def get_user_stories():
    """Return the user-stories.html template with all user stories"""
    user_stories = user_story_service.list_user_stories()
    return render_template('user-stories.html', user_stories=user_stories)

@user_story_bp.route('/user-stories/<user_story_id>/tasks', methods=['GET'])
def get_user_story_tasks(user_story_id):
    """Return the tasks.html template with tasks for a specific user story"""
    user_story = user_story_service.get_user_story(user_story_id)
    if not user_story:
        return jsonify({'error': 'User story not found'}), 404
    
    # Get tasks for this user story
    tasks = task_service.get_tasks_by_user_story(user_story_id)
    return render_template('tasks.html', tasks=tasks, user_story=user_story)

@user_story_bp.route('/ai/user-stories', methods=['POST'])
def generate_user_story():
    """Generate a new UserStory using AI"""
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'prompt field is required'}), 400
    
    try:
        # Generate user story using AI
        user_story = ai_service.generate_user_story(data['prompt'])
        
        if user_story is None:
            return jsonify({'error': 'Failed to generate user story. Please try again.'}), 500
        
        # Add ID to the generated user story
        user_story_data = user_story.model_dump()
        user_story_data['id'] = str(uuid4())
        
        # Create the user story in the database
        created_user_story = user_story_service.create_user_story(user_story_data)
        return jsonify(created_user_story.model_dump()), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_story_bp.route('/ai/user-stories/<user_story_id>/generate_tasks', methods=['POST'])
def generate_tasks_from_user_story(user_story_id):
    """Generate Tasks from a UserStory using AI"""
    try:
        # Get the user story
        user_story = user_story_service.get_user_story(user_story_id)
        if not user_story:
            return jsonify({'error': 'User story not found'}), 404
        
        # Generate tasks using AI
        tasks = ai_service.generate_tasks_from_user_story(user_story)
        
        created_tasks = []
        for task in tasks:
            # Add ID and user_story_id to each task
            task_data = task.model_dump()
            task_data['id'] = str(uuid4())
            task_data['user_story_id'] = user_story_id
            
            # Create the task in the database
            created_task = task_service.create_task(task_data)
            created_tasks.append(created_task.model_dump())
        
        return jsonify(created_tasks), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 