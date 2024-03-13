from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from sqlalchemy.orm import Session
from . import  models
from .database import engine
from app.router import url


models.Base.metadata.create_all(bind=engine)
<<<<<<< Updated upstream
from app.api.api_v1.api import router as api_router
=======
feature_names = [
            'domainlength', 'www', 'subdomain', 'https', 'http', 'short_url', 'ip',
            '@', '-', '=', '.', '_', '/', 'digit', 'log', 'pay', 'web', 'cmd', 'account',
            'pcemptylinks', 'pcextlinks', 'pcrequrl', 'zerolink', 'extfavicon', 'submit2email',
            'sfh', 'redirection', 'domainage', 'domainend'
        ]
num_features = [
            'domainlength', '@', '-', '=', '.', '_', '/', 'digit',
            'pcemptylinks', 'pcextlinks', 'pcrequrl'
        ]
cat_features = [
            'www', 'subdomain', 'https', 'http', 'short_url', 'ip', 'log', 'pay',
            'web', 'cmd', 'account', 'zerolink', 'extfavicon', 'submit2email',
            'sfh', 'redirection', 'domainage', 'domainend'
        ]

def replace_minus_one(X):
    return X.replace(-1, np.nan)

def cast_to_float(X):
    return X.astype(float)

def cast_to_int(X):
    return X.astype(int)
>>>>>>> Stashed changes

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
