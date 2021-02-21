import logging
from typing import List, Set

from tqdm import tqdm

from books2020.problem import Problem, Solution

logger = logging.getLogger(__name__)


def solve(problem: Problem) -> Solution:
    libraries = problem.libraries
    for library in libraries:
        library.sort_books_by_value(problem.books)

    solution = Solution()
    day = 0

    progress_bar = tqdm(total=problem.number_of_days, position=0, leave=True)
    while day < problem.number_of_days and len(solution.scanning_queue) < len(
        problem.libraries
    ):
        logger.debug("Picking a new library at day %s", day)

        # pick the highest valued library
        best_library_id = rank_libraries(
            problem, solution.scanning_library_ids, problem.number_of_days - day
        )[0]
        best_library = problem.libraries[best_library_id]
        logger.debug("Picked library %s", best_library_id)

        # update the day we're on
        day += best_library.signup_days
        progress_bar.update(best_library.signup_days)

        # add the library with all it's best books to the scanning queue
        scan_capacity = (problem.number_of_days - day) * best_library.capacity
        logger.debug(
            "Trying to queue %s books starting from day %s because the capacity is %s per day",
            scan_capacity,
            day,
            library.capacity,
        )
        solution.queue_library(best_library_id)
        for book_id in best_library.book_ids[:scan_capacity]:
            solution.scanning_queue[-1].queue_book(book_id)
            problem.remove_book(book_id)

    return solution


def rank_libraries(
    problem: Problem, signed_libraries: Set[int], days_left: int
) -> List[int]:
    ranked_libraries = []

    for library_id, _ in enumerate(problem.libraries):
        if library_id not in signed_libraries:
            value = library_value(library_id, problem, days_left)
            ranked_libraries.append((value, library_id))

    ranked_libraries.sort(reverse=True)
    return [library_id for _, library_id in ranked_libraries]


def library_value(library_id: int, problem: Problem, days_left: int) -> float:
    library = problem.libraries[library_id]

    # how many books can it do
    book_capacity = (days_left - library.signup_days) * library.capacity

    # the greatest books should already be stored in front of the library list
    total_value = sum(
        problem.books[book_id].value for book_id in library.book_ids[:book_capacity]
    )
    corrected_value = float(total_value / (2 * library.signup_days))
    logger.debug("Found value %s for library %s", corrected_value, library_id)
    return corrected_value
