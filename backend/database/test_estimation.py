from datetime import UTC, datetime

from database.database import SessionLocal
from models.user import User
from models.project import Project
from models.estimation import Estimation


test_data = {
    "inputs": {
        "count": 5,
        "complexities": [
            "simple",
            "simple",
            "average",
            "complex",
            "simple",
        ],
    },
    "outputs": {
        "count": 3,
        "complexities": [
            "average",
            "complex",
            "simple",
        ],
    },
    "inquiries": {
        "count": 2,
        "complexities": [
            "simple",
            "average",
        ],
    },
    "files": {
        "count": 4,
        "complexities": [
            "average",
            "average",
            "complex",
            "simple",
        ],
    },
    "interfaces": {
        "count": 2,
        "complexities": [
            "simple",
            "average",
        ],
    }
}


session = SessionLocal()

try:
    # user = User(
    #     email="test@example.com",
    #     password_hash="dummy_hash",
    #     created_at=datetime.now(UTC),
    # )

    # session.add(user)
    # session.commit()

    # project = Project(
    #     user_id=user.id,
    #     name="Estimation Test Project",
    #     description="Testing estimation relationship",
    #     created_at=datetime.now(UTC),
    #     updated_at=datetime.now(UTC),
    # )

    # session.add(project)
    # session.commit()

    estimation = Estimation(
        project_id=13,

        inputs=test_data["inputs"],
        outputs=test_data["outputs"],
        inquiries=test_data["inquiries"],
        files=test_data["files"],
        interfaces=test_data["interfaces"],

        environment_complexity=15,
        project_mode="organic",
        language="python",
        salary_per_month=100000,
        team_size=5,

        ufp=96,
        tcf=0.8,
        fp=76.80000000000001,
        effort_person_months=3.766,
        time_months=4.138,
        time_formatted="4 months 5 days",
        cost_rupees=2069000,

        status="queued",
        celery_task_id=None,
        created_at=datetime.now(UTC),
        started_at=None,
        completed_at=None
    )

    session.add(estimation)
    session.commit()

    print("Created estimation:", estimation.id)

    print("Estimation's project:", estimation.project.name)

    print(
        "Project's estimations:",
        [item.id for item in project.estimations],
    )

    # session.delete(estimation)
    # session.delete(project)
    # session.delete(user)
    # session.commit()

finally:
    session.close()