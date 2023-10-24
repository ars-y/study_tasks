from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cache import redis
from db import sessions
from services.spimex import SpimexService
from schemas import spimex as spimex_schema
from helpers.datetime import DateTimeWorker as dtw
from utils import (
    convert_to_schema,
    hash_key,
    json_encode_rows
)


router = APIRouter()


@router.get('/last-date', response_model=list[spimex_schema.LastTradeDate])
async def get_last_trading_dates(
    limit_day: int,
    session: Annotated[AsyncSession,  Depends(sessions.get_session)]
):
    """Returns a list of dates for the last trading days."""
    key: str = hash_key('limit_day_' + str(limit_day))
    cache_data = await redis.get_cache(key)

    if not cache_data:
        trades_data = await SpimexService.get_last_trading_dates(
            session, limit_day
        )
        data_to_cahe = json_encode_rows(trades_data)
        await redis.set_cache(key, data_to_cahe, dtw.get_seconds_left())

        return convert_to_schema(spimex_schema.LastTradeDate, trades_data)

    return convert_to_schema(spimex_schema.LastTradeDate, cache_data)


@router.post('/dynamics', response_model=list[spimex_schema.TradeResults])
async def get_dynamics(
    trade_filter: spimex_schema.TradePostWithDate,
    session: Annotated[AsyncSession,  Depends(sessions.get_session)]
):
    """Returns list of trades for a given period."""
    date_format: str = '%Y-%m-%d'
    trade_filter.start_date = dtw.create_date(
        trade_filter.start_date, date_format
    )
    trade_filter.end_date = dtw.create_date(trade_filter.end_date, date_format)

    key: str = hash_key(trade_filter.model_dump_json())
    cache_data = await redis.get_cache(key)

    if not cache_data:
        trades_data = await SpimexService.get_dynamics(session, trade_filter)
        data_to_cahe = json_encode_rows(trades_data)
        await redis.set_cache(key, data_to_cahe, dtw.get_seconds_left())

        return convert_to_schema(
            spimex_schema.TradeResults,
            trades_data
        )

    return convert_to_schema(spimex_schema.TradeResults, cache_data)


@router.post(
    '/trading-results',
    response_model=list[spimex_schema.TradeResults]
)
async def get_trading_results(
    trade_filter: spimex_schema.TradePost,
    session: Annotated[AsyncSession,  Depends(sessions.get_session)]
):
    """Returns a list of recent trades."""
    key: str = hash_key(trade_filter.model_dump_json())
    cache_data = await redis.get_cache(key)

    if not cache_data:
        trades_data = await SpimexService.get_trading_results(
            session, trade_filter
        )
        data_to_cahe = json_encode_rows(trades_data)
        await redis.set_cache(key, data_to_cahe, dtw.get_seconds_left())

        return convert_to_schema(
            spimex_schema.TradeResults,
            trades_data
        )

    return convert_to_schema(spimex_schema.TradeResults, cache_data)
