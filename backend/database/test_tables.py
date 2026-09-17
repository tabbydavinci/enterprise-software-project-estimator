from sqlalchemy import text

from database import database


with database.engine.connect() as connection:
    result = connection.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
        )
    )

    for row in result:
        print(row[0])