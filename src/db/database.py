from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from collections.abc import Generator
from src.core.conf import settings
from ..models.models import Base

database_url = settings.database_url

engine = create_engine(database_url, echo=True)
def create_db_and_tables():
    Base.metadata.create_all(engine)

def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session
        
        