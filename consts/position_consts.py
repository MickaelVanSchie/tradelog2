from typing import Literal

TradeType = Literal["long", "short"]

TradeStatus = Literal["open", "filled", "cancelled", "take_profit", "stop_loss", "closed"]

class TRADE_TYPE:
    LONG = "long"
    SHORT = "short"