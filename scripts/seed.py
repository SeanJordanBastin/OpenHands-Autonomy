from app.db import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        db.execute(text("CREATE TABLE IF NOT EXISTS dummy (id INTEGER PRIMARY KEY, name TEXT)"))
        db.execute(text("INSERT INTO dummy (name) VALUES ('Test 1'), ('Test 2')"))
        db.commit()
        print("✅ Seeded dummy data.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
