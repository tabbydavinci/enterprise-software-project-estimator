from datetime import UTC, datetime

from database.database import SessionLocal
from models.user import User
from models.project import Project


session = SessionLocal()

try:
    user = User(
        email="project_test1@example.com",
        password_hash="dummy_hash",
        created_at=datetime.now(UTC),
    )

    session.add(user)
    session.commit()

    project = Project(
        user_id=user.id,
        name="Test Project",
        description="Testing project relationship",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    session.add(project)
    session.commit()

    print("Created project:", project.id, project.name)
    print("Project's user:", project.user.email)

    session.delete(project)
    session.delete(user)
    session.commit()

finally:
    session.close()