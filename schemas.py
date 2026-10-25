from pydantic import BaseModel, Field


class Education(BaseModel):
    degree: str | None
    field: str | None
    institution: str | None


class WorkExperience(BaseModel):
    job_title: str | None
    company: str | None
    description: str | None


class ResumeInfo(BaseModel):
    name: str | None
    email: str | None
    skills: list[str]
    education: list[Education]
    work_experience: list[WorkExperience]