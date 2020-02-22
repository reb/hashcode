from unittest import TestCase
from books.problem import Library, Problem
from books.solvers.bookworm import library_value


class BookwormTest(TestCase):
    def test_library_value_single(self):
        problem = Problem(4, 1, 2, [10, 20, 30, 40])
        library = Library(4, 1, 1, [0, 1, 2, 3])
        library.sort_books_by_value(problem.books)
        problem.append_library(library)

        value = library_value(0, problem, [], 2)
        self.assertEqual(40, value)

    def test_library_value_triple(self):
        problem = Problem(3, 1, 3, [1, 1, 1])
        library_0 = Library(2, 1, 2, [0, 2])
        library_1 = Library(1, 1, 2, [1])
        library_2 = Library(2, 0, 2, [0, 1])

        problem.append_library(library_0)
        problem.append_library(library_1)
        problem.append_library(library_2)

        self.assertEqual(1.5, library_value(0, problem, [2], 2))
