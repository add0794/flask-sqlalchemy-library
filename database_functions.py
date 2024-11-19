# from database_backend import database_path
# import os
# from server import db, Book

# # clear tables
# def clear_tables():
#     if os.path.exists(database_path()):
#         # Delete all the records in the database
#         db.reflect()
#         db.drop_all()
#         print("Tables & data deleted successfully!")
#     else:
#         print("No database found to delete.")

# # delete the database
# def delete_database():
#     if os.path.exists(database_path()):
#         # Delete all the records in the database
#         db.reflect()
#         db.drop_all()
#         # Delete the database file
#         os.remove(database_path())
#         print("Database deleted successfully!")
#     else:
#         print("No database found to delete.")

# from database_backend import database_path
# from db_file import db
# import os

# class DatabaseManager:
#     def __init__(self, database_path):
#         """
#         Initialize the DatabaseManager with the path to the database.
#         """
#         self.database_path = database_path

#     def clear_tables(self):
#         """
#         Clear all tables in the database.
#         """
#         if os.path.exists(self.database_path):
#             db.reflect()
#             db.drop_all()
#             print("Tables & data deleted successfully!")
#         else:
#             print("No database found to delete.")

#     def delete_database(self):
#         """
#         Delete the entire database file along with its tables.
#         """
#         if os.path.exists(self.database_path):
#             db.reflect()
#             db.drop_all()
#             os.remove(self.database_path)
#             print("Database deleted successfully!")
#         else:
#             print("No database found to delete.")


# from database_backend import database_uri
# from flask_sqlalchemy import SQLAlchemy
# # from flask import current_app  # Import current_app for app context management
# import os

# db = SQLAlchemy()

# class DatabaseManager:
#     def __init__(self, database_path):
#         """
#         Initialize the DatabaseManager with the path to the database.
#         """
#         self.database_path = database_path

#     def clear_tables(self):
#         """
#         Clear all tables in the database.
#         """
#         if os.path.exists(self.database_path):
#             # with current_app.app_context():  # Ensure app context is active
#             db.reflect()
#             db.drop_all()
#             print("Tables & data deleted successfully!")
#         else:
#             print("No database found to delete.")

#     def delete_database(self):
#         """
#         Delete the entire database file along with its tables.
#         """
#         if os.path.exists(self.database_path):
#             # with current_app.app_context():  # Ensure app context is active
#             db.reflect()
#             db.drop_all()
#             os.remove(self.database_path)
#             print("Database deleted successfully!")
#         else:
#             print("No database found to delete.")


# database_backend/db_manager.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

class DatabaseManager:
    def __init__(self, database_path):
        """
        Initialize the DatabaseManager with the path to the database.
        """
        self.database_path = database_path
        # Create a temporary Flask app for database operations
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

    def clear_tables(self):
        """
        Clear all tables in the database.
        """
        if os.path.exists(self.database_path):
            with self.app.app_context():
                db.reflect()
                db.drop_all()
                db.create_all()  # Recreate the tables
                print("Tables & data deleted successfully!")
        else:
            print("No database found to delete.")

    def delete_database(self):
        """
        Delete the entire database file along with its tables.
        """
        if os.path.exists(self.database_path):
            with self.app.app_context():
                db.reflect()
                db.drop_all()
            os.remove(self.database_path)
            print("Database deleted successfully!")
        else:
            print("No database found to delete.")

    def initialize_database(self):
        """
        Initialize the database and create all tables.
        """
        with self.app.app_context():
            db.create_all()
            print("Database initialized successfully!")


# database_backend/db_manager.py

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# # Create base class for declarative models
# Base = declarative_base()

# class DatabaseManager:
#     def __init__(self, database_path):
#         """
#         Initialize the DatabaseManager with the path to the database.
        
#         Args:
#             database_path (str): Path to the SQLite database file
#         """
#         self.database_path = database_path
#         self.engine = create_engine(f'sqlite:///{database_path}')
#         self.Session = sessionmaker(bind=self.engine)
        
