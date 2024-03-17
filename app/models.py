from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import random
from .database import Base

#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine, text
class Submission(Base):
    __tablename__ = 'submission'
    
    submission_id = Column(Integer, primary_key=True, index=True)
    time_submitted = Column(DateTime(timezone=True), server_default=func.now())

    result = relationship("Result", back_populates="submission")

class Result(Base):
    __tablename__ = 'result'

    result_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submission.submission_id'))
    url_id = Column(Integer, ForeignKey('url.url_id'))
    submitted_url = Column(String(2000))
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    submission = relationship("Submission", back_populates="result")
    url = relationship("Url", back_populates="result")


class Url(Base):
    __tablename__ = 'url'
    url_id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey('feature.feature_id'))
    final_url = Column(String(2000))
    phish_prob = Column(Float)
    is_phishing = Column(Boolean)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    
    feature = relationship("Feature", back_populates="url")
    result = relationship("Result", back_populates="url")
    #feature = relationship("Feature", uselist=False, back_populates="url")

class Feature(Base):
    __tablename__ = 'feature'
    feature_id = Column(Integer, primary_key=True, index=True)
    domainlength = Column(Integer) #1
    www = Column(Integer) # 2
    subdomain = Column(Integer) # 3
    https = Column(Integer) # 4
    http = Column(Integer) # 5
    short_url = Column(Integer) # 6
    ip = Column(Integer) # 7
    at_count = Column(Integer) # 8
    dash_count = Column(Integer) # 9
    equal_count = Column(Integer) # 10
    dot_count = Column(Integer) # 11
    underscore_count = Column(Integer) # 12
    slash_count = Column(Integer) # 13
    digit_count = Column(Integer) # 14
    log_contain = Column(Integer) # 15
    pay_contain = Column(Integer) # 16
    web_contain = Column(Integer) #17
    cmd_contain = Column(Integer) # 18
    account_contain = Column(Integer) # 19
    pc_emptylink = Column(Float) # 20
    pc_extlink = Column(Float) # 21
    pc_requrl = Column(Float) # 22
    zerolink = Column(Integer) # 23
    ext_favicon = Column(Integer) # 24
    submit_to_email = Column(Integer) # 25
    sfh = Column(Integer) # 26
    redirection = Column(Integer) # 27
    domainage = Column(Integer) # 28
    domainend = Column(Integer) # 29 
    
    url = relationship("Url", back_populates="feature")

