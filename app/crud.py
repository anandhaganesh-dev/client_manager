from sqlalchemy.orm import Session
from .models import Client
from .schemas import ClientCreate, ClientUpdate

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