# Flask Book Management Application

This is a simple Flask application for managing books in a SQLite database. The application allows users to create, read, update, and delete books from the database.

## Installation

To get started with this application, you will need to have Python 3.x and install the dependencies in the requirements.txt to your system. You can install the dependencies using pip:

```bash
pip install flask
```

## Running the Application

Save this code as `app.py` and run it using the following command:

```bash
python app.py
```

By default, the application will start on port 5000. You can access it in your web browser at http://127.0.0.1:5000/.

## Database Models

The application uses a SQLite database to store book information. The `Book` model represents each book with its title, author, and rating attributes.

```python
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
```

## Routes

### Home Route (`/`)

The home route displays all books in the database and an empty message if there are no books.

### Add Book Route (`/add`)

The add book route allows users to add a new book to the database by filling out a form with the book's title, author, and rating. If the user submits invalid data or tries to submit a rating outside the valid range (1-10), an error message is displayed, and they are redirected back to the add book page.

### Edit Book Route (`/edit`)

The edit book route allows users to update the information of an existing book in the database. It displays a form prefilled with the selected 
book's data for easy editing. Users can update the title, author, and rating of the book by submitting the form. If the user submits invalid 
data or tries to submit a rating outside the valid range (1-10), an error message is displayed, and they are redirected back to the edit book page.

### Delete Book Route (`/delete`)

The delete book route allows users to remove a book from the database by selecting the book they want to delete from the list of books on the home page.

## HTML Templates

HTML Templates for this application are located in the `templates` directory:

- `index.html`: The HTML template for displaying the list of books and an empty message if there are no books. It also includes forms to add, edit, or delete a book.
- `add.html`: The HTML template for adding a new book.
- `edit.html`: The HTML template for editing a book's information, prefilled with the selected book's data.

## Future Improvements

This application can be further improved by adding more features such as:

- Pagination for displaying books if the number of books in the database becomes large.
- Search functionality to quickly find specific books.
- Add validation for form inputs to ensure only valid data is entered (e.g., alphabetical characters for titles and authors, numerical values for ratings).
