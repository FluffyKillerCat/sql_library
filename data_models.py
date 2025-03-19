from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):  # Added .Model to make it valid
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Author(author_id={self.id}, name={self.name})"

    def __str__(self):
        return f"Fun fact: {self.name} lived to be {(self.date_of_death - self.birth_date).days // 365} years old"


class Book(db.Model):  # Added .Model to make it valid
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer)
    title = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return f"Book(book_id={self.id}, name={self.title})"

    def __str__(self):
        return f"{self.title}'s ISBN is {self.isbn}"

