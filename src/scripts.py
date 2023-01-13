from random import randint

from mixer.backend.sqlalchemy import mixer
from sqlalchemy import text
from typer import Typer

from database.db import SessionFactory, engine, Base
from database.decorators import session_transaction
from database.models import Product, Seller


app = Typer()


@app.command()
@session_transaction
def load_db_data(quantity: int = 100):
    """
    Loads fake data to the database. The script is used for the
    development purposes.
    """
    session = SessionFactory()
    session.add_all(
        [mixer.blend(
            Product, price=randint(100, 500), quantity=randint(0, 100),
            offer_id=randint(1, 10), seller=Seller(), name=mixer.RANDOM,
            available=mixer.RANDOM(True, True, False)
        ) for _ in range(quantity)]
    )
    print(f"Added {quantity} product and seller records.")


@app.command()
@session_transaction
def truncate_tables(restart_identity: bool = True):
    """
    Delete all rows in the existing tables.
    """
    statement = f"TRUNCATE TABLE {', '.join(Base.metadata.tables.keys())}"
    statement += " RESTART IDENTITY" if restart_identity else ""
    with engine.connect() as conn:
        conn.execute(text(statement))


if __name__ == '__main__':
    app()
