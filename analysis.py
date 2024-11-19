# from database_backend import database_uri
# import os
# import pandas as pd
# # from multiprocessing import Process
# from sqlalchemy import select, create_engine
# from server import app, Book  # Import Book from server.py
# import threading
# import time

# def analyze_books():
#     # Create the engine (adjust the URI to match your setup)
#     engine = create_engine(database_uri())

#     # Execute the query and load data into a DataFrame
#     # if os.path.exists(database_uri()):
#     while os.path.exists(database_uri()):
#         with engine.connect() as connection:
#             stmt = select(Book.title, Book.author, Book.rating)  # Define the columns you want
#             df = pd.read_sql(stmt, connection)  # Read directly into a DataFrame
#             print(df)
#             time.sleep(5)
#         # if os.path.exists(database_uri()):
#         #     while os.path.exists(database_uri()):
#         #         print(df)
#         #         time.sleep(5)

#         # Print the DataFrame

#         # dt = datetime.now()
#         # print("Date and time is:", dt)
#         # print("Database file exists!")
#         # time.sleep(5)  # Check every 5 minutes (adjust as needed)
#     # while os.path.exists(database_uri()):
#     #     print(df)
#     #     time.sleep(5)

# if __name__ == "__main__":
#     # Analyze the database with a pandas dataframe
#     db_analyze_books = threading.Thread(target=analyze_books, daemon=True)
#     db_analyze_books.start()

#     # Run the Flask app
#     app.run(debug=True, use_reloader=False)


from database_backend import database_uri
import os
import pandas as pd
from sqlalchemy import select, create_engine
from server import app, Book
import threading
import time

def analyze_books():
    # Create the engine
    engine = create_engine(database_uri())

    # if os.path.exists(database_uri()):
    with engine.connect() as connection:
        # Define and execute the query, load data into a DataFrame
        stmt = select(Book.title, Book.author, Book.rating)
        df = pd.read_sql(stmt, connection)
        
        # Print the DataFrame
        print(df)

def run_analysis_periodically(interval=5):
    while True:
        analyze_books()
        time.sleep(interval)

if __name__ == "__main__":
    # Start the analysis in a separate thread
    db_analyze_books = threading.Thread(target=run_analysis_periodically, daemon=True)
    db_analyze_books.start()

    # Run the Flask app
    app.run(debug=True, use_reloader=False)
