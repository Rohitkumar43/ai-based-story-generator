####
# what it will actually alraeadyv built the data model for the story_id
# here what actually is that the frontend will get the job 
# backend will return the job 
# frontned -> if the job is done 
# backend -. send tjhe response 
# frontend -> update the status of the job 
# if the job is done then it will send the story 
# ####



from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class StoryJob(Base):
    __tablename__ = "jobstory"

    id = Column(Integer, primary_key=True)
    job_id = Column(String(256), unique=True , index = True)
    theme = Column(String(100), nullable=False)
    session_id = Column(String())
    story_id = Column(String())
    error = Column(String())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)