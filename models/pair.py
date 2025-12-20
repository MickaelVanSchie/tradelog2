from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Pair(Base):
    __tablename__ = "pair"

    id = Column(UUID, primary_key=True)
    base_currency = Column(Text, nullable=False)
    quote_currency = Column(Text, nullable=False)

    @property
    def shorthand(self) -> str:
        return f"{self.base_currency}/{self.quote_currency}"