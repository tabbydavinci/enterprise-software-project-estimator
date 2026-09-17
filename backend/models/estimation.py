from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Estimation(Base):
    __tablename__ = "estimations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    inputs: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    outputs: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    inquiries: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    files: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    interfaces: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    environment_complexity: Mapped[int] = mapped_column(
        nullable=False,
    )

    project_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    salary_per_month: Mapped[int] = mapped_column(
        nullable=False,
    )

    team_size: Mapped[int] = mapped_column(
        nullable=False,
    )

    ufp: Mapped[int] = mapped_column(
        nullable=False,
    )

    tcf: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    fp: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    effort_person_months: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    time_months: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    time_formatted: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cost_rupees: Mapped[int] = mapped_column(
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    celery_task_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    project: Mapped["Project"] = relationship(
        back_populates="estimations"
    )