# import os
# import pandas as pd
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from server import Book  # Import your Book model from server.py

# os.chdir('/Users/alexdubro/Documents/Programming Tools/GitHub Projects/Udemy Learning/100 Days of Code (Udemy)/Assignments/Day 63 - SQLite & SQLAlchemy/instance')
# DATABASE_URI = 'sqlite:///books.db'  # Replace with your actual database URI
# engine = create_engine(DATABASE_URI)

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Query using the ORM
# books = session.query(Book).all()

# # Convert the result to a Pandas DataFrame
# df = pd.DataFrame([name.__dict__ for name in books])  # Use __dict__ to get the attributes of each Book

# # Drop the SQLAlchemy internal _sa_instance_state column
# df = df.drop(columns=['_sa_instance_state'])

# print(df.head())

# # Close the session
# # session.close()

# # if __name__ == "__main__":
# #     app.run(debug=True)

# analysis.py
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server import Book

# Set up the database connection
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'books.db')
DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def analyze_books():
    try:
        # Query using the ORM
        books = session.query(Book).all()

        # Convert to DataFrame
        df = pd.DataFrame([{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'rating': book.rating
        } for book in books])

        # Perform your analysis
        print("\nBasic Statistics:")
        print("=================")
        print(f"Total number of books: {len(df)}")
        print(f"\nAverage rating: {df['rating'].mean():.2f}")
        print(f"Highest rated book: {df.loc[df['rating'].idxmax(), 'title']}")
        print(f"Lowest rated book: {df.loc[df['rating'].idxmin(), 'title']}")
        
        print("\nRatings Distribution:")
        print("====================")
        print(df['rating'].value_counts().sort_index())
        
        print("\nAuthors with multiple books:")
        print("=========================")
        author_counts = df['author'].value_counts()
        print(author_counts[author_counts > 1])

        return df
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None
    
    finally:
        session.close()

def main():
    df = analyze_books()
    if df is not None:
        # Additional analysis or export if needed
        df.to_csv('book_analysis.csv', index=False)
        print("\nAnalysis exported to 'book_analysis.csv'")

if __name__ == "__main__":
    main()