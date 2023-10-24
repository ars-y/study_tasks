import datetime as dt
from typing import Optional

from pydantic import BaseModel


class LastTradeDate(BaseModel):
    """Pydantic model for getting last trade results."""

    date: dt.datetime


class TradeResults(BaseModel):
    """Pydantic model for getting trading results."""

    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: float
    total: float
    count: int
    date: dt.datetime


class TradePost(BaseModel):
    """Base pydantic model for trade."""

    oil_id: str
    delivery_basis_id: str = None
    delivery_type_id: str = None


class TradePostWithDate(TradePost):
    """Pydantic model for body with POST request."""

    start_date: Optional[str] = None
    end_date: Optional[str] = None
