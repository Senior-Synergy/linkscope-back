from fastapi import FastAPI
from app.router import router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, From Backend!"}


# Import and include additional routers as needed
app.include_router(router)
