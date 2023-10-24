import json

from sqlalchemy import Row


def convert_to_schema(schema_model, data_sequence) -> list:
    """Convert a data sequence to a pyndantic model."""
    if isinstance(data_sequence[0], Row):
        return [
            schema_model(**data._mapping)
            for data in data_sequence
        ]

    data_sequence = json.loads(data_sequence)
    return [schema_model(**data) for data in data_sequence]
