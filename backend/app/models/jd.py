from pydantic import BaseModel, Field

class JobAnalysis(BaseModel):
    job_title: str = Field(default="未提及")
    technical_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    education: str = Field(default="未提及")
    experience: str = Field(default="未提及")
    bonus_skills: list[str] = Field(default_factory=list)