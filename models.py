from sqlalchemy import Boolean, Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from config import Tashkent_tz
from database import Base

class UsersTable(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String(36))
    last_name = Column(String(36))
    phone_num = Column(String(36), unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String(24))

    created_at = Column(DATETIME, nullable=False, default=datetime.now(tz=Tashkent_tz))
    updated_at = Column(DATETIME, onupdate=datetime.now(tz=Tashkent_tz))

    assignments = relationship("AssignmentTable", back_populates="owner")

    @validates('role')
    def validate_role(self, key, value):
        valid_roles = ["PM", "developer", "employee"]
        if value not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return value

class AssignmentTable(Base):
    __tablename__ = "Assignment"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    description = Column(String, index=True)
    priority = Column(String(24))
    is_complete = Column(Boolean, default=False)
    created_at = Column(DATETIME, nullable=False, default=datetime.now(tz=Tashkent_tz))
    updated_at = Column(DATETIME, onupdate=datetime.now(tz=Tashkent_tz))

    owner_id = Column(Integer, ForeignKey("User.id"))
    owner = relationship("UsersTable", back_populates="assignments")
