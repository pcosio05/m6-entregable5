from flask import Blueprint, request, jsonify
from app.application.task_service import TaskService
from uuid import uuid4
from app.domain.task import Task
from pydantic import ValidationError

task_bp = Blueprint('tasks', __name__)
task_service = TaskService()

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        task_data = {
            'id': str(uuid4()),
            **data,
        }
        task = Task.parse_obj(task_data)
        task = task_service.create_task(task.model_dump())
        return jsonify(task.model_dump()), 201
    except ValidationError as e:
        # Convert validation errors to serializable format
        error_messages = []
        for error in e.errors():
            error_messages.append({
                'field': error['loc'][0] if error['loc'] else 'unknown',
                'message': error['msg'],
                'type': error['type']
            })
        return jsonify({'error': error_messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = task_service.list_tasks()
    return jsonify([task.model_dump() for task in tasks])

@task_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = task_service.get_task(task_id)
    if task:
        return jsonify(task.model_dump())
    return jsonify({'error': 'Task not found'}), 404

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    try:
        existing_task = task_service.get_task(task_id)
        if not existing_task:
            return jsonify({'error': 'Task not found'}), 404
        updated_data = existing_task.model_dump()
        updated_data.update(data)
        updated_task = Task.parse_obj(updated_data)
        task = task_service.update_task(task_id, updated_task.model_dump())
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.model_dump())
    except ValidationError as e:
        # Convert validation errors to serializable format
        error_messages = []
        for error in e.errors():
            error_messages.append({
                'field': error['loc'][0] if error['loc'] else 'unknown',
                'message': error['msg'],
                'type': error['type']
            })
        return jsonify({'error': error_messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_service.delete_task(task_id):
        return '', 204
    return jsonify({'error': 'Task not found'}), 404 