from datetime import datetime, timedelta
from typing import cast

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select

from src.main.com.gegunov.library.exceptions.BookAlreadyExistsException import BookAlreadyExistsException
from src.main.com.gegunov.library.exceptions.BookHasBorrowedInstancesException import BookHasBorrowedInstancesException
from src.main.com.gegunov.library.exceptions.BorrowNotFoundException import BorrowNotFoundException
from src.main.com.gegunov.library.exceptions.NoBooksAvailableException import NoBooksAvailableException
from src.main.com.gegunov.library.exceptions.ReaderAlreadyExistsException import ReaderAlreadyExistsException
from src.main.com.gegunov.library.exceptions.ReaderHasBorrowedBooksException import ReaderHasBorrowedBooksException
from src.main.com.gegunov.library.model.model import *


class LibraryManager:
    engine = create_engine('postgresql://postgres:qwerty@localhost/library')
    Session = sessionmaker(bind=engine)

    def add_book(self):
        title: str = input('Введите название книги: ')
        author: str = input('Введите автора книги: ')
        published_year: int = int(input('Введите год издания: '))
        qty: int = int(input('Введите кол-во: '))
        book: Book = Book(title=title, author=author, published_year=published_year, quantity=qty)

        with self.Session() as session:
            try:
                session.add(book)
                session.commit()
                print(f"A book {title} , {author}, {published_year} has been added")
            except sqlalchemy.exc.IntegrityError:
                raise BookAlreadyExistsException(f"Книга с названием {title} и автором {author} уже существует")

    def add_reader(self):
        name: str = input('Имя ')
        email: str = input('email ')
        reader: Reader = Reader(name=name, email=email)
        with self.Session() as session:
            try:
                session.add(reader)
                session.commit()
                print(f"reader {name} , {email} has been added")
            except sqlalchemy.exc.IntegrityError:
                raise ReaderAlreadyExistsException(f"Пользователь с email {email} уже существует")

    def get_readers_with_borrowed_books(self):
        with self.Session() as session:
            print(session.execute(
                select(Reader).join(Reader.borrows))
                  .scalars().all())

    def get_borrowed_books(self):
        with self.Session() as session:
            print(session.execute(select(BorrowedBook)).scalars().all())

    def borrow_book(self):
        book_id: int = int(input('Введите ID книги'))
        reader_id: int = int(input('Введите ID читателя'))

        with self.Session() as session:
            book: Book = session.execute(select(Book).where(
                cast("ColumnElement[bool]", Book.id == book_id)
            )).scalars().first()
            if book.quantity < 1:
                raise NoBooksAvailableException(f"Нет свободных книг {book.author}-{book.title}")
            reader: Reader = session.execute(select(Reader).where(
                cast("ColumnElement[bool]", Reader.id == reader_id)
            )).scalars().first()

            borrow: BorrowedBook = BorrowedBook(book_id=book_id, reader_id=reader_id, borrow_date=datetime.today(),
                                                return_date=(datetime.now() + timedelta(days=10)))
            book.quantity -= 1
            session.add(borrow)
            session.commit()

            print(f"книга {book} была успешно выдана пользователю {reader}, срок возврата - через 10 дней")

    def return_book(self):
        book_id: int = int(input('Введите ID книги: '))
        reader_id: int = int(input('Введите ID читателя: '))

        with self.Session() as session:
            borrow: BorrowedBook = session.execute(select(BorrowedBook).where(
                cast("ColumnElement[bool]", Book.id == book_id and Reader.id == reader_id))).scalars().first()

            if not borrow:
                raise BorrowNotFoundException(f"Выдача c ID книги {book_id} и ID читателя {reader_id} не найдена")

            book: Book = session.execute(select(Book).where(
                cast("ColumnElement[bool]", Book.id == book_id)
            )).scalars().first()

            book.quantity += 1
            session.delete(borrow)
            session.commit()
            print(f"Читатель [{borrow.reader}] сдал книгу [{book}] ")

    def get_all_books(self):
        with self.Session() as session:
            books = session.execute(select(Book).order_by(Book.published_year)).scalars().all()
            print(f"{books}")

    def delete_book(self):
        book_id: int = int(input('Введите ID книги'))
        with self.Session() as session:
            book: Book = session.execute(select(Book).where(
                cast("ColumnElement[bool]", Book.id == book_id)
            )).scalars().first()
            if len(book.borrows) > 0:
                raise BookHasBorrowedInstancesException(f"Книга {book} имеет выданные экземпляры. Удаление невозможно")

    def delete_reader(self):
        reader_id: int = int(input('Введите ID читателя'))
        with self.Session() as session:
            reader: Reader = session.execute(select(Reader).where(
                cast("ColumnElement[bool]", Reader.id == reader_id)
            )).scalars().first()
            if len(reader.borrows) > 0:
                raise ReaderHasBorrowedBooksException(
                    f"Читатель {reader} имеет выданные экземпляры. Удаление невозможно")

    def search_book_by_title(self):
        book_title = input("Введите название книги для поиска: ")
        with self.Session() as session:
            books = session.query(Book).filter(Book.title.like(f"%{book_title}%")).scalar()
            print(books)

    def search_book_by_author(self):
        book_author = input("Введите автора книги для поиска: ")
        with self.Session() as session:
            books = session.query(Book).filter(Book.author.like(f"%{book_author}%")).scalar()
            print(books)
