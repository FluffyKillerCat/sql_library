from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# Initialize the Flask application
app = Flask(__name__)

# Set the database URI for SQLAlchemy
import os
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('data/library.sqlite')}"

# Initialize the database with the app
db.init_app(app)

# Create the database tables within the app context (one-time use)
"""
with app.app_context():
    db.create_all()
"""

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
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
    if request.method == 'GET':
        # Render the form for adding a book
        return render_template('add_book.html')
    elif request.method == 'POST':
        # Get form data
        book_title = request.form.get('title')
        book_author_id = request.form.get('author_id')
        book_published_date = request.form.get('published_date')
        book_summary = request.form.get('summary')

        # Create an instance of the Book model
        book = Book(
            title=book_title,
            author_id=book_author_id,  # Assuming you are linking a book to an author using their ID
            published_date=book_published_date,
            summary=book_summary
        )

        # Add the new book to the database
        db.session.add(book)
        db.session.commit()

        return "Book added successfully!"  # Success message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
