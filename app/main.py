from fastapi import FastAPI
from app import models
from app.database import engine
from mangum import Mangum

from app.api import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}


# API Endpoints
app.include_router(api.router, prefix="/api/v3")


handler = Mangum(app)
