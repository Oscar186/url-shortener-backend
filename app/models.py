from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
from sqlalchemy.sql import func
from app.database import Base

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer,primary_key = True, index = True)
    long_url = Column(String(2048), nullable = False)
    short_code = Column(String(10), nullable = False, unique = True, index = True)
    clicks = Column(Integer, default = 0)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
# from pydantic import BaseModel,HttpUrl

# class URLRequest(BaseModel):
#     long_url: HttpUrl


