from datetime import datetime
import os
import time

def database_path():
    # Get the absolute path of the current file's directory
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Create the database URI by joining the path and database name
    global database_path_uri
    DATABASE_PATH = os.path.join(basedir, 'books.db')

    return DATABASE_PATH

def database_uri():
    # Create the engine URI
    DATABASE_URI = f'sqlite:///{database_path()}'

    return DATABASE_URI

def check_database_file():
    """Background thread to check if the database file exists."""
    while os.path.exists(database_path_uri):
        dt = datetime.now()
        print("Date and time is:", dt)
        print("Database file exists!")
        time.sleep(5)  # Check every 5 minutes (adjust as needed)
    else:
        dt = datetime.now()
        print("Date and time is:", dt)
        print("Database file does not exist.")
        raise RuntimeError("Server going down.")