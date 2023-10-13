import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src import Base


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name_genre: Mapped[str] = mapped_column()


class Author(Base):
    __tablename__ = 'author'

    author_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name_author: Mapped[str] = mapped_column()


class City(Base):
    __tablename__ = 'city'

    city_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name_city: Mapped[str] = mapped_column()
    days_delivery: Mapped[int] = mapped_column()


class Book(Base):
    __tablename__ = 'book'

    book_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(
        ForeignKey('author.author_id', ondelete='RESTRICT')
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genre.genre_id', ondelete='RESTRICT')
    )
    price: Mapped[float] = mapped_column(default=0.0)
    amount: Mapped[int] = mapped_column(default=0)


class Client(Base):
    __tablename__ = 'client'

    client_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name_client: Mapped[str] = mapped_column()
    city_id: Mapped[int] = mapped_column(
        ForeignKey('city.city_id', ondelete='CASCADE')
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)


class Buy(Base):
    __tablename__ = 'buy'

    buy_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    buy_description: Mapped[Optional[str]]
    clien_id: Mapped[int] = mapped_column(
        ForeignKey('client.client_id', ondelete='CASCADE')
    )


class Step(Base):
    __tablename__ = 'step'

    step_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name_step: Mapped[str] = mapped_column()


class BuyBook(Base):
    __tablename__ = 'buy_book'

    buy_book_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey('buy.buy_id', ondelete='CASCADE')
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('book.book_id', ondelete='CASCADE')
    )
    amount: Mapped[int] = mapped_column(default=0)


class BuyStep(Base):
    __tablename__ = 'buy_step'

    buy_step_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey('buy.buy_id', ondelete='CASCADE')
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey('step.step_id', ondelete='CASCADE')
    )
    date_step_beg: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    date_step_end: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
