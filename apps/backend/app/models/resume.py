from sqlalchemy import Column, Integer, String, Text
from ..models.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    filename = Column(String(255))
    content = Column(Text)
    match_rate = Column(Integer)

class ProcessedResume(Base):
    __tablename__ = "processed_resumes"

    id = Column(Integer, primary_key=True, index=True)
    job_description = Column(Text)
    resume_content = Column(Text)
    score = Column(Integer)
