#classs for th table icreation in thee sqlite

from sqlachemy import Column, Integer,String , JSON , ForeignKey , Boolean ,DateTime
from sqlachemy.orm import relationship
from sqlachemy.sql import func

from database.database import Base



class story():
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    session_id = Column(String(256) , index=True)

    creaded_at = Column(DateTime(timezone=True), server_default=func.now())

    nodes = relationship("storyNode", back_populates="story")


#for the storyname contesdt 

class storyNode(Base):
    __tablename__ = "story_node"

    id = Column(Integer, primary_key=True)
    story_id= Column(ForeignKey("story.id"),nullable=False)
    content  = Column(JSON, nullable=False)
    is_root = Column(Boolean,default=False)
    is_ending = Column(Boolean,default=False)
    is_wining_root = Column(Boolean,default=False)


    options = Column(List[JSON],default=[])

    story = relationship("story" ,back_populates="nodes")


