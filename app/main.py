from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Base
from .database import engine, get_db
from .schemas import ClientCreate, ClientResponse, ClientUpdate
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
    client = crud.get_clients(db)
    if client is None:
        raise HTTPException(status_code=404,detail="Client Not Found")
    return client
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