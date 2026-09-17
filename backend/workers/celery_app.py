import os
from celery import Celery


celery_app = Celery(
    "software_estimator",
    broker=(
        f"redis://{os.getenv('REDIS_HOST', 'localhost')}:"
        f"{os.getenv('REDIS_PORT', '6379')}/0"
    ),
    include=["workers.tasks"],
)