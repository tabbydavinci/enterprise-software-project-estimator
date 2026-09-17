from datetime import UTC, datetime

from workers.celery_app import celery_app

from database.database import SessionLocal
from models.estimation import Estimation
from services.estimator_service import run_estimator


@celery_app.task(bind=True)
def process_estimation(self, estimation_id: int):
    db = SessionLocal()

    try:
        estimation = db.get(Estimation, estimation_id)

        if estimation is None:
            raise ValueError(
                f"Estimation {estimation_id} was not found."
            )

        estimation.status = "processing"
        estimation.started_at = datetime.now(UTC)
        estimation.celery_task_id = self.request.id

        db.commit()

        estimator_data = {
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
        }

        results = run_estimator(estimator_data)

        estimation.ufp = results["ufp"]
        estimation.tcf = results["tcf"]
        estimation.fp = results["fp"]
        estimation.effort_person_months = results[
            "effort_person_months"
        ]
        estimation.time_months = results["time_months"]
        estimation.time_formatted = results["time_formatted"]
        estimation.cost_rupees = results["cost_rupees"]

        estimation.status = "completed"
        estimation.completed_at = datetime.now(UTC)

        db.commit()

        return {
            "estimation_id": estimation.id,
            "status": estimation.status,
        }

    except Exception:
        if "estimation" in locals() and estimation is not None:
            estimation.status = "failed"
            db.commit()

        raise

    finally:
        db.close()