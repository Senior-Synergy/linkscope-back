from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
# from sqlalchemy.orm import Field, relationship, SQLModel
from sqlalchemy.sql import func

from .database import Base
# Shared properties
class ScanResult(Base):
    __tablename__ = 'url_results'
    scan_id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    final_url = Column(String(255))
    phish_prob = Column(Float)
    is_phishing = Column(Boolean)
    is_active = Column(Boolean, default=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
 
