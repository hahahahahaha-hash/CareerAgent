from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import chat
from app.api import resume
from app.api import report

app = FastAPI(
    title=settings.app_name
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(resume.router)
app.include_router(report.router)

@app.get("/")
def root():

    return {
        "message": settings.app_name
    }