from database_backend import database_path
import os
from server import db, Book

def delete_database():
    if os.path.exists(database_path()):
        # Delete all the records in the database
        db.reflect()
        db.drop_all()
        # Delete the database file
        os.remove(database_path())
        print("Database deleted successfully!")
    else:
        print("No database found to delete.")

# Call the delete_database() function to delete the database
delete_database()