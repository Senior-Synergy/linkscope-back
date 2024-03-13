from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

#from sqlalchemy.orm import Session
from . import  models
from .database import engine
from app.router import url


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url.router)

# Use this to update requirements:
# pip freeze > requirements.txt

# Use this to start:
# uvicorn app.main:app --reload
