from fastapi import FastAPI

app = FastAPI()

from app.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@app.get("/health/db")
def db_health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "DB connected ✅"}
    except:
        return {"status": "❌ DB connection failed"}

