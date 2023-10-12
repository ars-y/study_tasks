from pathlib import Path


###############################################################################
# DIR PATH
###############################################################################

BASE_DIR: Path = Path(__file__).resolve().parent

DATA_FILES_DIR: Path = BASE_DIR / 'data'

DOWNLOAD_DIR: Path = DATA_FILES_DIR / 'download'

###############################################################################
# URL PATH
###############################################################################

BASE_URL: str = 'https://spimex.com'

TRADES_ENDPOINT: str = '/markets/oil_products/trades/results/'

###############################################################################
# HTML TAGS AND ATTRIBUTES
###############################################################################

A_TAG_CLASS: str = 'accordeon-inner__item-title link xls'

DIV_TAG_CLASS: str = 'accordeon-inner__item'

LI_TAG_CLASS: str = 'bx-pag-next'


class AttrName:

    HREF: str = 'href'
    KLASS: str = 'class'


class TagName:

    A: str = 'a'
    DIV: str = 'div'
    LI: str = 'li'
    P: str = 'p'
    SPAN: str = 'span'


###############################################################################
# PARSER ENGINE
###############################################################################

BS_PARSER: str = 'lxml'

###############################################################################
# DATETIME
###############################################################################

DATE_FORMAT_PATTERN: str = '%d.%m.%Y'

###############################################################################
# EXCEL TABLE FIELDS
###############################################################################

TABLE_FORM_NAME: str = 'Форма СЭТ-БТ'

START_PARSE_FIELD: str = 'Единица измерения: Метрическая тонна'

###############################################################################
# DATABASE TABLE FIELDS
###############################################################################

TABLE_DB_NAME: str = 'spimex_trading_results'

EXCHANGE_PRODUCT_ID: str = 'exchange_product_id'

EXCHANGE_PRODUCT_NAME: str = 'exchange_product_name'

DELIVERY_BASIS_NAME: str = 'delivery_basis_name'

VOLUME: str = 'volume'

TOTAL: str = 'total'

COUNT: str = 'count'

OIL_ID: str = 'oil_id'

DELIVERY_BASIS_ID: str = 'delivery_basis_id'

DELIVERY_TYPE_ID: str = 'delivery_type_id'

DATE: str = 'date'

CREATED_ON: str = 'created_on'

UPDATED_ON: str = 'updated_on'

###############################################################################
# PARSER PARAMS
###############################################################################

PERIOD_DAYS: int = 30

LINK_PATTERN: str = '/upload/'
