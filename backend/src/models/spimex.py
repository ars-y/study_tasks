import datetime as dt

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.bases import Base


class SpimexTradingResults(Base):

    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column()
    exchange_product_name: Mapped[str] = mapped_column()
    oil_id: Mapped[str] = mapped_column()
    delivery_basis_id: Mapped[str] = mapped_column()
    delivery_basis_name: Mapped[str] = mapped_column()
    delivery_type_id: Mapped[str] = mapped_column()
    volume: Mapped[float] = mapped_column()
    total: Mapped[float] = mapped_column()
    count: Mapped[int] = mapped_column()
    date: Mapped[dt.datetime] = mapped_column(DateTime())
    created_on: Mapped[dt.datetime] = mapped_column(DateTime())
    updated_on: Mapped[dt.datetime] = mapped_column(DateTime())
