from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes.shortener import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router, prefix = "/api")