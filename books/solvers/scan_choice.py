from operator import itemgetter
from typing import List
from books.problem import Problem, Solution


def scan_choice(problem: Problem, chosen_library_ids: List[int]) -> Solution:

    # cancelling libraries with no book
    nonempty_library_ids = filter( lambda library_id: problem.libraries[library_id].book_ids,chosen_library_ids)

    # how many scans are there between all the libraries
    number_of_scans = 0
    for lib in chosen_library_ids:
        library_entry = problem.libraries[lib]
        number_of_scans += library_entry["capacity"]

    remaining_scans = number_of_scans



    return Solution()