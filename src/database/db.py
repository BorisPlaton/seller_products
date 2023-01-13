from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings


def engine_factory() -> Engine:
    return create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DEBUG)


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@" \
                          f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


engine = engine_factory()
SessionFactory = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
