from src.main.com.gegunov.library.exceptions.BaseLibraryException import BaseLibraryException
from src.main.com.gegunov.library.service.LibraryManager import LibraryManager

if __name__ == '__main__':
    reader_manager: LibraryManager = LibraryManager()

    while True:
        print('Добро пожаловать в систему управления библиотекой')
        print('Введите необходимое действие')
        print('1 - Добавить нового читателя')
        print('2 - Вывести список читателей, у которых есть хотя бы 1 книга ')
        print('3 - Добавление новой книги в базу')
        print('4 - Выдача книги')
        print('5 - Возврат книги')
        print('6 - Вывести список книг, у которых есть хотя бы 1 читатель')
        print('7 - Список всех книг')
        print('8 - Удаление книги')
        print('9 - Удаление читателя')
        print('10 - Поиск книги по названию')
        print('11 - Поиск книги по автору')

        try:
            num = int(input("Введите число: "))
            if num == 1:
                reader_manager.add_reader()
            elif num == 2:
                reader_manager.get_readers_with_borrowed_books()
            elif num == 3:
                reader_manager.add_book()
            elif num == 4:
                reader_manager.borrow_book()
            elif num == 5:
                reader_manager.return_book()
            elif num == 6:
                reader_manager.get_borrowed_books()
            elif num == 7:
                reader_manager.get_all_books()
            elif num == 8:
                reader_manager.delete_book()
            elif num == 9:
                reader_manager.delete_reader()
            elif num == 10:
                reader_manager.search_book_by_title()
            elif num == 11:
                reader_manager.search_book_by_author()
        except BaseLibraryException as exc:
            print(exc)
        print('\n\n\n\n')
