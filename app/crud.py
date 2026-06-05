from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Client, Project
from .schemas import ClientCreate, ClientUpdate, ProjectCreate, ProjectUpdate, ProjectStatus

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
    
    for project in client.projects:
        if project.status in [ProjectStatus.PENDING,
                              ProjectStatus.IN_PROGRESS]:
            raise HTTPException(status_code=400,
                                detail=("Cannot Delete Client with Active Projects"))
    
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

def get_projects(db):
    return db.query(Project).all()

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

def validate_status_transition(
        old_status: ProjectStatus,
        new_status: ProjectStatus
):
    
    if old_status == new_status:
        return
    
    allowed_transitions ={
        ProjectStatus.PENDING: [
            ProjectStatus.IN_PROGRESS,
            ProjectStatus.CANCELLED
        ],
        ProjectStatus.IN_PROGRESS: [
            ProjectStatus.COMPLETED,
            ProjectStatus.CANCELLED
        ],
        ProjectStatus.COMPLETED:[],
        ProjectStatus.CANCELLED:[]
    }

    if new_status not in allowed_transitions[old_status]:
        raise HTTPException(status_code=400, detail="Invalid Status Transition")


def update_project(db: Session, project_id: int, project_update: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        return None

    if project_update.status is not None:
        validate_status_transition(project.status, project_update.status)
    
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