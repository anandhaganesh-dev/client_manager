from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE__URL = "postgresql://postgres:@localhost:5432/client_manager"

engine = create_engine(DATABASE__URL)

SessionLocal = sessionmaker(
    autoflush = False,
    autocommit = False,
    bind = engine
)

Base = declarative_base()