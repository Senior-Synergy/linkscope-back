from fastapi import FastAPI
from app import models
from app.database import engine
from mangum import Mangum

from app.api.api_v3.api import router as router_v3

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}


# API Endpoints
app.include_router(router_v3, prefix="/api/v3")


handler = Mangum(app)
