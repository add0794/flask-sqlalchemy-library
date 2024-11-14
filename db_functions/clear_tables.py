from database_backend import database_path
import os
from server import db, Book

def clear_tables():
    if os.path.exists(database_path()):
        # Delete all the records in the database
        db.reflect()
        db.drop_all()
        print("Tables & data deleted successfully!")
    else:
        print("No database found to delete.")

# Call the delete_database() function to delete the database
clear_tables()

