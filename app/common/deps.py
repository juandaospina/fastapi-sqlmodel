import typing as t

from fastapi import Depends
from sqlmodel import Session

from app.config.db import get_db


DBDepends = t.Annotated[Session, Depends(get_db)]