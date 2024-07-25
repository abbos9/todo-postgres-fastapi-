from sqlalchemy.orm import Session
import models, schemas

def get_assignment(db:Session):
    return db.query(models.AssignmentTable).all()

def create_assignment(db: Session, assignment: schemas.CrudAssignmentSchema, owner_id: int):
    db_assignment = models.AssignmentTable(**assignment.dict(), owner_id=owner_id)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment