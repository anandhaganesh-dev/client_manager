from sqlalchemy import Integer, Column, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from enum import Enum as pyEnum
from .database import Base

class ProjectStatus(str, pyEnum):
    PENDING  = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    company = Column(String, nullable=True)

    projects = relationship("Project", back_populates= "client")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key= True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    budget = Column(Float, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates = "projects")