# #here we write the api endpoint for the backend 


# from fastapi import APIRouter, Depends , Response , HTTPException,status , Cookies , background_tasks

# from datetime import datetime
# from sqlalchemy.orm import session


# from database.database import get_db , SessionLocal
# from model.story import storyNode , story
# from model.job import storyJob
# from schemas.story import (
#     CompleteStoryResponse , CompleteStoryNodeResponse , CompleteStoryRequest
# )
# from schemas.job import StoryJobResponse
# from schemas.story_schema import StoryCreateSchema , StoryUpdateSchema

# router = APIRouter(
#     prefix="/story",
#     tags=["story"]
# )


# # ge the session id 

# def get_sesssion_id();
# if not session_id:
#     #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Session ID is missing")
#     session_id =str(uuid.uuid4().hex)
#     return session_id


# @router.post("/create" , response_model=StoryJobResponse )
# def create_story(
#     request: CreateStoryRequest
#     background_tasks: BackgroundTasks
#     response: Response
#     session_id:str = Depends(get_sesssion_id)
#     db: session = Depends(get_db)
# ):
#     response.set_cookie(key="session_id", value="session_id")
#     #ge tthe job id

#     job_id = str(uuid.uuid4().hex)

#     job = storyJob(
#         job_id=job_id,
#         session_id=session_id,
#         theme=request.theme,
#         status =  "pending"
#     )

#     db.add(job)
#     db.commit()

#     return job
    
# # ttTODO: IMPELMENT THE BACKGROUND TASKS TO CREATE A STORY



# def generate_story_task(job_id: str, theme: str, session_id: str):
#     db = SessionLocal()

#     try:
#         job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

#         if not job:
#             return

#         try:
#             job.status = "processing"
#             db.commit()

#             story = StoryGenerator.generate_story(db, session_id, theme)

#             job.story_id = story.id  # todo: update story id
#             job.status = "completed"
#             job.completed_at = datetime.now()
#             db.commit()
#         except Exception as e:
#             job.status = "failed"
#             job.completed_at = datetime.now()
#             job.error = str(e)
#             db.commit()
#     finally:
#         db.close()


# @router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
# def get_complete_story(story_id: int, db: Session = Depends(get_db)):
#     story = db.query(Story).filter(Story.id == story_id).first()
#     if not story:
#         raise HTTPException(status_code=404, detail="Story not found")

#     complete_story = build_complete_story_tree(db, story)
#     return complete_story


# def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
#     nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

#     node_dict = {}
#     for node in nodes:
#         node_response = CompleteStoryNodeResponse(
#             id=node.id,
#             content=node.content,
#             is_ending=node.is_ending,
#             is_winning_ending=node.is_winning_ending,
#             options=node.options
#         )
#         node_dict[node.id] = node_response

#     root_node = next((node for node in nodes if node.is_root), None)
#     if not root_node:
#         raise HTTPException(status_code=500, detail="Story root node not found")

#     return CompleteStoryResponse(
#         id=story.id,
#         title= story.title,
#         session_id=story.session_id,
#         created_at=story.created_at,
#         root_node=node_dict[root_node.id],
#         all_nodes=node_dict
#     )



from fastapi import APIRouter, Depends, Response, HTTPException, status, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

from database.database import get_db, SessionLocal
from model.story import StoryNode, Story
from model.job import StoryJob
from schemas.story import (
    CompleteStoryResponse, CompleteStoryNodeResponse, CompleteStoryRequest
)
from schemas.job import StoryJobResponse
from schemas.story_schema import StoryCreateSchema, StoryUpdateSchema

router = APIRouter(
    prefix="/story",
    tags=["story"]
)

# Create Story Request Schema (assuming this was missing)
class CreateStoryRequest:
    def __init__(self, theme: str):
        self.theme = theme

# Story Generator class (assuming this was missing)
class StoryGenerator:
    @staticmethod
    def generate_story(db: Session, session_id: str, theme: str):
        # Placeholder implementation - replace with your actual story generation logic
        story = Story(
            title=f"Story about {theme}",
            session_id=session_id,
            created_at=datetime.now()
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return story

# Get session id function
def get_session_id():
    session_id = str(uuid.uuid4().hex)
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id)
    
    # Get the job id
    job_id = str(uuid.uuid4().hex)

    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Add background task
    background_tasks.add_task(generate_story_task, job_id, request.theme, session_id)

    return job

# Background task to create a story
def generate_story_task(job_id: str, theme: str, session_id: str):
    db = SessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            story = StoryGenerator.generate_story(db, session_id, theme)

            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )