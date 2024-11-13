from multiprocessing import Process
import os
from server import app, db
from sqlalchemy import create_engine

def clear_database():
    # Get the absolute path of the current file's directory
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Create the database URI by joining the path and database name
    database_path = os.path.join(basedir, 'books.db')

    # Create the engine (adjust the URI to match your setup)
    DATABASE_URI = f'sqlite:///{database_path}'  # Match this with your database path in server.py
    engine = create_engine(DATABASE_URI)

    # Execute the query and load data into a DataFrame
    with engine.connect() as connection:
        db.drop_all()

if __name__ == "__main__":
    p = Process(target=clear_database())
    p.start()
    p.join()
    app.run(debug=True, use_reloader=False)