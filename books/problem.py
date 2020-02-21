from typing import List


class Book:
    def __init__(self, value):
        self.value = value
        self.in_libraries = set()

    def add_to_library(self, library_id):
        self.in_libraries.add(library_id)


class Library:
    def __init__(
        self, number_of_books: int, signup_days: int, capacity: int, book_ids: List[int]
    ):
        assert number_of_books == len(
            book_ids
        ), "The number of books does not equal the size of book_ids passed"
        self.number_of_books = number_of_books
        self.signup_days = signup_days
        self.capacity = capacity
        self.book_ids = book_ids

    def remove_book(self, book_id: int):
        if book_id in self.book_ids:
            self.book_ids.remove(book_id)
            self.number_of_books -= 1

    def sort_books_by_value(self, books: List[Book]):
        self.book_ids.sort(key=lambda book_id: books[book_id].value, reverse=True)


class Problem:
    def __init__(
        self,
        number_of_books: int,
        number_of_libraries: int,
        number_of_days: int,
        book_values: List[int],
    ):
        self.number_of_books = number_of_books
        self.number_of_libraries = number_of_libraries
        self.number_of_days = number_of_days
        self.books: List[Book] = [Book(value) for value in book_values]
        self.libraries: List[Library] = []

    def append_library(self, library: Library):
        self.libraries.append(library)

    def remove_book(self, book_id):
        for library in self.libraries:
            library.remove_book(book_id)


class ScanningLibrary:
    def __init__(self, library_id: int):
        self.library_id = library_id
        self.book_ids: List[int] = []

    def queue_book(self, book_id: int):
        self.book_ids.append(book_id)


class Solution:
    def __init__(self):
        self.scanning_queue: List[ScanningLibrary] = []
        self.scanning_library_ids: List[int] = []

    def queue_library(self, library_id: int):
        self.scanning_queue.append(ScanningLibrary(library_id))
        self.scanning_library_ids.append(library_id)


def read(text: str) -> Problem:
    lines = text.split("\n")
    [number_of_books, number_of_libraries, number_of_days] = [
        int(i) for i in lines[0].split(" ")
    ]
    book_values = [int(i) for i in lines[1].split(" ")]
    problem = Problem(number_of_books, number_of_libraries, number_of_days, book_values)

    for index in range(2, len(lines) - 2, 2):
        if not lines[index]:
            continue
        [books_in_library, signup_days, capacity] = [
            int(i) for i in lines[index].split(" ")
        ]
        book_ids = [int(i) for i in lines[index + 1].split(" ")]

        problem.append_library(
            Library(books_in_library, signup_days, capacity, book_ids)
        )

    return problem


def write(solution: Solution) -> str:
    # remove empty scanning queues
    scanning_queue = [item for item in solution.scanning_queue if item.book_ids]
    result = f"{len(scanning_queue)}\n"
    for item in scanning_queue:
        description = f"{item.library_id} {len(item.book_ids)}"
        book_ids = " ".join(str(book_id) for book_id in item.book_ids)
        result += f"{description}\n{book_ids}\n"

    return result
