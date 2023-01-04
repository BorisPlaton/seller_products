from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@" \
                          f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)
