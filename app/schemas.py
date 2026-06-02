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

class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    company: str | None = None