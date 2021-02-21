import logging
from typing import List

from tqdm import tqdm

from books.problem import Problem, Solution
from books.solvers.scan_choice import scan_choice

logger = logging.getLogger(__name__)


class ScheduledLibrary:
    def __init__(self, library_id: int, starting_day: int):
        self.library_id = library_id
        self.starting_day = starting_day

    def starting_today(self, day):
        return day == self.starting_day


def solve(problem: Problem) -> Solution:

    # sort books by value
    for library in problem.libraries:
        library.sort_books_by_value(problem.books)

    solution = Solution()
    scheduled_library_ids: List[ScheduledLibrary] = []

    # how many times do we want to do a signup round
    signup_rounds = 4
    signup_round = 0

    for day in tqdm(range(problem.number_of_days)):
        logger.debug("Starting day %s", day)
        if not scheduled_library_ids:
            new_signup_day = day
            signup_round += 1
            goal_day = signup_round * (problem.number_of_days / signup_rounds)
            logger.debug("Scheduling libraries until day %s", goal_day)

            ranked_library_ids = rank_libraries(
                problem, solution.scanning_library_ids, problem.number_of_days - day
            )
            while new_signup_day < goal_day and ranked_library_ids:
                new_signup_id = ranked_library_ids.pop(0)
                new_signup_day += problem.libraries[new_signup_id].signup_days
                scheduled_library_ids.append(
                    ScheduledLibrary(new_signup_id, new_signup_day)
                )
                logger.debug(
                    "Scheduled new library %s to start at day %s",
                    new_signup_id,
                    new_signup_day,
                )

        if scheduled_library_ids and scheduled_library_ids[0].starting_today(day):
            new_scheduled_id = scheduled_library_ids.pop(0).library_id
            solution.queue_library(new_scheduled_id)
            logger.debug("Signed up new library %s", new_signup_id)

        planned_books = scan_choice(problem, solution.scanning_library_ids)
        plan_books(problem, solution, planned_books)

    return solution


def plan_books(problem: Problem, solution: Solution, planned_books: dict):
    for place in solution.scanning_queue:
        book_ids_for_library = planned_books.get(place.library_id, [])
        place.book_ids.extend(book_ids_for_library)
        for book_id in book_ids_for_library:
            problem.remove_book(book_id)


def rank_libraries(
    problem: Problem, signed_libraries: List[int], days_left: int
) -> List[int]:
    ranked_libraries = []

    for library_id, _ in enumerate(problem.libraries):
        if library_id not in signed_libraries:
            value = library_value(library_id, problem, signed_libraries, days_left)
            ranked_libraries.append((value, library_id))

    ranked_libraries.sort(reverse=True)
    return [library_id for _, library_id in ranked_libraries]


def library_value(
    library_id: int, problem: Problem, signed_libraries: List[int], days_left: int
) -> float:
    library = problem.libraries[library_id]

    # how many books can it do
    book_capacity = (days_left - library.signup_days) * library.capacity

    # the greatest books should already be stored in front of the library list
    # divide by the number of libraries that are signed up with that book
    total_value = 0.0
    for book_id in library.book_ids[:book_capacity]:
        amount_of_libraries = 0
        for signed_library_id in signed_libraries:
            signed_library = problem.libraries[signed_library_id]
            if book_id in signed_library.book_ids:
                amount_of_libraries += 1
        total_value += float(problem.books[book_id].value / (amount_of_libraries + 1))

    logger.debug("Found value %s for library %s", total_value, library_id)
    return total_value
