from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

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


@app.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}


app.include_router(url.router)


# Use this to update requirements:
# pip freeze > requirements.txt

# Use this to start:
# uvicorn app.main:app --reload
