# import pandas as pd
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
# import os
# from datetime import datetime

from celery import shared_task
from celery.contrib.abortable import AbortableTask


from multiprocessing import Process
import os
import pandas as pd
from sqlalchemy import select, create_engine
from server import app, Book  # Import Book from server.py

# @shared_task(bind=True, base=AbortableTask)
def analyze_books():
    # Get the absolute path of the current file's directory
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Create the database URI by joining the path and database name
    database_path = os.path.join(basedir, 'books.db')

    # Create the engine (adjust the URI to match your setup)
    DATABASE_URI = f'sqlite:///{database_path}'  # Match this with your database path in server.py
    engine = create_engine(DATABASE_URI)

    # Execute the query and load data into a DataFrame
    with engine.connect() as connection:
        stmt = select(Book.title, Book.author, Book.rating)  # Define the columns you want
        df = pd.read_sql(stmt, connection)  # Read directly into a DataFrame

    # Print the DataFrame and its type to verify
    # print("Type:", type(df))
    print(df)

if __name__ == "__main__":
    # app.run(debug=True)
    # p = Process(target=analyze_books)
    # p.start()
    # p.join()
    analyze_books()
    app.run(debug=True, use_reloader=False)

# Get the absolute path of the current file's directory
# basedir = os.path.abspath(os.path.dirname(__file__))

# # Create the database URI by joining the path and database name
# database_path = os.path.join(basedir, 'books.db')
# class BookAnalyzer(Process):
#     def __init__(self, db_path=database_path):
#         super().__init__()
#         self.db_path = db_path
#         self.engine = create_engine(f'sqlite:///{db_path}')
#         self.output_dir = 'analysis_results'
#         os.makedirs(self.output_dir, exist_ok=True)

#     def run(self):
#         """Main process that runs independently"""
#         print(f"Starting analysis process at {datetime.now()}")
#         # df = self.extract()
#         # if df is not None:
#         #     analysis = self.transform(df)
#         #     self.load(analysis)

#     def extract(self):
#         """Extract data from database"""
#         try:
#             df = pd.read_sql("SELECT * FROM books", self.engine)
#             print(f"Extracted {len(df)} books from database")
#             return df
#         except Exception as e:
#             print(f"Extraction error: {e}")
#             return None

    # def transform(self, df):
    #     """Transform the data"""
    #     print("Transforming data...")
    #     analysis = {
    #         'total_books': len(df),
    #         'average_rating': round(df['rating'].mean(), 2),
    #         'ratings_dist': df['rating'].value_counts().to_dict(),
    #         'authors': df['author'].value_counts().to_dict(),
    #         'timestamp': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    #     }
    #     return analysis

    # def load(self, analysis):
    #     """Save analysis results"""
    #     print("Saving analysis results...")
    #     timestamp = analysis['timestamp']
        
    #     # Save numerical analysis to CSV
    #     results_df = pd.DataFrame([analysis])
    #     results_df.to_csv(f'{self.output_dir}/analysis_{timestamp}.csv')

    #     # Create and save visualizations
    #     self.create_visualizations(analysis, timestamp)
        
    #     print(f"Analysis complete! Results saved in {self.output_dir}")

    # def create_visualizations(self, analysis, timestamp):
    #     """Create visualization plots"""
    #     # Ratings distribution
    #     plt.figure(figsize=(10, 6))
    #     ratings = pd.Series(analysis['ratings_dist'])
    #     ratings.plot(kind='bar')
    #     plt.title('Book Ratings Distribution')
    #     plt.tight_layout()
    #     plt.savefig(f'{self.output_dir}/ratings_dist_{timestamp}.png')
    #     plt.close()

# Usage example
# if __name__ == "__main__":
    # Create and start the analyzer process
    # analyzer = BookAnalyzer()
    # analyzer.extract()
    
    # # This will run immediately, showing that the main program continues
    # print("Main program continues running...")
    # print("You can do other things while the analysis runs...")
    
    # # If you want to wait for the analysis to complete before exiting
    # analyzer.join()
    # print("Analysis process completed!")