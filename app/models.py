from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from .database import Base

#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine, text
class Submission(Base):
    __tablename__ = 'submission'
    
    submission_id = Column(Integer, primary_key=True, index=True)
    datetime_submitted = Column(DateTime(timezone=True), server_default=func.now())

    result = relationship("Result", back_populates="submission")



class Url(Base):
    __tablename__ = 'url'
    url_id = Column(Integer, primary_key=True, index=True)
    final_url = Column(String(2000))

    hostname = Column(String(200))
    domain = Column(String(200))
    registrar = Column(String(200)) #
    ip_address = Column(String(200)) #
    subdomains = Column(String(200))
    scheme = Column(String(200))
      # extra domain infomation
    creation_date = Column(DateTime(timezone=True))
    expiration_date = Column(DateTime(timezone=True))            
    domainage = Column(Integer)
    domainend = Column(Integer)
    city = Column(String(100)) 
    state = Column(String(100)) 
    country =Column(String(100))
    google_safe_browsing = Column(Integer)
    updated_date =  Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())       
    result = relationship("Result", back_populates="url")
    #feature = relationship("Feature", uselist=False, back_populates="url")

class Feature(Base):
    __tablename__ = 'feature'
    feature_id = Column(Integer, primary_key=True, index=True)
    domainlength = Column(Integer) #1
    www = Column(Integer) # 2
    https = Column(Integer) # 3    
    short_url = Column(Integer) # 4
    ip = Column(Integer) # 5    
    dash_count = Column(Integer) # 6
    equal_count = Column(Integer) # 7
    dot_count = Column(Integer) # 8
    underscore_count = Column(Integer) # 9
    slash_count = Column(Integer) # 10
    digit_count = Column(Integer) # 11  
    pc_emptylink = Column(Float) # 12
    pc_extlink = Column(Float) # 13
    pc_requrl = Column(Float) # 14
    zerolink = Column(Integer) # 15
    ext_favicon = Column(Integer) # 16    
    sfh = Column(Integer) # 17
    redirection = Column(Integer) # 18 
    domainend = Column(Integer) # 19 

    shortten_url = Column(String(200))
    ip_in_url  = Column(String(200))                        
    len_empty_links = Column(Integer)
    external_links  = Column(Text) 
    len_external_links  = Column(Integer)
    external_img_requrl = Column(Text)  
    external_audio_requrl = Column(Text)  
    external_embed_requrl = Column(Text) 
    external_iframe_requrl = Column(Text) 
    len_external_img_requrl = Column(Integer)
    len_external_audio_requrl = Column(Integer)
    len_external_embed_requrl = Column(Integer)
    len_external_iframe_requrl = Column(Integer) 
    
    result = relationship("Result", back_populates="feature")


class Result(Base):
    __tablename__ = 'result'

    result_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submission.submission_id'))
    url_id = Column(Integer, ForeignKey('url.url_id'))
    feature_id = Column(Integer, ForeignKey('feature.feature_id'))
    submitted_url = Column(String(2000))
    phish_prob = Column(Float)
    verdict = Column(String(100))
    trust_score = Column(Float)
    datetime_created = Column(DateTime(timezone=True), server_default=func.now())

    submission = relationship("Submission", back_populates="result")
    url = relationship("Url", back_populates="result")
    feature = relationship("Feature", back_populates="result")