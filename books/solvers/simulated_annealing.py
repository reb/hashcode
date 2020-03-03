import logging
import math
import random
from typing import List

from tqdm import tqdm

from books.problem import Problem, Solution

logger = logging.getLogger(__name__)


def solve(problem: Problem) -> Solution:
    # seed solution so we have the same random values for debug purposes
    # random.seed("simulated_annealing")

    steps = int(problem.number_of_libraries * (problem.number_of_libraries - 1) / 2)

    # max value of the solution is all books
    temperature = 10_000.0
    reduction_rate = float(temperature / steps)

    # start with a random order
    library_ids_order = [library_id for library_id in range(problem.number_of_libraries)]
    random.shuffle(library_ids_order)
    current_value = value(library_ids_order, problem)

    # do simulated annealing
    pbar = tqdm(range(steps))
    pbar.set_postfix_str(f"{current_value:,}")
    for _ in pbar:
        new_order = random_swap(library_ids_order)
        new_value = value(new_order, problem)
        if accept_new(current_value, new_value, temperature):
            if new_value != current_value:
                pbar.set_postfix_str(f"{new_value:,}")
            current_value = new_value
            library_ids_order = new_order
            logger.debug("Accepting solution with value %s", new_value)

        temperature -= reduction_rate

    return to_solution(library_ids_order, problem)


def accept_new(current_value: int, new_value: int, temperature: float) -> bool:
    if current_value <= new_value:
        return True
    # simulated annealing acceptance probability
    acceptance_probability = math.e ** (- (current_value - new_value) / temperature)
    return acceptance_probability > random.random()


def random_neighbour(order: List[int]) -> List[int]:
    order = order.copy()
    i = random.randint(0, len(order) - 2)
    order[i], order[i+1] = order[i+1], order[i]
    logger.debug("Swapped %s and %s", i, i+1)
    return order


def random_swap(order: List[int]) -> List[int]:
    order = order.copy()
    [i, j]  = random.sample(range(len(order)), 2)
    order[i], order[j] = order[j], order[i]
    logger.debug("Swapped %s and %s", i, j)
    return order


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

