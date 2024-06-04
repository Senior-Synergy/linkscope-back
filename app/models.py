from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Submission(Base):
    __tablename__ = 'submission'

    submission_id = Column(Integer, primary_key=True, index=True)
    datetime_submitted = Column(
        DateTime(timezone=True), server_default=func.now())

    result = relationship("Result", back_populates="submission")

    def __repr__(self):
        return (
            f'SubmissionModel(id={self.submission_id})'
        )

class Url(Base):
    __tablename__ = 'url'
    
    url_id = Column(Integer, primary_key=True, index=True)
    final_url = Column(String(2000))

    hostname = Column(String(200))
    domain = Column(String(200))
    registrar = Column(String(200))
    ip_address = Column(String(200))
    subdomains = Column(String(200))
    scheme = Column(String(200))

    # extra domain infomation
    creation_date = Column(DateTime(timezone=True))
    expiration_date = Column(DateTime(timezone=True))
    domainage = Column(Integer)
    domainend = Column(Integer)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    google_is_malicious = Column(Integer)
    updated_date = Column(DateTime(timezone=True),
                          server_default=func.now(), onupdate=func.now())

    result = relationship("Result", back_populates="url")

    def __repr__(self):
        return (
            f'UrlModel(id={self.url_id})'
        )

class Feature(Base):
    __tablename__ = 'feature'
    
    feature_id = Column(Integer, primary_key=True, index=True)
    domainlength = Column(Integer)  #1
    www = Column(Integer)  # 2
    subdomain = Column(Integer) #3
    https = Column(Integer)  # 4
    short_url = Column(Integer)  #5
    at_count = Column(Integer) #6
    dash_count = Column(Integer)  # 7
    equal_count = Column(Integer)  # 8
    dot_count = Column(Integer)  # 9
    underscore_count = Column(Integer)  # 10
    slash_count = Column(Integer)  # 11
    digit_count = Column(Integer)  # 12
    log_count = Column(Integer) #13
    pay_count = Column(Integer) #14
    web_count = Column(Integer) #15
    account_count = Column(Integer)# 16
    pc_emptylink = Column(Float) # 17 
    pc_extlink = Column(Float) # 18 
    pc_requrl = Column(Float)  # 19
    zerolink = Column(Integer)  # 20
    ext_favicon = Column(Integer)  #21
    submit2Email = Column(Integer) # 22
    sfh = Column(Integer)  # 23
    redirection = Column(Integer) # 24 
    domainage = Column(Integer) # 25
    domainend = Column(Integer)  # 26
    
    shortten_url = Column(String(200))
    ip_in_url = Column(String(200))
    empty_links_count = Column(Integer)
    external_links = Column(Text)
    external_img_requrl = Column(Text)
    external_audio_requrl = Column(Text)
    external_embed_requrl = Column(Text)
    external_iframe_requrl = Column(Text)
    len_external_links  = Column(Integer)
    len_external_img_requrl = Column(Integer)
    len_external_audio_requrl = Column(Integer)
    len_external_embed_requrl = Column(Integer)
    len_external_iframe_requrl = Column(Integer) 

    result = relationship("Result", back_populates="feature")
    
    def __repr__(self):
        return (
            f'FeatureModel(id={self.feature_id})'
        )

class Result(Base):
    __tablename__ = 'result'

    result_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submission.submission_id'))
    url_id = Column(Integer, ForeignKey('url.url_id'))
    feature_id = Column(Integer, ForeignKey('feature.feature_id'))
    submitted_url = Column(String(2000))
    phish_prob = Column(Float)
    phish_prob_mod = Column(Float)
    has_soup = Column(Integer)
    datetime_created = Column(DateTime(timezone=True),
                              server_default=func.now())

    submission = relationship("Submission", back_populates="result")
    url = relationship("Url", back_populates="result")
    feature = relationship("Feature", back_populates="result")

    def __repr__(self):
        return (
            f'ResultModel(id={self.result_id})'
        )