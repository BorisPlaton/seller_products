import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.orm import Session

from config.settings import settings
from database.db import SessionLocal


@pytest.fixture
def db_session() -> Session:
    session = SessionLocal()
    session.begin()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    config = Config(settings.BASE_DIR / 'alembic.ini')
    config.set_section_option('alembic', 'script_location', str(settings.BASE_DIR / 'migrations'))
    command.upgrade(config, 'head')
    yield
    command.downgrade(config, 'base')
    command.upgrade(config, 'head')
