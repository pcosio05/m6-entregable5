from openai import OpenAI
from typing import Dict, Any, Optional, List
import os
from app.application.log_service import LogService
from app.domain.task import Category
from app.domain.user_story import UserStory, UserStoryPriority
from app.domain.task import Task
from app.domain.tasks import Tasks

model = "gpt-4o-mini"

class AIService:
    def __init__(self, azure_endpoint: str, azure_api_key: str, log_service: Optional[LogService] = None):
        self.clientOpenai = OpenAI(
            base_url=azure_endpoint,
            api_key=azure_api_key,
            default_query={"api-version": "preview"}, 
        )
        self.log_service = log_service if log_service is not None else LogService()

    def generate_task_description(self, task_data: Dict[str, Any]) -> str:
        prompt = f"Generate a concise task description (max 20 words) for a task with title: {task_data['title']}, " \
                f"priority: {task_data['priority']}, effort hours: {task_data['effort_hours']}, " \
                f"status: {task_data['status']}, assigned to: {task_data['assigned_to']} and category{task_data['category']}"

        response = self.clientOpenai.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a task description generator. These tasks are for a task management system of a software company's development team. Keep the descriptions concise and professional. The fields received are: title, priority, effort_hours, status, assigned_to. From there, generate a good description that can make sense for the task that matches the title and category that comes in the request. The result should not exceed 100 words."},
                {"role": "user", "content": prompt}
            ],
            max_output_tokens=50,
            temperature=0.5,
            top_p=0.5
        )

        usage = getattr(response, 'usage', {})
        input_tokens_used = getattr(usage, 'input_tokens', 0)
        output_tokens_used = getattr(usage, 'output_tokens', 0)
        self.log_service.log_token_usage(
            endpoint="/ai/tasks/describe",
            input_tokens_used=input_tokens_used,
            output_tokens_used=output_tokens_used,
            model=model
        )

        return response.output_text

    def generate_task_category(self, task_data: Dict[str, Any]) -> str:
        prompt = f"Based on the following task details, determine the most appropriate category (Frontend, Backend, Testing, Infra, or Mobile):\n" \
                f"Title: {task_data['title']}\n" \
                f"Description: {task_data['description']}\n" \
                f"Priority: {task_data['priority']}\n" \
                f"Effort Hours: {task_data['effort_hours']}\n" \
                f"Status: {task_data['status']}\n" \
                f"Assigned To: {task_data['assigned_to']}"

        response = self.clientOpenai.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a task categorizer. Your task is to determine the most appropriate category for a development task. The categories are: Frontend, Backend, Testing, Infra, and Mobile. You must respond with exactly one of these categories, nothing else."},
                {"role": "user", "content": prompt}
            ],
            max_output_tokens=50,
            temperature=0.5,
            top_p=0.5
        )

        usage = getattr(response, 'usage', {})
        input_tokens_used = getattr(usage, 'input_tokens', 0)
        output_tokens_used = getattr(usage, 'output_tokens', 0)
        self.log_service.log_token_usage(
            endpoint="/ai/tasks/categorize",
            input_tokens_used=input_tokens_used,
            output_tokens_used=output_tokens_used,
            model=model
        )

        # Validate and return the category
        category = response.output_text.strip()
        try:
            return Category(category).value
        except ValueError:
            # If AI returns an invalid category, default to Backend
            return Category.BACKEND.value

    def estimate_effort_hours(self, task_data: Dict[str, Any]) -> float:
        prompt = f"Based on the following task details, estimate the effort hours needed (respond with a single number with one decimal place):\n" \
                f"Title: {task_data['title']}\n" \
                f"Description: {task_data['description']}\n" \
                f"Category: {task_data['category']}"

        response = self.clientOpenai.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a task effort estimator. Your task is to estimate the number of hours needed to complete a development task. Consider the task's title, description and category. Respond with a single number with one decimal place (e.g., 2.5, 4.0, 8.5). The estimate should be realistic and consider the task's scope."},
                {"role": "user", "content": prompt}
            ],
            max_output_tokens=50,
            temperature=0.5,
            top_p=0.5
        )

        usage = getattr(response, 'usage', {})
        input_tokens_used = getattr(usage, 'input_tokens', 0)
        output_tokens_used = getattr(usage, 'output_tokens', 0)
        self.log_service.log_token_usage(
            endpoint="/ai/tasks/estimate",
            input_tokens_used=input_tokens_used,
            output_tokens_used=output_tokens_used,
            model=model
        )

        # Parse and validate the effort hours
        try:
            effort_hours = float(response.output_text.strip())
            return round(effort_hours, 1)  # Ensure one decimal place
        except ValueError:
            # If AI returns an invalid number, return a default value
            return 4.0

    def generate_risk_analysis(self, task_data: Dict[str, Any]) -> str:
        prompt = f"Analyze the potential risks for the following task:\n" \
                f"Title: {task_data['title']}\n" \
                f"Description: {task_data['description']}\n" \
                f"Priority: {task_data['priority']}\n" \
                f"Effort Hours: {task_data['effort_hours']}\n" \
                f"Status: {task_data['status']}\n" \
                f"Assigned To: {task_data['assigned_to']}\n" \
                f"Category: {task_data['category']}"

        response = self.clientOpenai.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a risk analyst for software development tasks. Analyze the potential risks associated with the given task, considering factors like technical complexity, dependencies, resource availability, and project impact. Provide a concise but comprehensive risk analysis that identifies key areas of concern. Generated text should be shorter than 1024 characters"},
                {"role": "user", "content": prompt}
            ],
            max_output_tokens=200,
            temperature=0.5,
            top_p=0.5
        )

        usage = getattr(response, 'usage', {})
        input_tokens_used = getattr(usage, 'input_tokens', 0)
        output_tokens_used = getattr(usage, 'output_tokens', 0)
        self.log_service.log_token_usage(
            endpoint="/ai/tasks/audit/risk_analysis",
            input_tokens_used=input_tokens_used,
            output_tokens_used=output_tokens_used,
            model=model
        )

        return response.output_text

    def generate_risk_mitigation(self, task_data: Dict[str, Any], risk_analysis: str) -> str:
        prompt = f"Based on the following task details and risk analysis, provide risk mitigation strategies:\n" \
                f"Task Details:\n" \
                f"Title: {task_data['title']}\n" \
                f"Description: {task_data['description']}\n" \
                f"Priority: {task_data['priority']}\n" \
                f"Effort Hours: {task_data['effort_hours']}\n" \
                f"Status: {task_data['status']}\n" \
                f"Assigned To: {task_data['assigned_to']}\n" \
                f"Category: {task_data['category']}\n\n" \
                f"Risk Analysis:\n{risk_analysis}"

        response = self.clientOpenai.responses.create(
            model=model,
            input=[
                {"role": "system", "content": "You are a risk mitigation strategist for software development tasks. Based on the provided risk analysis, suggest practical and actionable strategies to mitigate each identified risk. Focus on concrete steps that can be taken to reduce or eliminate the risks while maintaining project quality and timeline. Generated text should be shorter than 1024 characters"},
                {"role": "user", "content": prompt}
            ],
            max_output_tokens=200,
            temperature=0.5,
            top_p=0.5
        )

        # Log token usage
        usage = getattr(response, 'usage', {})
        input_tokens_used = getattr(usage, 'input_tokens', 0)
        output_tokens_used = getattr(usage, 'output_tokens', 0)
        self.log_service.log_token_usage(
            endpoint="/ai/tasks/audit/risk_mitigation",
            input_tokens_used=input_tokens_used,
            output_tokens_used=output_tokens_used,
            model=model
        )

        return response.output_text

    def generate_user_story(self, prompt: str) -> UserStory | None:
        """Generate a UserStory using the parse method"""
        try:
            response = self.clientOpenai.responses.parse(
                model=model,
                input=[
                    {"role": "system", "content": "You are a user story generator for software development projects. Based on the user's prompt, generate a complete user story with all required fields. The user story should follow the format: 'As a [role], I want [goal] so that [reason]'. Make sure all fields are realistic and appropriate for a software development context."},
                    {"role": "user", "content": prompt}
                ],
                text_format=UserStory,
                max_output_tokens=500,
                temperature=0.7,
                top_p=0.8
            )

            usage = getattr(response, 'usage', {})
            input_tokens_used = getattr(usage, 'input_tokens', 0)
            output_tokens_used = getattr(usage, 'output_tokens', 0)
            self.log_service.log_token_usage(
                endpoint="/ai/user-stories",
                input_tokens_used=input_tokens_used,
                output_tokens_used=output_tokens_used,
                model=model
            )

            return response.output_parsed if response.output_parsed else None
            
        except Exception as e:
            print(f"Error generating user story: {e}")
            return None
    

    def generate_tasks_from_user_story(self, user_story: UserStory) -> List[Task]:
        """Generate Tasks from a UserStory using the parse method"""
        try:
            prompt = f"""Based on the following user story, generate 3-5 development tasks that would be needed to implement this feature:

User Story:
- Project: {user_story.project}
- Role: {user_story.rol}
- Goal: {user_story.goal}
- Reason: {user_story.reason}
- Description: {user_story.description}
- Priority: {user_story.priority}
- Story Points: {user_story.story_points}
- Effort Hours: {user_story.effort_hours}

Generate tasks that cover different aspects of the implementation (frontend, backend, testing, etc.) and ensure they are properly sized and categorized."""

            response = self.clientOpenai.responses.parse(
                model=model,
                input=[
                    {"role": "system", "content": "You are a task generator for software development projects. Based on a user story, generate multiple development tasks that would be needed to implement the feature. Each task should be specific, actionable, and properly categorized. Tasks should cover different aspects like frontend, backend, testing, etc."},
                    {"role": "user", "content": prompt}
                ],
                text_format=Tasks,
                max_output_tokens=800,
                temperature=0.7,
                top_p=0.8
            )

            usage = getattr(response, 'usage', {})
            input_tokens_used = getattr(usage, 'input_tokens', 0)
            output_tokens_used = getattr(usage, 'output_tokens', 0)
            self.log_service.log_token_usage(
                endpoint="/ai/user-stories/generate_tasks",
                input_tokens_used=input_tokens_used,
                output_tokens_used=output_tokens_used,
                model=model
            )
            if response.output_parsed:
                return response.output_parsed.tasks
            else:
                return []
        except Exception as e:
            print(f"Error generating tasks from user story: {e}")
            return []