from pydantic import EmailStr, BaseModel
from .models import ProjectStatus

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None

class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    company: str | None = None

    class Config:
        from_attributes = True

class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    company: str | None = None

class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    budget: float
    status: ProjectStatus = ProjectStatus.PENDING
    client_id: int

class ProjectResponse(BaseModel):
    id:int
    title:str
    description:str | None = None
    budget: float
    status: ProjectStatus
    client_id: int

    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    budget: float | None = None
    client_id: int | None = None