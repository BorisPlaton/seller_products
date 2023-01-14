import random
from random import randint

from loguru import logger
from mixer.backend.sqlalchemy import mixer
from sqlalchemy import text, select
from typer import Typer

from database.db import SessionFactory, Base
from database.models import Product, Seller
from scripts.state import transaction, state


app = Typer()


@app.command('load-db-data')
@transaction
def load_db_data(quantity: int = 100):
    """
    Loads fake data to the database. The script is used for the
    development purposes.
    """
    session = SessionFactory(bind=state.connection)
    sellers = [Seller() for _ in range(10)]
    session.add_all(sellers)
    session.add_all(
        [mixer.blend(
            Product, price=randint(100, 500), quantity=randint(0, 100),
            offer_id=randint(1, 1000), seller=random.choice(sellers),
            name=mixer.RANDOM
        ) for _ in range(quantity)]
    )
    session.commit()
    logger.info(f"Added {quantity} product records.")


@app.command('truncate-tables')
@transaction
def truncate_tables(restart_identity: bool = True):
    """
    Delete all rows in the existing tables.
    """
    statement = f"TRUNCATE TABLE {', '.join(Base.metadata.tables.keys())}"
    statement += " RESTART IDENTITY" if restart_identity else ""
    state.connection.execute(text(statement))
    logger.info(f"All tables are truncated.")


@app.command('show-products')
def show_products():
    """
    Shows all product records in the database.
    """
    statement = select(Product)
    res = state.connection.execute(statement).all()
    for product in res:
        logger.info(product)


if __name__ == '__main__':
    app()
