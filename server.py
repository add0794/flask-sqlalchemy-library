import db_init
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# import sqlite3

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

all_books = []

# SQLite version
# db = sqlite3.connect("books-collection.db") # creates the database
# cursor = db.cursor() # creates the cursor
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)") # creates the table
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')") # inserts an entry into the tab;e
# db.commit() # ensures that the entry is placed
# db.close()

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///new-books-collection.db'
# initialize the app with the extension
db.init_app(app)


class Book(db.Model):
    # __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home(name=None):
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        rating = request.form.get('rating')
        all_books.append({'title': title, 'author': author, 'rating': rating})
        # new_book = {
        #     "title": request.form["title"],
        #     "author": request.form["author"],
        #     "rating": request.form["rating"]
        # }
        # all_books.append(new_book)
        return redirect(url_for("home"))
    return render_template('add.html')


# @app.route("/edit", methods=["GET", "POST"])
# def edit():
#     # if request.method == "PUT":
#     #     book_id = request.form["id"]
#     #     book_to_update = db.get_or_404(Book, book_id)
#     #     book_to_update.rating = request.form["rating"]
#     #     db.session.commit()
#     #     return redirect(url_for('home'))
#     # return render_template('edit.html')
#     id = request.args.get('id')
#     book_selected = db.get_or_404(books, id)
#     if request.method == 'POST':
#         book_selected.rating = request.form['rating']
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template('edit.html', book=book_selected)

# def edit():
#     id = request.args.get('id')
#     book_selected = books.query.get_or_404(id)

#     if request.method == 'POST':
#         book_selected.rating = request.form['rating']
#         db.session.commit()
#         return redirect(url_for('home'))

#     return render_template('edit.html', book=book_selected)

@app.route('/edit', methods=['GET', 'POST'])
def edit(id):
    the_book = Book.query.get(id)
 
    if request.method == 'POST':
        the_book.rating = request.form['new-rating']
        db.session.commit()
        return redirect(url_for('home'))
 
    return render_template("edit_rating.html", book=the_book)

# @app.route("/edit", methods=["GET", "POST"])
# def edit():
#     if request.method == "POST":
#         #UPDATE RECORD
#         book_id = request.form["id"]
#         book_to_update = db.get_or_404(Book, book_id)
#         book_to_update.rating = request.form["rating"]
#         db.session.commit()
#         return redirect(url_for('home'))
#     book_id = request.args.get('id')
#     book_selected = db.get_or_404(Book, book_id)
#     return render_template("edit_rating.html", book=book_selected)
    # book = Book.query.get_or_404()

    # if request.method == "POST":
    #     new_rating = request.form.get('rating')
    #     if new_rating is not None:
    #         # Update the book's rating in the database
    #         book.rating = new_rating
    #         db.session.commit()
    #         return redirect(url_for('home'))

    # return render_template('edit.html', book=book)

        #     rating = request.form.get('rating')
    #     # all_books.append({'title': title, 'author': author, 'rating': rating})
    #     # new_book = {
    #     #     "title": request.form["title"],
    #     #     "author": request.form["author"],
    #     #     "rating": request.form["rating"]
    #     # }
    #     # all_books.append(new_book)
    #     return redirect(url_for("home"))
    # return render_template('edit.html')

    # book_id = request.form.get('title')
    # if request.method == "PUT":
    #     new_rating = request.form.get('rating')
        # if new_rating is not None:
        #     try:
        #         all_books[index]["rating"] = int(new_rating)
        #         return redirect(url_for("home"))
        #     except IndexError:
        #         return "Index out of range", 404
        #     except ValueError:
        #         return "Invalid rating value", 400
        # else:
        #     return "Missing 'rating' in form data", 400


# @app.route("/delete", methods=["DELETE"])


if __name__ == "__main__":
    app.run(debug=True)

