from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings



app = FastAPI(
    title="Fast API Full Stack story generated",
    description="this is a full stack app using fast api and react js"
    version=0.1.0,
    docs= "/docs"
    redoc="/redocs"
)

#adding middleware for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#to run the server

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app: "main:app"  , host='0.0.0.0', port=8000 , reload =True)