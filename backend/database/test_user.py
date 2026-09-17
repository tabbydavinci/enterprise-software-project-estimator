from datetime import UTC, datetime

from database.database import SessionLocal
from models.user import User


session = SessionLocal()

try:
    user = User(
        email="test@example.com",
        password_hash="dummy_hash",
        created_at=datetime.now(UTC)
    )

    session.add(user)
    session.commit()

    print("Created user:", user.id, user.email)

    found_user = session.query(User).filter_by(
        email=user.email,
    ).first()

    print("Found user:", found_user.id, found_user.email)

    # session.delete(found_user)
    # session.commit()

finally:
    session.close()