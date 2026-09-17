from models.base import Base
import models.user
import models.project
import models.estimation

print("Tables known to SQLAlchemy:")
print(Base.metadata.tables.keys())