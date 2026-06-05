from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Base
from .database import engine, get_db
from .schemas import ClientCreate, ClientResponse, ClientUpdate, ProjectCreate, ProjectResponse, ProjectUpdate
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return{"message":"API is running"}

@app.post("/client")
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    return crud.client_create(db, client)

@app.get("/clients", response_model=list[ClientResponse])
def get_clients(
    db: Session=Depends(get_db)
):
    clients = crud.get_clients(db)
    if clients is None:
        raise HTTPException(status_code=404,detail="Client Not Found")
    return clients

@app.get("/projects", response_model=list[ProjectResponse])
def get_projects(
    db: Session=Depends(get_db)
):
    projects = crud.get_projects(db)
    if projects is None:
        raise HTTPException(status_code=404,detail="Project Not Found")
    return projects

@app.get("/client/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id:int, db:Session=Depends(get_db)
                     ):
    client = crud.get_client_by_id(db, client_id)
    if client is None:
        raise HTTPException(status_code=404,detail="Client Not Found")
    return client

@app.put("/client/{client_id}")
def update_client(client_id:int,
                  client_update: ClientUpdate,
                  db: Session=Depends(get_db)
                  ):
    client = crud.update_client(db,client_id,client_update)
    if client is None:
        raise HTTPException(status_code=404,detail="Client Not Found")
    return client

@app.delete("/client/{client_id}")
def delete_client(client_id: int, db: Session=Depends(get_db)):
    client = crud.delete_client(db, client_id)
    if client is None:
        raise HTTPException(status_code=404,detail="Client Not Found")
    return {'message':'Client Deleted Sucessfully'}

@app.post("/project",response_model=ProjectResponse)
def create_project(project:ProjectCreate, db: Session=Depends(get_db)):
    new_project = crud.create_project(db, project)

    if new_project is None:
        raise HTTPException(status_code=404, detail="Client Not Found")
    
    return new_project

@app.get("/project/{project_id}",response_model=ProjectResponse)
def get_project_by_id(project_id:int, db: Session=Depends(get_db)):
    return crud.get_project_by_id(db, project_id)

@app.get(
    "/client/{client_id}/projects",
    response_model=list[ProjectResponse]
)
def get_client_projects(
    client_id: int,
    db: Session = Depends(get_db)
):
    projects = crud.get_client_projects(
        db,
        client_id
    )

    if projects is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return projects

@app.put("/project/{project_id}", response_model=ProjectResponse)
def update_project(project_id:int,
                  project_update: ProjectUpdate,
                  db: Session=Depends(get_db)
                  ):
    project = crud.update_project(db,project_id,project_update)
    if project is None:
        raise HTTPException(status_code=404,detail="Project Not Found")
    return project

@app.delete("/project/{project_id}")
def delete_project(project_id: int, db: Session=Depends(get_db)):
    project = crud.delete_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404,detail="Project Not Found")
    return {'message':'Project Deleted Sucessfully'}