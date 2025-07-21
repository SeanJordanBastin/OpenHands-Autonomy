from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.project import Project, ProjectCreate

router = APIRouter()

@router.get("/projects")
def read_projects(db: Session = Depends(get_db)):
    return [{"id": 1, "name": "Sample Project"}]
