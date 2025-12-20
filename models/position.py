from __future__ import annotations
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from consts.trade_consts import TradeType, TradeStatus
from models import Base
from models.pair import Pair


class Position(Base):
    __tablename__ = "position"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True)
    pair_id: UUID = Column(UUID(as_uuid=True), ForeignKey("pair.id"))
    type: TradeType = Column(Text, nullable=False)
    entry: float = Column(nullable=False)
    stop_loss: float = Column(nullable=False)
    take_profit: float = Column(nullable=False)
    exit_price: float | None = Column(nullable=True)
    position_size: float = Column(nullable=False)
    opening_reason: str = Column(Text, nullable=True)
    created: datetime = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated: datetime | None = Column(TIMESTAMP, nullable=True, default=datetime.now())
    status: TradeStatus = Column(Text, nullable=False, default="open")

    # Relationships

    pair: Pair = relationship('Pair')

    # Properties

    @property
    def result_money(self) -> float:
        value_one = self.position_size * self.entry
        if self.exit_price:
            value_two = self.position_size * self.exit_price
            if self.type == TradeType.SHORT:
                return value_one - value_two
            return value_two - value_one
        return 0.0

    @property
    def risk_reward_ratio(self) -> float:
        maximum_loss_ratio = max(self.entry, self.stop_loss) - min(self.entry, self.stop_loss)
        maximum_profit_ratio = max(self.entry, self.take_profit) - min(self.entry, self.take_profit)
        return round(maximum_profit_ratio / maximum_loss_ratio, 2)
