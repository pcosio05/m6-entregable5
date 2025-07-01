# Task Management System with AI-Powered User Stories

A Flask-based task management system that follows Hexagonal Architecture principles and includes AI-powered features for generating user stories and tasks using Azure OpenAI.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Azure OpenAI API access

### 1. Bootstrap the System

#### Start MySQL Database
```bash
# Start the MySQL database using Docker Compose
docker-compose up -d db

# Verify the database is running
docker-compose ps
```

#### Set Up Environment Variables
Create a `.env` file in the root directory:

```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/m4_entregable3
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
```

#### Install Dependencies
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📋 User Story Endpoints

The system provides comprehensive user story management with AI-powered generation capabilities.

### Web Interface Endpoints

#### 1. User Stories Dashboard
- **URL**: `GET /user-stories`
- **Description**: Web interface to view all user stories
- **Features**:
  - List all user stories with their details
  - Generate new user stories using AI
  - Navigate to tasks for each user story
  - Generate tasks for user stories using AI

#### 2. User Story Tasks View
- **URL**: `GET /user-stories/<user_story_id>/tasks`
- **Description**: Web interface showing tasks for a specific user story
- **Features**:
  - Display user story details
  - Show all tasks associated with the user story
  - Navigate back to user stories list

### AI-Powered API Endpoints

#### 3. Generate User Story with AI
- **URL**: `POST /ai/user-stories`
- **Description**: Generate a complete user story from a natural language prompt
- **Request Body**:
```json
{
    "prompt": "As a customer, I want to reset my password so that I can access my account if I forget my credentials"
}
```
- **Response**: Returns the generated user story with all required fields populated
- **Example Response**:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "project": "E-commerce Platform",
    "rol": "Customer",
    "goal": "reset my password",
    "reason": "I can access my account if I forget my credentials",
    "description": "As a customer, I want to be able to reset my password so that I can access my account if I forget my credentials.",
    "priority": "medium",
    "story_points": 3,
    "effort_hours": 4.0,
    "created_at": "2024-01-15T10:30:00"
}
```

#### 4. Generate Tasks from User Story
- **URL**: `POST /ai/user-stories/<user_story_id>/generate_tasks`
- **Description**: Generate 3-5 development tasks based on a user story
- **Request**: No body required, uses the user story ID from the URL
- **Response**: Returns an array of generated tasks
- **Example Response**:
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "title": "Implement password reset form",
        "description": "Create a password reset form with email input validation",
        "priority": "medium",
        "effort_hours": 2.0,
        "status": "pending",
        "assigned_to": "Frontend Developer",
        "category": "Frontend",
        "user_story_id": "550e8400-e29b-41d4-a716-446655440000",
        "risk_analysis": "Form validation complexity",
        "risk_mitigation": "Use established validation libraries"
    }
]
```

## 🎯 How to Use the Application

### 1. Access the Web Interface
1. Open your browser and go to `http://localhost:5000/user-stories`
2. You'll see the user stories dashboard

### 2. Generate a New User Story
1. Click the "Generate User Story with AI" button
2. Enter a natural language description of what you want to achieve
3. The AI will generate a complete user story with all required fields
4. The user story will be automatically saved to the database

### 3. Generate Tasks from a User Story
1. From the user stories list, click "View Tasks" for any user story
2. Click "Generate Tasks with AI" button
3. The AI will analyze the user story and generate 3-5 development tasks
4. All tasks will be automatically saved and linked to the user story

### 4. View and Manage Tasks
1. Navigate to any user story's tasks page
2. View all generated tasks with their details
3. Tasks include AI-generated risk analysis and mitigation strategies

## 🏗️ Architecture

The system follows Hexagonal Architecture principles:

### Domain Layer (`app/domain/`)
- **UserStory**: Core business entity with validation rules
- **Task**: Task entity with user story relationship
- **Enums**: Priority, Status, Category definitions

