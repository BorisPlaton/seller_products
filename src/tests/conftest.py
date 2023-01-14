from typing import Callable

import pytest
from alembic import command
from alembic.config import Config
from mixer.backend.sqlalchemy import mixer
from sqlalchemy.future import Connection
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from config.settings import settings
from database.db import SessionFactory, engine_factory
from database.models import Product
from main import create_app


@pytest.fixture(scope='session')
def engine():
    return engine_factory()


@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    config = Config(settings.BASE_DIR / 'alembic.ini')
    config.set_section_option('alembic', 'script_location', str(settings.BASE_DIR / 'migrations'))
    command.downgrade(config, 'base')
    command.upgrade(config, 'head')
    yield
    command.downgrade(config, 'base')
    command.upgrade(config, 'head')


@pytest.fixture(scope='session')
def test_app():
    app = create_app()
    return TestClient(app)


@pytest.fixture(scope='session')
def url_for(test_app) -> Callable:
    app = create_app()

    def inner(url_path: str) -> str:
        return app.url_path_for(url_path)

    return inner


@pytest.fixture
def db_session(engine) -> Session:
    with SessionFactory(bind=engine) as session:
        session.begin()
        try:
            yield session
        finally:
            session.rollback()


@pytest.fixture
def conn(engine) -> Connection:
    with engine.connect() as conn:
        yield conn


@pytest.fixture
def get_product():
    def inner(**kwargs):
        kwargs.setdefault('quantity', 1)
        kwargs.setdefault('price', 100)
        kwargs.setdefault('offer_id', 1)
        kwargs.setdefault('available', True)
        return mixer.blend(Product, **kwargs)

    return inner
