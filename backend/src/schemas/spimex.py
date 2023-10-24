import datetime as dt
from typing import Optional

from pydantic import BaseModel


class LastTradeDate(BaseModel):
    """Pydantic model for getting last trade results."""

    date: dt.datetime


class Trade(BaseModel):
    """Base pydantic model for trade."""

    oil_id: str
    delivery_basis_id: str = None
    delivery_type_id: str = None


class TradePost(Trade):
    """Pydantic model for body with POST request."""

    start_date: Optional[str] = None
    end_date: Optional[str] = None


class TradeResults(Trade):
    """Pydantic model for getting trading results."""

    date: dt.datetime