### Infrastructure Layer (`app/infrastructure/`)
- **Database**: MySQL with SQLAlchemy ORM
- **Models**: UserStoryORM and TaskORM with relationships
- **Managers**: UserStoryManager and TaskManager for data operations

### Application Layer (`app/application/`)
- **Services**: UserStoryService and TaskService orchestrate business logic
- **AI Service**: Azure OpenAI integration for content generation
- **Logging**: Token usage tracking and cost monitoring

### API Layer (`app/api/`)
- **Routes**: RESTful endpoints and web interface
- **Templates**: Jinja2 HTML templates for web views
- **Validation**: Pydantic models for request/response validation

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | MySQL connection string | Yes | `mysql+pymysql://user:password@localhost:3306/m4_entregable3` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes | `sk-...` |
| `FLASK_ENV` | Flask environment | No | `development` |
| `FLASK_DEBUG` | Flask debug mode | No | `1` |

### Database Schema
The system automatically creates the following tables:
- `user_stories`: Stores user story data
- `tasks`: Stores task data with foreign key to user stories

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_task_api.py
```

## 📊 Monitoring

The system includes token usage logging:
- Logs are stored in `logs/token_usage_YYYY-MM-DD.json`
- Tracks OpenAI API calls and token consumption
- Helps monitor AI service costs

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running: `docker-compose ps`
   - Check DATABASE_URL in `.env` file
   - Verify database credentials

2. **Azure OpenAI API Error**
   - Verify AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY
   - Check Azure OpenAI service status
   - Ensure API key has proper permissions

3. **Port Already in Use**
   - Change Flask port in `run.py`
   - Kill existing processes on port 5000

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export FLASK_DEBUG=1
python run.py
```

## 📝 API Testing

The project includes a comprehensive `api.rest` file with ready-to-use API examples for testing all user story endpoints.

### Using the API Examples
1. **Install REST Client Extension**: If using VS Code, install the "REST Client" extension
2. **Open api.rest**: Open the `api.rest` file in your editor
3. **Run Requests**: Click "Send Request" above any request to execute it
4. **Modify Variables**: Update the `@baseUrl` variable if your server runs on a different port

### Available Examples in api.rest
- **Generate User Story with AI**: Create user stories from natural language prompts
- **Generate Tasks from User Story**: Generate development tasks based on user stories
- **Web Interface Endpoints**: Access the HTML dashboard and task views
- **Multiple Use Cases**: Examples for e-commerce, payment processing, and order tracking

### Quick Test with curl
If you prefer using curl, here are some basic examples:

```bash
# Generate a user story
curl -X POST http://localhost:5000/ai/user-stories \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "As a user, I want to search for products so that I can find what I need quickly"
  }'

# Generate tasks from a user story (replace {user_story_id})
curl -X POST http://localhost:5000/ai/user-stories/{user_story_id}/generate_tasks

# Access the web interface
curl http://localhost:5000/user-stories
```

## 🔄 Development Workflow

1. **Start Development Environment**
   ```bash
   docker-compose up -d db
   source venv/bin/activate
   python run.py
   ```

2. **Make Changes**
   - Modify code in the `app/` directory
   - Flask will auto-reload in debug mode

3. **Test Changes**
   ```bash
   pytest
   ```

4. **Stop Environment**
   ```bash
   docker-compose down
   ```

## 📈 Features Overview

- ✅ **AI-Powered User Story Generation**: Create user stories from natural language
- ✅ **AI-Powered Task Generation**: Generate tasks from user stories
- ✅ **Web Interface**: User-friendly HTML interface
- ✅ **Database Integration**: MySQL with SQLAlchemy ORM
- ✅ **RESTful API**: Complete API for programmatic access
- ✅ **Validation**: Pydantic models with comprehensive validation
- ✅ **Testing**: pytest with coverage reporting
- ✅ **Monitoring**: Token usage tracking and logging
- ✅ **Docker Support**: Easy database setup with Docker Compose 