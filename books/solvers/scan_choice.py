from collections import defaultdict
from operator import itemgetter
from typing import List
from books.problem import Problem, Solution
import logging

logger = logging.getLogger(__name__)


def scan_choice(problem: Problem, chosen_library_ids: List[int]):
    scan_list = defaultdict(list)

    # cancelling libraries with no book
    nonempty_library_ids = list(
        filter(
            lambda library_id: problem.libraries[library_id].book_ids,
            chosen_library_ids,
        )
    )

    # how many scans are there between all the libraries
    remaining_scans = sum(
        [problem.libraries[library_id].capacity for library_id in nonempty_library_ids]
    )

    # creating a dictionary of books - where they are, their value, id, how many libraries
    dict_of_books = {}
    for library_id in nonempty_library_ids:
        library = problem.libraries[library_id]
        for book_id in library.book_ids:
            if book_id in dict_of_books:
                dict_of_books[book_id]["libraries"].append(library_id)
                dict_of_books[book_id]["number_of_libraries"] += 1
            else:
                value = problem.books[book_id].value
                dict_of_books[book_id] = {
                    "libraries": [library_id],
                    "value": value,
                    "book_id": book_id,
                    "number_of_libraries": 1,
                }

    # change dictionary of books to list ordered by values of book
    list_of_books = list(dict_of_books.values())
    list_of_books.sort(key=itemgetter("value"))

    while remaining_scans > 0 and list_of_books:

        interesting_book = list_of_books[0]
        available_libraries = interesting_book["libraries"]
        best_library_id = available_libraries[0]
        best_condition = problem.libraries[best_library_id].capacity - len(
            scan_list[best_library_id]
        )
        for library_id in available_libraries:
            if library_id in chosen_library_ids:
                optimality_condition = problem.libraries[library_id].capacity - len(
                    scan_list[library_id]
                )
                if optimality_condition > best_condition:
                    best_library_id = library_id
                    best_condition = optimality_condition

        if best_condition > 0:
            scan_list[best_library_id].append(interesting_book["book_id"])
            if (
                len(scan_list[best_library_id])
                == problem.libraries[best_library_id].capacity
            ):
                chosen_library_ids.remove(library_id)
            remaining_scans -= 1
            list_of_books.pop(0)
        else:
            list_of_books.pop(0)

    return scan_list
