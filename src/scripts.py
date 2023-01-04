from random import randint

from mixer.backend.sqlalchemy import mixer
from sqlalchemy import text
from sqlalchemy.orm import Session
from typer import Typer

from database.db import SessionLocal, engine, Base
from database.models import Product, Seller


app = Typer()


@app.command()
def load_db_data(quantity: int = 100):
    """
    Loads fake data to the database. The script is used for the
    development purposes.
    """
    with SessionLocal.begin() as session:
        session: Session
        session.add_all(
            [mixer.blend(
                Product, price=randint(100, 500), quantity=randint(0, 100),
                offer_id=randint(1, 10), seller=Seller()
            ) for _ in range(quantity)]
        )
        for product in session.query(Product).all():
            print(product)
            print(product.seller)


@app.command()
def truncate_tables(restart_identity: bool = True):
    """
    Delete all rows in the existing tables.
    """
    statement = f"TRUNCATE TABLE {', '.join(Base.metadata.tables.keys())}"
    statement += " RESTART IDENTITY" if restart_identity else ""
    with SessionLocal.begin():
        with engine.connect() as conn:
            conn.execute(text(statement))


if __name__ == '__main__':
    app()
