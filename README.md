Yes — update the README before submitting. Your current README is now outdated because it says SQLite, while A3 uses PostgreSQL + Docker Compose.
# Task API — CRUD + PostgreSQL + Docker (BE-04 / W3 A3)

A small REST API for managing a to-do list, built with **Python** and **FastAPI**.

This version replaces the previous SQLite/in-memory storage with **PostgreSQL running in Docker**. The API and service layer remain unchanged while the repository layer is switched to PostgreSQL, demonstrating the storage-layer separation from the previous assignment.

Built as part of the FlyRank Internship — Backend Track.

## Assignment

**A3 — Containerize your stack**

- Postgres runs in Docker
- FastAPI application runs in Docker
- PostgreSQL data persists through a Docker volume
- Database connection is configured through `.env`
- `.env` is gitignored
- `.env.example` is committed
- App and database start together with `docker compose up`
- PostgreSQL repository replaces the previous storage implementation
- Persistence was tested across container/app restarts

## Architecture

The application is separated into layers:

```text
FastAPI routes
      ↓
Service / application logic
      ↓
PostgreSQL repository
      ↓
PostgreSQL


The important part of this assignment is that the routes and service logic did not need to change when storage was switched to PostgreSQL. The repository implementation is responsible for database access.

Project structure
crud-api/
├── main.py
├── repository.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
├── README.md
└── screenshots/

How to run
Requirements
Docker Desktop
Git

No local Python installation is required to run the containerized stack.

1. Clone the repository
git clone https://github.com/prathamesh-shirdhankar/flyrankai-crud-w2.git
cd flyrankai-crud-w2

2. Create .env

Copy .env.example to .env:

copy .env.example .env


The .env file contains the PostgreSQL connection configuration and is not committed to Git.

3. Start the application
docker compose up --build


The command starts both:

FastAPI application
PostgreSQL database

The API runs at:

http://localhost:8000


Interactive Swagger documentation:

http://localhost:8000/docs

Endpoints
Method	Path	Description	Success	Errors
GET	/	API info	200	—
GET	/health	Health check	200	—
GET	/tasks	List all tasks	200	—
GET	/tasks/{id}	Get a single task	200	404
POST	/tasks	Create a new task	201	400
PUT	/tasks/{id}	Update a task's title and/or done	200	400, 404
DELETE	/tasks/{id}	Delete a task	204	404
Task object
{
  "id": 1,
  "title": "Buy milk",
  "done": false
}

Database

PostgreSQL is run as a Docker service using the official PostgreSQL image.

The database uses a named Docker volume so that PostgreSQL data survives container restarts.

The application connects to PostgreSQL using the Docker Compose service name:

db


The connection string is supplied through the environment rather than hard-coded into the application.

Database initialization

On first startup, PostgreSQL initializes the database and creates the configured database/user.

The application repository creates the tasks table if it does not already exist and seeds example tasks when the table is empty.

PostgreSQL repository

The previous storage implementation was replaced by a PostgreSQL repository in:

repository.py


The FastAPI routes and application/service behavior remain unchanged.

This demonstrates the intended layered architecture: changing the storage backend does not require rewriting the API routes.

Persistence test

Persistence was verified using the following process:

Started the complete stack:
docker compose up --build


Created tasks through the API/Swagger UI.

Confirmed that the created tasks were returned by:

GET /tasks

Stopped the application and database containers:
docker compose down

Started the stack again:
docker compose up

Called:
GET /tasks

The previously created tasks were still present.

This confirmed that PostgreSQL data was persisted through the Docker volume rather than existing only inside the running container.

Note: docker compose down -v removes the named database volume and therefore intentionally deletes the persisted database data. It was used during development when resetting the database.

Docker Compose

The complete stack is started with:

docker compose up


For a clean rebuild:

docker compose up --build


To stop the stack:

docker compose down

Example — curl
GET /tasks/1


Example response:

{
  "id": 1,
  "title": "Buy milk",
  "done": false
}

Swagger UI

Interactive API documentation is available at:

http://localhost:8000/docs


The complete CRUD cycle can be tested through Swagger UI using Try it out.

Example SQL

The PostgreSQL repository uses parameterized SQL queries rather than string concatenation.

Example:

SELECT * FROM tasks WHERE done = %s;


Values are passed separately to the database driver.

A3 outcome

This assignment demonstrates:

PostgreSQL running in Docker
Persistent database storage using a Docker volume
Environment-based database configuration
FastAPI + PostgreSQL integration
Repository-layer separation
Docker Compose orchestration
Persistence across container restarts
A complete containerized local development stack

