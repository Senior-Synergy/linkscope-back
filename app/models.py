from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from app.database import Base

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, text


class Submission(Base):
    __tablename__ = 'submission'

    submission_id = Column(Integer, primary_key=True, index=True)
    datetime_submitted = Column(
        DateTime(timezone=True), server_default=func.now())

    result = relationship("Result", back_populates="submission")


class Url(Base):
    __tablename__ = 'url'
    url_id = Column(Integer, primary_key=True, index=True)
    final_url = Column(String(2000))

    hostname = Column(String(200))
    domain = Column(String(200))
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
    updated_date = Column(DateTime(timezone=True),
                          server_default=func.now(), onupdate=func.now())
    result = relationship("Result", back_populates="url")
    # feature = relationship("Feature", uselist=False, back_populates="url")


class Feature(Base):
    __tablename__ = 'feature'
    feature_id = Column(Integer, primary_key=True, index=True)
    domainlength = Column(Integer)  # 1
    www = Column(Integer)  # 2
    subdomain = Column(Integer)  # 3
    https = Column(Integer)  # 4
    http = Column(Integer)  # 5
    short_url = Column(Integer)  # 6
    ip = Column(Integer)  # 7
    at_count = Column(Integer)  # 8
    dash_count = Column(Integer)  # 9
    equal_count = Column(Integer)  # 10
    dot_count = Column(Integer)  # 11
    underscore_count = Column(Integer)  # 12
    slash_count = Column(Integer)  # 13
    digit_count = Column(Integer)  # 14
    log_contain = Column(Integer)  # 15
    pay_contain = Column(Integer)  # 16
    web_contain = Column(Integer)  # 17
    cmd_contain = Column(Integer)  # 18
    account_contain = Column(Integer)  # 19
    pc_emptylink = Column(Float)  # 20
    pc_extlink = Column(Float)  # 21
    pc_requrl = Column(Float)  # 22
    zerolink = Column(Integer)  # 23
    ext_favicon = Column(Integer)  # 24
    submit_to_email = Column(Integer)  # 25
    sfh = Column(Integer)  # 26
    redirection = Column(Integer)  # 27
    domainage = Column(Integer)  # 28
    domainend = Column(Integer)  # 29

    shortten_url = Column(String(200))
    ip_in_url = Column(String(200))
    len_empty_links = Column(Integer)
    external_links = Column(Text)
    len_external_links = Column(Integer)
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
    datetime_created = Column(DateTime(timezone=True),
                              server_default=func.now())

    submission = relationship("Submission", back_populates="result")
    url = relationship("Url", back_populates="result")
    feature = relationship("Feature", back_populates="result")
