from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from data_models import db, Author, Book

app = Flask(__name__)

import os
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('data/library.sqlite')}"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Handles the addition of authors to the database."""
    if request.method == 'GET':
        return render_template('add_author.html')
    elif request.method == 'POST':
        author_name = request.form.get('name')
        author_birthdate = request.form.get('birthdate')
        author_date_of_death = request.form.get('date_of_death')

        author = Author(
            name=author_name,
            birth_date=author_birthdate,
            date_of_death=author_date_of_death
        )
        db.session.add(author)
        db.session.commit()
        return "Author added successfully!", 201

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Handles the addition of books to the database."""
    if request.method == 'GET':
        authors_names_id = db.session.query(Author.name, Author.id).all()
        return render_template('add_book.html', authors=authors_names_id)
    elif request.method == 'POST':
        book_title = request.form.get('title')
        author_id = request.form.get('author_id')
        book_published_date = request.form.get('publication_year')
        book_isbn = request.form.get('isbn')

        book = Book(
            title=book_title,
            isbn=book_isbn,
            author_id=author_id,
            publication_year=book_published_date
        )
        db.session.add(book)
        db.session.commit()
        return "Book added successfully!", 201

@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the homepage with a list of books and search functionality."""
    if request.method == 'GET':
        books_with_authors = db.session.query(
            Book.id, Book.title, Author.name, Book.isbn, Book.publication_year
        ).join(Author).order_by(Book.title, Author.name).all()
        return render_template('home.html', books=books_with_authors)
    elif request.method == 'POST':
        search_q = request.form.get("searchInput")
        books_with_authors = db.session.query(
            Book.title, Author.name, Book.isbn, Book.publication_year
        ).join(
            Author
        ).filter(
            or_(
                Book.title.ilike(f"%{search_q}%"),
                Author.name.ilike(f"%{search_q}%")
            )
        ).order_by(Book.title, Author.name).all()
        if books_with_authors:
            return render_template('home.html', books=books_with_authors), 201
        else:
            return render_template('home.html', books=None), 401

@app.route('/delete-book/<int:_id>', methods=['POST'])
def delete_book(_id):
    """Deletes a book by ID and removes the author if they have no remaining books."""
    book = Book.query.get(_id)
    if not book:
        return "Book not found", 404

    author_id = book.author_id
    author = Author.query.get(author_id)

    db.session.delete(book)
    db.session.commit()

    remaining_author_ids = db.session.query(Book.author_id).all()
    remaining_author_ids = [id_tuple[0] for id_tuple in remaining_author_ids]

    if author_id not in remaining_author_ids:
        db.session.delete(author)

    db.session.commit()
    return "done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
