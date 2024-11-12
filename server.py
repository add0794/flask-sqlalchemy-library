from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float

# Create the Flask application
app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "books"

# Create the SQLAlchemy extension and specify the base class
Base = declarative_base()
db = SQLAlchemy(model_class=Base)

# Define the Book model and map it to the database table
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.init_app(app) # Initialize the Flask application with the SQLAlchemy extension
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

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            # Get the rating and validate it first
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
            
        except ValueError:
            flash("Error: Rating must be a valid number.", "error")
            return redirect(url_for('add'))
        except Exception as e:
            db.session.rollback()
            flash("Error adding book.", "error")
            return redirect(url_for('add'))
    
    return render_template('add.html')

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # Retrieve book ID from form data instead of URL arguments in POST request
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)

        # Update title if form input is not empty
        if request.form["title"]:
            book_to_update.title = request.form["title"]

        # Update author if form input is not empty
        if request.form["author"]:
            book_to_update.author = request.form["author"]

        # Update rating if form input is not empty and within valid range
        if request.form["rating"]:
            try:
                rating = int(request.form["rating"])
                if rating < 1 or rating > 10:
                    flash("Error: Rating must be between 1 and 10.", "error")
                    return redirect(url_for('edit', id=book_id))
                else:
                    book_to_update.rating = rating
            except ValueError:
                flash("Error: Rating must be a valid number.", "error")
                return redirect(url_for('edit', id=book_id))

        # Save the updated book to the database
        db.session.add(book_to_update)
        db.session.commit()
        flash("Book updated successfully!", "success")
        return redirect(url_for('home'))  # Redirect to home page after successful edit

    # Retrieve the selected book to pass to the edit template
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Book, book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    flash("Book deleted successfully!", "success")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)