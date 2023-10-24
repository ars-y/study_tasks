from typing import Union

import pandas as pd
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models.spimex import SpimexTradingResults
from schemas import spimex as spimex_schema


class SpimexService:

    @staticmethod
    async def get_last_trading_dates(session: AsyncSession, limit_days: int):
        results = await session.execute(
            select(SpimexTradingResults.date)
            .order_by(desc(SpimexTradingResults.date))
            .distinct()
            .limit(limit_days)
        )
        return results.fetchall()

    @staticmethod
    async def get_dynamics(
        session: AsyncSession,
        trade_filter: spimex_schema.TradePost
    ):
        query = await SpimexService.__get_trade_query(trade_filter)

        if trade_filter.start_date and trade_filter.end_date:
            query = query.filter(
                SpimexTradingResults.date.between(
                    trade_filter.start_date, trade_filter.end_date
                )
            )

        results = await session.execute(query)

        return results.fetchall()

    @staticmethod
    async def get_trading_results(
        session: AsyncSession,
        trade_filter: spimex_schema.Trade
    ):
        query = await SpimexService.__get_trade_query(trade_filter)

        results = await session.execute(query)

        return results.fetchall()

    @staticmethod
    async def save_trade_dataframe(
        session: AsyncSession,
        df: pd.DataFrame
    ) -> None:
        for row in df.itertuples():
            record = SpimexTradingResults(
                exchange_product_id=row.exchange_product_id,
                exchange_product_name=row.exchange_product_name,
                oil_id=row.oil_id,
                delivery_basis_id=row.delivery_basis_id,
                delivery_basis_name=row.delivery_basis_name,
                delivery_type_id=row.delivery_type_id,
                volume=row.volume,
                total=row.total,
                count=row.count,
                date=row.date,
                created_on=row.created_on,
                updated_on=row.updated_on
            )
            session.add(record)

        await session.commit()

    @staticmethod
    async def __get_trade_query(
        trade_filter: Union[spimex_schema.Trade, spimex_schema.TradePost]
    ):
        query = select(
            SpimexTradingResults.oil_id,
            SpimexTradingResults.delivery_type_id,
            SpimexTradingResults.delivery_basis_id,
            SpimexTradingResults.date
        )
        query = query.filter(
            SpimexTradingResults.oil_id == trade_filter.oil_id
        )
        query = query.filter(
            SpimexTradingResults.delivery_type_id == trade_filter.delivery_type_id  # type: ingnore # noqa: E501
        )
        query = query.filter(
            SpimexTradingResults.delivery_basis_id == trade_filter.delivery_basis_id  # type: ingnore # noqa: E501
        )

        return query
