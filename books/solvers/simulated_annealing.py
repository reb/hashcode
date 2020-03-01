import logging
import random
from typing import List

from books.problem import Problem, Solution

logger = logging.getLogger(__name__)


def solve(problem: Problem) -> Solution:
    random.seed("simulated_annealing")

    # start with a random order
    library_ids_order = [library_id for library_id in range(problem.number_of_libraries)]
    random.shuffle(library_ids_order)

    logger.debug("Found solution with value %s", value(library_ids_order, problem))
    return to_solution(library_ids_order, problem)


def value(library_ids_order: List[int], problem: Problem) -> int:
    day = 0
    scanned_book_ids = set()
    total_value = 0

    for library_id in library_ids_order:
        library = problem.libraries[library_id]
        day += library.signup_days
        if day >= problem.number_of_days:
            break

        library_capacity = (problem.number_of_days - day) * library.capacity
        library_book_ids = library.book_ids_set - scanned_book_ids
        new_book_ids = sorted(library_book_ids,
                              key=lambda book_id: problem.books[book_id].value,
                              reverse=True)[:library_capacity]

        total_value += sum(problem.books[book_id].value for book_id in new_book_ids)

        scanned_book_ids.update(new_book_ids)

    return total_value


def to_solution(library_ids_order: List[int], problem: Problem) -> Solution:
    day = 0
    scanned_book_ids = set()
    solution = Solution()

    for library_id in library_ids_order:
        library = problem.libraries[library_id]
        day += library.signup_days
        if day >= problem.number_of_days:
            break

        solution.queue_library(library_id)

        capacity = (problem.number_of_days - day) * library.capacity
        library_book_ids = library.book_ids_set - scanned_book_ids
        new_book_ids = sorted(library_book_ids,
                              key=lambda book_id: problem.books[book_id].value,
                              reverse=True)[:capacity]

        for book_id in new_book_ids:
            solution.scanning_queue[-1].queue_book(book_id)

        scanned_book_ids.update(new_book_ids)

    return solution

