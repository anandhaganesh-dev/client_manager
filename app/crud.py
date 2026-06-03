from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Client, Project
from .schemas import ClientCreate, ClientUpdate, ProjectCreate, ProjectUpdate

def client_create(db: Session, client = ClientCreate):
    db_client = Client(
        name = client.name,
        email = client.email,
        company = client.company
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client

def get_clients(db):
    return db.query(Client).all()

def get_client_by_id(db:Session, client_id:int):
    client = db.query(Client).filter(Client.id==client_id).first()

    if client is None:
        return None
    return client


def update_client(db: Session, client_id: int, client_update: ClientUpdate):
    client = db.query(Client).filter(Client.id==client_id).first()

    if client is None:
        return None
    
    update_data = client_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)

    return client

def delete_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id==client_id).first()

    if client is None:
        return None
    
    db.delete(client)
    db.commit()

    return client

def create_project(db: Session, project_data= ProjectCreate):
    client = db.query(Client).filter(Client.id == project_data.client_id).first()

    if client is None:
        return None
    
    project = Project(
        title = project_data.title,
        description = project_data.description,
        budget = project_data.budget,
        status = project_data.status
    )

    client.projects.append(project)
    db.add(project)
    db.commit()
    db.refresh(project)

    return project

def get_client_projects(
    db: Session,
    client_id: int
):
    client = (
        db.query(Client)
        .filter(Client.id == client_id)
        .first()
    )

    if client is None:
        return None

    return client.projects

def get_project_by_id(
    db: Session,
    project_id: int
):
    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

def update_project(db: Session, project_id: int, project_update: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        return None
    
    if (
        project_update.client_id is not None
    ):
        client = (
            db.query(Client)
            .filter(
                Client.id == project_update.client_id
            )
            .first()
        )

        if client is None:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
    
    update_data = project_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id==project_id).first()

    if project is None:
        return None
    
    db.delete(project)
    db.commit()

    return project