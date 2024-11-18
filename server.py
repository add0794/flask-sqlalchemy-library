from database_backend import *
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import matplotlib.pyplot as plt
# from multiprocessing import Process
import pandas as pd
from sqlalchemy import Integer, String, create_engine
# import threading

# Create the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "books"

# Create the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the Book model and map it to the database table
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

app.app_context().push()
db.create_all()

@app.route("/")
def home(name=None):
    # Execute your query to get the result set
    result_set = db.session.query(Book).all()

    # Check if the result set is empty
    is_empty = not result_set

    # READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_books = result.scalars()
    return render_template('index.html', books=all_books, is_empty=is_empty)

@app.route("/search", methods=["GET"])
def search():
    # q = request.args.get('q')  # Get the search query from the URL parameters
    # if q:
    #     # Apply the filter to search for books by title containing the query string
    #     results = Book.query.filter(Book.title.contains(q)).all()
    # else:
    #     results = []  # Return an empty list if there's no search term
    q = request.args.get('q', '')
    search = f"%{q}%"
    results = Book.query.filter(
    or_(
        Book.id.ilike(search),
        Book.title.ilike(search),
        Book.author.ilike(search),
        Book.rating.ilike(search),
    )).all() if q else []
    return render_template("search.html", results=results)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        rating = int(request.form["rating"])
        if rating < 1 or rating > 10:
            flash("Error: Rating must be between 1 and 10.", "error")
            return redirect(url_for('add'))
        
        # If rating is valid, create new book
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=rating
        )
        
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for('home'))
    
    return render_template('add.html')

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)

        # Track whether any field has been successfully updated
        updated = False

        # Update title if form input is not empty and different
        if request.form["title"]:
            if book_to_update.title != request.form["title"]:
                book_to_update.title = request.form["title"]
                updated = True

        # Update author if form input is not empty and different
        if request.form["author"]:
            if book_to_update.author != request.form["author"]:
                book_to_update.author = request.form["author"]
                updated = True

        # Update rating if form input is not empty and different
        if request.form["rating"]:
            rating = float(request.form["rating"])  # Ensure the rating is an integer
            if book_to_update.rating != rating:
                book_to_update.rating = rating
                updated = True

        # If no fields were updated, show an error message
        if not updated:
            flash("Error: Edit any or all boxes must be edited or return to library.", "error")
            return redirect(url_for('edit', id=book_id))

        # Commit the updates to the database
        db.session.add(book_to_update)
        db.session.commit()
        flash("Book updated successfully!", "success")
        return redirect(url_for('home'))  # Redirect to home page after successful edit

    # GET request: Render the edit form
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template('edit.html', book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    flash("Book deleted successfully!", "success")
    return redirect(url_for('home'))

@app.route('/analyze', methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        flash("Analysis complete!", "info")
        engine = create_engine(database_uri())

        with engine.connect() as connection:
            # Get the column and value from the form
            column = request.form.get("column")
            value = request.form.get("value")
            
            # Basic input validation to prevent SQL injection
            valid_columns = ["id", "title", "author", "rating"]
            if column not in valid_columns:
                flash("Invalid column name. Please choose a valid column.", "danger")
                return render_template("analyze.html", df_html=None)
            
            # Build the query dynamically based on user input
            try:
                query = f"SELECT * FROM books WHERE {column} = :value"
                df = pd.read_sql(query, connection, params={"value": value})
                
                # Check if the DataFrame has data
                if df.empty:
                    flash(f"No records found for {column} = '{value}'.", "info")
                    df_html = "<p>No results found.</p>"
                else:
                    # Convert DataFrame to HTML table
                    df_html = df.to_html(classes="table table-striped", index=False)
            except Exception as e:
                flash(f"Error occurred: {e}", "danger")
                df_html = None
            
            return render_template("analyze.html", df_html=df_html)
    
    # Render the initial analyze page
    return render_template("analyze.html", df_html=None)


# @app.route('/plot', methods=["GET", "POST"])
# def plot():
#     if request.method == "POST":


if __name__ == "__main__":
    # Option 1: Threading
    # db_check_thread = threading.Thread(target=check_database_file, daemon=True)
    # db_check_thread.start()

    app.run(debug=True, use_reloader=False)

    # Option 2: Multiprocessing

    # p1 = multiprocessing.Process(target=app.run(debug=True, use_reloader=False))
    # p2 = multiprocessing.Process(target=check_database_file)
   
    # p1.start()
    # p2.start()

    # p1.join()
    # p2.join()