from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from sqlalchemy.orm import Session
from . import  models
from .database import engine
from app.router import url


models.Base.metadata.create_all(bind=engine)
from app.api.api_v1.api import router as api_router

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


app.include_router(api_router, prefix="/api/v1")

# Use this to update requirements:
# pip freeze > requirements.txt

# Use this to start:
# uvicorn app.main:app --reload
