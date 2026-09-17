from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from fastapi import Depends
from database.database import SessionLocal
from models.project import Project
from models.estimation import Estimation
from models.user import User
from datetime import UTC, datetime

from workers.tasks import process_estimation

from fastapi.security import OAuth2PasswordRequestForm
from auth import (
    create_access_token,
    get_current_user_id,
    hash_password,
    verify_password,
)


app = FastAPI(
    title="Enterprise Software Project Estimator",
    version="1.0.0"
)

# CORS resolution
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    email: str
    password: str = Field(
        min_length=8,
        max_length=128,
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class EntityModel(BaseModel):
    count: int
    complexities: list[str]

class EstimationCreate(BaseModel):
    inputs: EntityModel
    outputs: EntityModel
    inquiries: EntityModel
    files: EntityModel
    interfaces: EntityModel

    environment_complexity: int
    project_mode: str
    language: str
    salary_per_month: int
    team_size: int

# debug
# @app.get("/db-test")
# def db_test(db=Depends(get_db)):
#     return {
#         "database": "session created successfully"
#     }

@app.get("/")
def root():
    return {
        "message": "Software Estimator API is running!"
    }

# auth register
@app.post("/auth/register")
def register(
    data: UserCreate,
    db=Depends(get_db)
):
    email = data.email.strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    user= User(
        email=email,
        password_hash=hash_password(data.password),
        created_at=datetime.now(UTC)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email
    }

# auth login
@app.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db)
):
    email = form_data.username.strip().lower()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if (
        user is None
        or not verify_password(
            form_data.password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# get user
@app.get("/auth/me")
def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db)
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

# projects
@app.post("/projects")
def create_project(
    data: ProjectCreate,
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db)
):
    project = Project(
        user_id=user_id,
        name=data.name,
        description=data.description,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }

# list of projects under one user - needs auth
@app.get("/projects")
def get_projects(
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db)
):
    projects = (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .order_by(Project.created_at.desc())
        .all()
    )

    return [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
        }
        for project in projects
    ]

# individual project - needs auth
@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.user_id == user_id,
        )
        .first()
    )

    if project is None:
        return {
            "error": "Project not found"
        }

    return {
        "id": project.id,
        "user_id": project.user_id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }

# post estimations to one project belong to a user
@app.post("/projects/{project_id}/estimations")
def create_estimation(
    project_id: int,
    data: EstimationCreate,
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.user_id == user_id
        )
        .first()
    )

    if project is None:
        return {
            "error": "Project not found"
        }

    estimation = Estimation(
        project_id=project.id,

        inputs=data.inputs.model_dump(),
        outputs=data.outputs.model_dump(),
        inquiries=data.inquiries.model_dump(),
        files=data.files.model_dump(),
        interfaces=data.interfaces.model_dump(),

        environment_complexity=data.environment_complexity,
        project_mode=data.project_mode,
        language=data.language,
        salary_per_month=data.salary_per_month,
        team_size=data.team_size,

        ufp=0,
        tcf=0,
        fp=0,
        effort_person_months=0,
        time_months=0,
        time_formatted="",
        cost_rupees=0,

        status="queued",
        celery_task_id=None,
        created_at=datetime.now(UTC),
        started_at=None,
        completed_at=None,
    )

    db.add(estimation)
    db.commit()
    db.refresh(estimation)

    # debug
    # print(
    #     "CELERY DEBUG:",
    #     process_estimation.app.conf.broker_url,
    #     process_estimation.app.conf.task_default_queue,
    #     process_estimation.app.conf.task_always_eager,
    # )

    task = process_estimation.delay(estimation.id)

    # debug
    # print("CELERY TASK CREATED:", task.id)

    estimation.celery_task_id = task.id

    db.commit()

    return {
        "id": estimation.id,
        "project_id": estimation.project_id,
        "status": estimation.status
    }

# get - needs auth
@app.get("/projects/{project_id}/estimations")
def get_project_estimations(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.user_id == user_id,
        )
        .first()
    )

    if project is None:
        return {
            "error": "Project not found"
        }

    return [
        {
            "id": estimation.id,
            "project_id": estimation.project_id,

            "inputs": estimation.inputs,
            "outputs": estimation.outputs,
            "inquiries": estimation.inquiries,
            "files": estimation.files,
            "interfaces": estimation.interfaces,

            "environment_complexity": estimation.environment_complexity,
            "project_mode": estimation.project_mode,
            "language": estimation.language,
            "salary_per_month": estimation.salary_per_month,
            "team_size": estimation.team_size,

            "ufp": estimation.ufp,
            "tcf": estimation.tcf,
            "fp": estimation.fp,
            "effort_person_months": estimation.effort_person_months,
            "time_months": estimation.time_months,
            "time_formatted": estimation.time_formatted,
            "cost_rupees": estimation.cost_rupees,

            "status": estimation.status,
            "celery_task_id": estimation.celery_task_id,
            "created_at": estimation.created_at,
            "started_at": estimation.started_at,
            "completed_at": estimation.completed_at
        }
        for estimation in project.estimations
    ]

# get individual estimation
@app.get("/estimations/{estimation_id}")
def get_estimation(
    estimation_id: int,
    user_id: int = Depends(get_current_user_id),
    db=Depends(get_db)
):
    estimation = (
        db.query(Estimation)
        .join(Project)
        .filter(
            Estimation.id == estimation_id,
            Project.user_id == user_id,
        )
        .first()
    )

    if estimation is None:
            return {
                "error": "Estimation not found"
            }

    return {
        "id": estimation.id,
        "project_id": estimation.project_id,

        "inputs": estimation.inputs,
        "outputs": estimation.outputs,
        "inquiries": estimation.inquiries,
        "files": estimation.files,
        "interfaces": estimation.interfaces,

        "environment_complexity": estimation.environment_complexity,
        "project_mode": estimation.project_mode,
        "language": estimation.language,
        "salary_per_month": estimation.salary_per_month,
        "team_size": estimation.team_size,

        "ufp": estimation.ufp,
        "tcf": estimation.tcf,
        "fp": estimation.fp,
        "effort_person_months": estimation.effort_person_months,
        "time_months": estimation.time_months,
        "time_formatted": estimation.time_formatted,
        "cost_rupees": estimation.cost_rupees,

        "status": estimation.status,
        "celery_task_id": estimation.celery_task_id,
        "created_at": estimation.created_at,
        "started_at": estimation.started_at,
        "completed_at": estimation.completed_at
    }
