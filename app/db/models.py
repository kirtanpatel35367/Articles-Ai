from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source = Column(Text, nullable=True)
    url = Column(String, nullable=False, unique=True, index=True)  # <-- add unique + index
    points = Column(Integer)
    published_at = Column(DateTime, default=datetime.utcnow)
    author = Column(String)
