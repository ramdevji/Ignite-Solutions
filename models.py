from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = 'books_author'
    id = Column(Integer, primary_key=True, index=True)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)
    name = Column(String, index=True)

    books = relationship("Book", secondary="books_book_authors", back_populates="authors")


class Book(Base):
    __tablename__ = 'books_book'
    id = Column(Integer, primary_key=True, index=True)
    download_count = Column(Integer, default=0)
    gutenberg_id = Column(Integer, unique=True, index=True)
    media_type = Column(String)
    title = Column(String, index=True)

    authors = relationship("Author", secondary="books_book_authors", back_populates="books")
    languages = relationship("Language", secondary="books_book_languages", back_populates="books")
    subjects = relationship("Subject", secondary="books_book_subjects", back_populates="books")
    bookshelves = relationship("Bookshelf", secondary="books_book_bookshelves", back_populates="books")
    formats = relationship("Format", back_populates="book")


class BooksBookAuthors(Base):
    __tablename__ = 'books_book_authors'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'))
    author_id = Column(Integer, ForeignKey('books_author.id'))


class BooksBookLanguages(Base):
    __tablename__ = 'books_book_languages'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'))
    language_id = Column(Integer, ForeignKey('books_language.id'))


class BooksBookSubjects(Base):
    __tablename__ = 'books_book_subjects'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'))
    subject_id = Column(Integer, ForeignKey('books_subject.id'))


class BooksBookBookshelves(Base):
    __tablename__ = 'books_book_bookshelves'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'))
    bookshelf_id = Column(Integer, ForeignKey('books_bookshelf.id'))


class Bookshelf(Base):
    __tablename__ = 'books_bookshelf'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", secondary="books_book_bookshelves", back_populates="bookshelves")


class Format(Base):
    __tablename__ = 'books_format'
    id = Column(Integer, primary_key=True, index=True)
    mime_type = Column(String, index=True)
    url = Column(String)
    book_id = Column(Integer, ForeignKey('books_book.id'))

    book = relationship("Book", back_populates="formats")


class Language(Base):
    __tablename__ = 'books_language'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)

    books = relationship("Book", secondary="books_book_languages", back_populates="languages")


class Subject(Base):
    __tablename__ = 'books_subject'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", secondary="books_book_subjects", back_populates="subjects")
