from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from mangum import Mangum

from app.api.api_v3.api import router as router_v3
from app.api.api_v2.api import router as router_v2

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


# API Endpoints
app.include_router(router_v2, prefix="/api/v2")
app.include_router(router_v3, prefix="/api/v3")


handler = Mangum(app)
