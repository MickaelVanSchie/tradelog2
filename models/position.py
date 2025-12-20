from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, ForeignKey, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as SQLUUID

from consts.trade_consts import TradeType
from models import Base


class Position(Base):
    __tablename__ = "position"

    id: UUID = Column(SQLUUID, primary_key=True)
    pair_id: UUID = Column(SQLUUID, ForeignKey("pair.id"))
    type: TradeType = Column(Text, nullable=False)
    entry: float = Column(nullable=False)
    stop_loss: float = Column(nullable=False)
    take_profit: float = Column(nullable=False)
    exit_price: float | None = Column(nullable=True)
    position_size: float = Column(nullable=False)
    opening_reason: str = Column(Text, nullable=True)
    created: datetime  = Column(TIMESTAMP, nullable=False)
    updated: datetime | None = Column(TIMESTAMP, nullable=True)

    @property
    def result_money(self) -> float:
        value_one = self.position_size * self.entry
        value_two = self.position_size * self.exit_price
        if self.type == TradeType.SHORT:
            return value_one - value_two
        return value_two - value_one