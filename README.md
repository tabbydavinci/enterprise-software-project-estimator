# Software Estimator

A full-stack software project estimation application built with FastAPI, PostgreSQL, Redis, Celery, and vanilla JavaScript.

The application estimates software development effort, development time, and project cost using Function Point Analysis and COCOMO-style effort estimation.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing with Argon2
- User-owned projects
- Project creation and management
- Function Point estimation
- Configurable entity complexity
- Environment complexity adjustment
- COCOMO project modes
- Programming-language adjustment
- Team-size and salary-based cost estimation
- Asynchronous estimation using Celery
- Redis-backed task queue
- PostgreSQL persistence
- Estimation status lifecycle:
  - `queued`
  - `processing`
  - `completed`
  - `failed`
- Project dashboard
- Estimation history
- Docker Compose development environment

## Architecture

```text
                        Browser
                           |
                           v
                 +-------------------+
                 |   Vanilla JS UI   |
                 |  HTML + CSS + JS  |
                 +---------+---------+
                           |
                           | HTTP / JSON
                           v
                 +-------------------+
                 |      FastAPI      |
                 |     Backend       |
                 +----+---------+----+
                      |         |
              SQL     |         | Celery task
                      |         |
                      v         v
              +-----------+  +-----------+
              | PostgreSQL|  |   Redis   |
              |           |  |           |
              | Users     |  | Task Queue|
              | Projects  |  +-----+-----+
              | Estimations|        |
              +-----------+         |
                                    v
                              +-----------+
                              |  Celery   |
                              |  Worker   |
                              +-----------+
                                    |
                                    v
                              Estimator Service
```

## Technology Stack

### Backend

* Python 3.14
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL
* Alembic
* Celery
* Redis
* PyJWT
* pwdlib / Argon2

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### Infrastructure

* Docker
* Docker Compose

## Estimation Flow

An estimation follows an asynchronous workflow.

```text
User submits estimation
        |
        v
Create estimation record
        |
        v
Status = queued
        |
        v
Celery task submitted
        |
        v
Worker picks up task
        |
        v
Status = processing
        |
        v
Run estimation algorithm
        |
        +----------------------+
        |                      |
        v                      v
   Calculation             Exception
        |                      |
        v                      v
Status = completed      Status = failed
        |
        v
Store results in PostgreSQL
```

The API does not wait for the estimator calculation to finish.

Instead, the frontend receives the estimation ID and polls the estimation endpoint until the worker finishes processing it.

## Authentication

Authentication uses JWT access tokens.

The authentication flow is:

```text
Register
   |
   v
Password hashed with Argon2
   |
   v
User stored in PostgreSQL
   |
   v
Login
   |
   v
JWT access token
   |
   v
Authorization: Bearer <token>
```

Protected project and estimation endpoints derive the current user from the JWT rather than trusting a user ID supplied by the client.

This means users can only access their own projects and estimations.

## Data Model

The primary database relationships are:

```text
User
 |
 | 1:N
 v
Project
 |
 | 1:N
 v
Estimation
```

### User

Stores:

* ID
* Email
* Password hash
* Created timestamp

### Project

Stores:

* ID
* Owner
* Name
* Description
* Created timestamp
* Updated timestamp

### Estimation

Stores:

* Project
* Function Point inputs
* Complexity information
* Environment complexity
* Project mode
* Programming language
* Salary
* Team size
* UFP
* TCF
* Function Points
* Effort
* Development time
* Cost
* Processing status
* Celery task ID
* Processing timestamps

## API

### Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Projects

```text
GET  /projects
POST /projects
GET  /projects/{project_id}
```

### Estimations

```text
POST /projects/{project_id}/estimations
GET  /projects/{project_id}/estimations
GET  /estimations/{estimation_id}
```

## Running Locally

The application is designed to run with Docker Compose.

### Start the complete stack

```bash
docker compose up -d --build
```

### Check service status

```bash
docker compose ps
```

The services are:

```text
backend
worker
postgres
redis
```

The FastAPI application is exposed on:

```text
http://localhost:8000
```

The frontend can be served locally on port `5500`.

For example:

```bash
python -m http.server 5500 -d frontend
```

Then open:

```text
http://localhost:5500
```

## Environment Configuration

Sensitive configuration is stored outside the source code.

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

The JWT secret is passed to the backend through Docker Compose.

The application intentionally fails to start when `SECRET_KEY` is missing rather than silently using a development secret.

## Database Migrations

Alembic is used for database schema migrations.

### Create a migration

```bash
alembic revision --autogenerate -m "describe change"
```

### Apply migrations

```bash
alembic upgrade head
```

## Project Structure

```text
.
├── backend
│   ├── alembic
│   ├── database
│   ├── models
│   ├── services
│   ├── workers
│   ├── estimator.py
│   ├── main.py
│   ├── auth.py
│   └── redis_client.py
│
├── frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── compose.yml
├── alembic.ini
├── .env
└── README.md
```

## Engineering Decisions

### PostgreSQL as the source of truth

Estimation state and results are stored in PostgreSQL rather than relying on Celery's result backend.

This allows the application to treat estimation records as persistent domain data instead of transient task results.

### Celery for asynchronous processing

Estimation calculations are executed by a dedicated worker so that API requests do not block while processing.

This also establishes a foundation for more expensive estimation workloads in the future.

### Redis as the broker

Redis is used as the Celery message broker to decouple API requests from background workers.

### JWT authentication

The backend uses stateless JWT access tokens for authenticated requests.

Project and estimation ownership is enforced server-side by associating resources with the authenticated user.

### Docker Compose

The application dependencies are containerized so that PostgreSQL, Redis, the API, and the worker can be started as one development environment.

## Current Scope

The application currently focuses on project estimation and asynchronous processing.

Potential future extensions include:

* Project editing and deletion
* Estimation comparison
* Estimation versioning
* Richer estimation analytics
* User profile management
* Production deployment
* Automated test coverage
* More advanced task retry and monitoring
