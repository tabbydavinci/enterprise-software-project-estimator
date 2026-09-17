from sqlalchemy import text

from database import database

with database.engine.connect() as connection:
    result = connection.execute(
        text("SELECT version();")
    )
    print(result.scalar())