#     def initialize_database(self):
#         """
#         Create all tables in the database.
#         """
#         Base.metadata.create_all(self.engine)
#         print("Database initialized successfully!")

#     def clear_tables(self):
#         """
#         Clear all tables in the database while keeping the database file.
#         """
#         if os.path.exists(self.database_path):
#             Base.metadata.drop_all(self.engine)
#             Base.metadata.create_all(self.engine)
#             print("Tables & data deleted successfully!")
#         else:
#             print("No database found to delete.")

#     def delete_database(self):
#         """
#         Delete the entire database file along with its tables.
#         """
#         if os.path.exists(self.database_path):
#             Base.metadata.drop_all(self.engine)
#             os.remove(self.database_path)
#             print("Database deleted successfully!")
#         else:
#             print("No database found to delete.")

#     def get_session(self):
#         """
#         Get a new database session.
        
#         Returns:
#             Session: A new SQLAlchemy session
#         """
#         return self.Session()

# database_backend/db_manager.py

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import NullPool
# import os

# Base = declarative_base()

# class DatabaseManager:
#     def __init__(self, database_path):
#         """
#         Initialize the DatabaseManager with the path to the database.
        
#         Args:
#             database_path (str): Path to the SQLite database file
#         """
#         self.database_path = database_path
#         self.engine = create_engine(f'sqlite:///{database_path}', poolclass=NullPool)
#         self.Session = sessionmaker(bind=self.engine)

#     def initialize_database(self):
#         """
#         Create all tables in the database.
#         """
#         Base.metadata.create_all(self.engine)
#         print("Database initialized successfully!")

#     def clear_tables(self):
#         """
#         Clear all tables in the database while keeping the database file.
#         Ensures all connections are closed and tables are properly cleared.
#         """
#         try:
#             # Close any existing sessions
#             self.Session.close_all()
            
#             # Dispose of the engine to close all connections
#             self.engine.dispose()
            
#             if os.path.exists(self.database_path):
#                 # Drop all tables
#                 Base.metadata.drop_all(self.engine)
                
#                 # Recreate tables
#                 Base.metadata.create_all(self.engine)
                
#                 # Create a new session and commit to ensure changes are saved
#                 session = self.Session()
#                 session.commit()
#                 session.close()
                
#                 print("Tables & data deleted successfully!")
#             else:
#                 print("No database found to delete.")
#         except Exception as e:
#             print(f"Error clearing tables: {str(e)}")

#     def delete_database(self):
#         """
#         Delete the entire database file along with its tables.
#         Ensures all connections are closed before deletion.
#         """
#         try:
#             # Close any existing sessions
#             self.Session.close_all()
            
#             # Dispose of the engine to close all connections
#             self.engine.dispose()
            
#             if os.path.exists(self.database_path):
#                 # Drop all tables
#                 Base.metadata.drop_all(self.engine)
                
#                 # Remove the file
#                 os.remove(self.database_path)
                
#                 print("Database deleted successfully!")
#             else:
#                 print("No database found to delete.")
#         except Exception as e:
#             print(f"Error deleting database: {str(e)}")
            
#     def force_delete_database(self):
#         """
#         Forcefully delete the database file, closing all connections first.
#         Use this if regular delete_database() isn't working.
#         """
#         try:
#             # Close any existing sessions
#             self.Session.close_all()
            
#             # Dispose of the engine to close all connections
#             self.engine.dispose()
            
#             # Force close by creating a new engine without pooling
#             self.engine = create_engine(f'sqlite:///{self.database_path}', poolclass=NullPool)
            
#             if os.path.exists(self.database_path):
#                 # Try to remove the file directly
#                 os.remove(self.database_path)
#                 print("Database forcefully deleted successfully!")
#             else:
#                 print("No database found to delete.")
#         except Exception as e:
#             print(f"Error during force delete: {str(e)}")

#     def get_session(self):
#         """
#         Get a new database session.
        
#         Returns:
#             Session: A new SQLAlchemy session
#         """
#         return self.Session()




