from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    published_year = Column(Integer)
    quantity = Column(Integer, nullable=False)
    borrows = relationship('BorrowedBook', back_populates="book")
    __table_args__ = (UniqueConstraint('title', 'author', name='_title_author_uc'),
                      )

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.title}, author={self.author}, qty={self.quantity})>"


class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    borrows = relationship('BorrowedBook', back_populates="reader")

    def __repr__(self):
        return f"<Reader(id={self.id}, name={self.name}, email={self.email})>"


class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)

    book = relationship('Book', back_populates='borrows')
    reader = relationship('Reader', back_populates='borrows')

    def __repr__(self):
        return f"[{self.book}] borrowed by [{self.reader}]. Borrow date: [{self.borrow_date}]. Return date: [{self.return_date}] "
