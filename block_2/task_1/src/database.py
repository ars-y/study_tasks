from sqlalchemy.engine import create_engine

from src import settings


engine = create_engine(str(settings.DATABASE_URL))
