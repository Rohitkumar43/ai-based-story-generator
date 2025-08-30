#here we will be write the route for the jobs which will be simulating 


import uuid
from fastapi import APIRouter , Depends ,status , HTTPException , Cookie

from backend.database import get_db 
from sqlachemy.orm import Session
from typing import Optional

from schemas.job import StoryJobResponse
from .database.database import Base
from .models.job import storyjob



router = APIRouter(
    prefix="/jobs",
    tags=['Jobs']
)


# to get the job details fromt the id from the database and return it as a response

@router.get("{job_id}" , response_model=StoryJobResponse)
def get_job_id( job_id: str , db:Session=Depends(get_db)):
    #query for the job
    job = db.query(storyjob).filter(storyjob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with id {job_id} doesnot exist")
    return job