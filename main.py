# imports
from fastapi import FastAPI
from database import engine
import models
import routers.auth as auth_router
import routers.assignments as assignment_router

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Todo Project")
app.include_router(auth_router.router)
app.include_router(assignment_router.router)
