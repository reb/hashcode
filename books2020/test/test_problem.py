from unittest import TestCase
from books.problem import Book, Library


class TestLibrary(TestCase):
    def test_remove_book(self):
        library = Library(5, 2, 2, [4, 2, 6, 9, 10])

        library.remove_book(6)
        self.assertEqual(
            4,
            library.number_of_books,
            "number_of_books is not updated after removing book_id 6",
        )
        self.assertEqual(
            [4, 2, 9, 10],
            library.book_ids,
            "book_ids is not updated after removing book_id 6",
        )

        library.remove_book(1)
        self.assertEqual(
            4,
            library.number_of_books,
            "number_of_books changed after removing a book that's not in the library",
        )
        self.assertEqual(
            [4, 2, 9, 10],
            library.book_ids,
            "book_ids changed after removing a book that's not in the library",
        )

    def test_sort_books_by_value(self):
        library = Library(5, 2, 2, [3, 2, 5, 8, 10])
        books = [Book(value) for value in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        library.sort_books_by_value(books)
        self.assertEqual(
            [10, 8, 5, 3, 2],
            library.book_ids,
            "book_ids is not properly sorted by value",
        )
