from sqlalchemy.orm import declarative_base

Base = declarative_base()
meta = Base.metadata

from .position import Position