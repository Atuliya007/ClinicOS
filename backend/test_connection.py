from sqlalchemy import text

from app.db.session import engine
from app.db.config import settings

print(settings.DATABASE_URL)
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("✅ Connected successfully!\n")

        for row in result:
            print(row[0])

except Exception as e:
    print("❌ Connection failed!")
    print(e)