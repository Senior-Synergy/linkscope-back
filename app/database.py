# Database Initializtion
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base #for mapping
from sqlalchemy.orm import sessionmaker


import json
with open('config.json') as f:
    config = json.load(f)

HOSTNAME = config['hostname']
USER = config['user']
PASSWORD = config['password']
DB_NAME = 'urldata'

url = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOSTNAME}:3306/{DB_NAME}'
#url = 'mysql://admin:seniorsynergy88@url-1.crfthzhiprmr.ap-southeast-2.rds.amazonaws.com:3306/{DB_NAME}'
#engine = create_engine(url,connect_args={"check_same_thread": False})
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

