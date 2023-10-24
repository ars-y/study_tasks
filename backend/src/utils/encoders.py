import json
from typing import Sequence

from sqlalchemy import Row

from helpers.datetime import DateTimeWorker as dtw


def json_encode_rows(rows: Sequence[Row]) -> str:
    """Serialize list of SQLAlchemy Rows to a JSON str."""
    return json.dumps(
        [dict(row._mapping) for row in rows],
        default=dtw.serialize_dates
    )
