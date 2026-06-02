from pydantic import EmailStr, BaseModel

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