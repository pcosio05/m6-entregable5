# Task Management System (Python Flask)

## Introduction
This is a Python application built with Flask that provides a task management system. It follows clean architecture principles and includes AI-powered features for generating user stories and tasks. The app is designed for easy deployment and reproducibility using Docker.

## Docker Packaging
The application is containerized using Docker. The Dockerfile builds a production-ready image with all dependencies installed, and uses Gunicorn as the WSGI server for optimal performance. Multi-architecture images (for both amd64 and arm64) are supported.

## CI/CD Pipeline Configuration
A GitHub Actions workflow is set up to:
1. Run tests on every push or pull request to the `main` branch.
2. If tests pass, build the Docker image for both `linux/amd64` and `linux/arm64` platforms.
3. Push the built image to Docker Hub with a tag based on the version in `pyproject.toml`.

## Container Image Storage
The Docker image is stored on Docker Hub under the repository:
```
docker.io/pcosio05/m5-entregable4:<version>
```
Replace `<version>` with the version specified in `pyproject.toml`.

## Running the App with Docker Compose

Docker compose stack contains two services:
- mysql service
- python flask application  

Then, these are the steps to bootstrap the application:

1. Ensure you have a `.env` file in the project root with the required variables. Database url value is already prepared for connecting to the Mysql server that is included in the docker-compose stack:
    ```
    DATABASE_URL=mysql+pymysql://user:password@mysql:3306/entregable4
    AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
    AZURE_OPENAI_API_KEY=your-azure-openai-api-key
    ```
2. Start the services:
    ```bash
    docker-compose up -d
    ```
3. The app will be available at [http://localhost:5000](http://localhost:5000)

4. Before testing the app, the containers should be up and running

```sh
$ docker ps -a
CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS          PORTS                               NAMES
651003c5426e   mysql:8.0                       "docker-entrypoint.s…"   10 minutes ago   Up 10 minutes   0.0.0.0:3306->3306/tcp, 33060/tcp   m5_entregable4_pablo_cosio_molleda-mysql-1
d0bc555415f1   pcosio05/m5-entregable4:0.0.3   "gunicorn --bind 0.0…"   10 minutes ago   Up 10 minutes   0.0.0.0:5000->5000/tcp              m5_entregable4_pablo_cosio_molleda-m5-entregable4-1
```

## Basic Tests to Ensure Functionality
### 1. Access the Web Interface
1. Open your browser and go to `http://localhost:5000/user-stories`
2. You'll see the user stories dashboard

![Welcome](docs/screen-0.png)

### 2. Generate a New User Story
1. Click the "Generate User Story with AI" button
2. Enter a natural language description of what you want to achieve
3. The AI will generate a complete user story with all required fields
4. The user story will be automatically saved to the database

![create user story](docs/screen-1.png)
![user story created](docs/screen-2.png)

### 3. Generate Tasks from a User Story
1. From the user stories list, click "View Tasks" for any user story
2. Click "Generate Tasks with AI" button
3. The AI will analyze the user story and generate 3-5 development tasks
4. All tasks will be automatically saved and linked to the user story

![generate tasks](docs/screen-3.png)

### 4. View and Manage Tasks
1. Navigate to any user story's tasks page
2. View all generated tasks with their details
3. Tasks include AI-generated risk analysis and mitigation strategies

![view tasks](docs/screen-4.png)

For more details on endpoints and features, see the source code and comments in the `app/` directory. 