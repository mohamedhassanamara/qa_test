from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String, nullable=False)
    summarized_text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
