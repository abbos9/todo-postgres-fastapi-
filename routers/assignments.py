

from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from config import Tashkent_tz
from database import SessionLocal
from models import AssignmentTable, UsersTable
import models, schemas, crud
from sqlalchemy.orm import Session
from utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/assignments",
    tags=['Assignments'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_depency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=list[schemas.ResponseAssignmentSchema], status_code=status.HTTP_200_OK)
async def get_assignments(db: Session = Depends(get_db)):
    db_assignments = crud.get_assignment(db=db)
    return db_assignments

@router.get('/{assignment_id}', status_code=status.HTTP_200_OK)
async def get_assignment(
        assignment_id: int = Path(gt=0),
        session: Session = Depends(db_dependency)):
    assignment = session.query(models.AssignmentTable).filter(
        models.AssignmentTable.id == assignment_id).first()
    if assignment is not None:
        return assignment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found !")


@router.post("/", response_model=schemas.CrudAssignmentSchema,status_code=status.HTTP_201_CREATED)
async def create_assignment(assignment:schemas.CrudAssignmentSchema,db:db_dependency,current_user: Annotated[UsersTable, Depends(get_current_user)]):
    if current_user.role != "PM":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")
    return crud.create_assignment(db=db, assignment=assignment, owner_id=current_user.id)


@router.delete("/{assignment_id}", response_model=schemas.CrudAssignmentSchema, status_code=status.HTTP_404_NOT_FOUND)
def delete_assignment(assignment_id: int, db: db_dependency,current_user: Annotated[UsersTable, Depends(get_current_user)]):
    if current_user.role != "PM":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")
    db_assignment = db.query(AssignmentTable).filter(AssignmentTable.id == assignment_id).first()
    print(db_assignment)
    if db_assignment:
        db.delete(db_assignment)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Assignment successfully delete"}


@router.put("/{assignment_id}", response_model=schemas.UpdateAssignmentSchema,status_code=status.HTTP_201_CREATED)
def update_assignment(assignment_id: int, assignment: schemas.UpdateAssignmentSchema, db: db_dependency,current_user: Annotated[UsersTable, Depends(get_current_user)]):
    if current_user.role not in ["employee", "developer", "PM"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action.")
    db_assignment = db.query(AssignmentTable).filter(AssignmentTable.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Item not found")
    db_assignment.title = assignment.title
    db_assignment.description = assignment.description
    db_assignment.priority = assignment.priority
    db_assignment.is_complete = assignment.is_complete
    db_assignment.updated_at = datetime.now(tz=Tashkent_tz)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
