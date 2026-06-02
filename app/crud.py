from sqlalchemy.orm import Session
from .models import Client
from .schemas import ClientCreate

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
    return db.query(Client).filter(Client.id==client_id).first()