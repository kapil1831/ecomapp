from sqlalchemy.orm import Session
from src.db.database import get_session
from fastapi import Depends
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

