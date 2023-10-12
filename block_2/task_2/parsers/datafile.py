from datetime import datetime
from pathlib import Path
from typing import Union

import pandas as pd

import constants as const
from database import engine
from parsers.utils import DateTimeWorker as dtw


class DataFileParser:
    """
    Data parser from excel file.
    Removes unnecessary data,
    adds special columns and saves it to the database.

    Args:
        - **file** - path to file
    """

    def __init__(self, file: Union[Path, str]) -> None:
        self._file = file
        self._date = self._get_trade_date()

    def _get_trade_date(self) -> datetime:
        """Gets date from filename."""
        filename = str(self._file).split('.')[0]
        filename = filename.split('_')[-1]
        date = filename[:8]
        return dtw.create_date(date, '%Y%m%d')

    def _get_skiprows(self) -> int:
        """
        Scans the file and returns the row number
        at which start parsing.
        """
        df = pd.read_excel(self._file)
        return (
            df[df[const.TABLE_FORM_NAME] == const.START_PARSE_FIELD]
            .index.values.astype(int)[0]
        ) + 2

    def _add_special_columns(self, df: pd.DataFrame, field: str) -> None:
        """Adds special columns to a DataFrame."""
        df[const.OIL_ID] = df[field].str[:4]
        df[const.DELIVERY_BASIS_ID] = df[field].str[4:7]
        df[const.DELIVERY_TYPE_ID] = df[field].str[-1]
        df[const.DATE] = pd.to_datetime(self._date.date())
        df[const.CREATED_ON] = pd.to_datetime(dtw.get_current_date())
        df[const.UPDATED_ON] = pd.to_datetime(dtw.get_current_date())

    def _rename_columns(
        self,
        df: pd.DataFrame,
        old_col_names: list[str],
        new_col_names: list[str]
    ) -> None:
        """
        Gets a list of old and new column names
        and renames the columns.
        """
        column_names: dict = {
            old: new for old, new in zip(old_col_names, new_col_names)
        }

        for col_name in old_col_names:
            df.rename(
                columns={col_name: column_names[col_name]},
                inplace=True
            )

    def _get_table_column_names(self) -> dict[str, str]:
        """
        Returns a dict of column names,
        where the values are special column names
        from excel table.
        """
        return {
            const.EXCHANGE_PRODUCT_ID: 'Код\nИнструмента',
            const.EXCHANGE_PRODUCT_NAME: 'Наименование\nИнструмента',
            const.DELIVERY_BASIS_NAME: 'Базис\nпоставки',
            const.VOLUME: 'Объем\nДоговоров\nв единицах\nизмерения',
            const.TOTAL: 'Обьем\nДоговоров,\nруб.',
            const.COUNT: 'Количество\nДоговоров,\nшт.',
        }

    def _save(self, df: pd.DataFrame) -> None:
        """Save DataFrame to database."""
        df.to_sql(
            const.TABLE_DB_NAME,
            engine, if_exists='append',
            index=False
        )

    def parse(self):
        """Run file data parsing."""
        cols: dict[str, str] = self._get_table_column_names()

        skiprows: int = self._get_skiprows()
        df = pd.read_excel(
            self._file, skiprows=skiprows, usecols=cols.values()
        )

        df.dropna(inplace=True)
        df.drop(df[df[cols[const.COUNT]] == '-'].index, inplace=True)

        self._add_special_columns(df, cols[const.EXCHANGE_PRODUCT_ID])
        self._rename_columns(df, cols.values(), cols.keys())

        self._save(df)
