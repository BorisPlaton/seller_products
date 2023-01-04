from typer import Typer


app = Typer()


@app.command()
def load_db_data():
    """
    Loads fake data to the database. The scripts is used for the
    development purposes.
    """
    pass


if __name__ == '__main__':
    app()
