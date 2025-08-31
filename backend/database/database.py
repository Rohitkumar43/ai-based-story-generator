#make the engine and the connect the mapping of th etables and the data


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from ..core.config import settings



engine  = create_engine(
    settings.DATABASE_URL
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base define
Base = declarative_base()

#fxn to start the db 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#BINDING ENGINE TO SPIN THE DATA

def create_tables():
    Base.metadata.create_all(bind=engine)