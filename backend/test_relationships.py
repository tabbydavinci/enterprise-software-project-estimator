from sqlalchemy import inspect

from models.user import User
from models.project import Project
from models.estimation import Estimation

user_mapper = inspect(User)
project_mapper = inspect(Project)
estimation_mapper = inspect(Estimation)

print("User relationships:")
print(list(user_mapper.relationships.keys()))

print("Project relationships:")
print(list(project_mapper.relationships.keys()))

print("Estimation relationships:")
print(list(estimation_mapper.relationships.keys()))