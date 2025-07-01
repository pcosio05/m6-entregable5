from dotenv import load_dotenv
load_dotenv()
from flask import Blueprint, request, jsonify
from app.application.ai_service import AIService
from app.application.task_service import TaskService
import os
from uuid import uuid4
from app.domain.task import Task
from pydantic import ValidationError

ai_bp = Blueprint('ai', __name__)

# Get required environment variables
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Validate required environment variables
if not azure_endpoint or not azure_api_key:
    raise ValueError("Missing required environment variables: AZURE_OPENAI_ENDPOINT and/or AZURE_OPENAI_API_KEY")

ai_service = AIService(azure_endpoint=azure_endpoint, azure_api_key=azure_api_key)
task_service = TaskService()

@ai_bp.route('/tasks/describe', methods=['POST'])
def describe_task():
    data = request.get_json()
    try:
        # Generate description using AI
        description = ai_service.generate_task_description(data)
        task_data = {
            'id': str(uuid4()),
            **data,
            'description': description,
        }
        task = Task.parse_obj(task_data)
        task = task_service.create_task(task.model_dump())
        return jsonify(task.model_dump()), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/tasks/categorize', methods=['POST'])
def categorize_task():
    data = request.get_json()
    try:
        # Generate category using AI
        category = ai_service.generate_task_category(data)
        task_data = {
            'id': str(uuid4()),
            **data,
            'category': category,
        }
        task = Task.parse_obj(task_data)
        task = task_service.create_task(task.model_dump())
        return jsonify(task.model_dump()), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/tasks/estimate', methods=['POST'])
def estimate_task():
    data = request.get_json()
    try:
        # Generate effort hours estimate using AI
        effort_hours = ai_service.estimate_effort_hours(data)
        task_data = {
            'id': str(uuid4()),
            **data,
            'effort_hours': effort_hours,
        }
        task = Task.parse_obj(task_data)
        task = task_service.create_task(task.model_dump())
        return jsonify(task.model_dump()), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/tasks/audit', methods=['POST'])
def audit_task():
    data = request.get_json()
    try:
        # Generate risk analysis using AI
        risk_analysis = ai_service.generate_risk_analysis(data)
        # Generate risk mitigation strategies using AI
        risk_mitigation = ai_service.generate_risk_mitigation(data, risk_analysis)
        task_data = {
            'id': str(uuid4()),
            **data,
            'risk_analysis': risk_analysis,
            'risk_mitigation': risk_mitigation,
        }
        task = Task.parse_obj(task_data)
        task = task_service.create_task(task.model_dump())
        return jsonify(task.model_dump()), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 