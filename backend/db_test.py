from sqlalchemy import text
from db import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT version()"))
    print(result.scalar())

print("database successfully connected")