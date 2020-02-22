from operator import itemgetter
from typing import List
from books.problem import Problem, Solution


def scan_choice(problem: Problem, chosen_library_ids: List[int]) -> Solution:
    scan_list = {}

    # cancelling libraries with no book
    nonempty_library_ids = filter(lambda library_id: problem.libraries[library_id].book_ids, chosen_library_ids)

    # how many scans are there between all the libraries
    remaining_scans = sum([problem.libraries[library_id].capacity for library_id in nonempty_library_ids])

    # creating a dictionary of books - where they are, their value, id, how many libraries
    dict_of_books = {}
    for library_id in nonempty_library_ids:
        library = problem.libraries[library_id]
        for book_id in library.book_ids:
            if book_id in dict_of_books:
                dict_of_books[book_id]["libraries"].append(library_id)
                dict_of_books[book_id]["number_of_libraries"] += 1
            else:
                value_loc = problem.books[book_id]
                dict_of_books[book_id] = {"libraries": [library_id],
                                          "value": value_loc,
                                          "book_id": book_id,
                                          "number_of_libraries": 1}

    # change dictionary of books to list ordered by values of book
    list_of_books = list(dict_of_books.values())
    list_of_books.sort(key=itemgetter("value"))

    # best books to scan
    slice = list_of_books[0:remaining_scans]

    for book in slice:
        if book["number_of_libraries"] == 1:
            only_library_id = book["libraries"]
            # library can still scan?
            if problem.libraries[only_library_id].capacity - len(scan_list[only_library_id]) < 1:
                slice.pop(book)
                list_of_books.pop(book)
                slice.append(list_of_books[remaining_scans])
            else:
                scan_list[only_library_id].append(book_id["book_id"])
                remaining_scans -= 1
                slice.pop(book)
                list_of_books.pop(book)

    while remaining_scans > 0 and list_of_books:

        interesting_book = list_of_books[0]
        available_libraries = interesting_book["libraries"]
        best_library = available_libraries[0]
        best_condition = problem.libraries[chosen_library_ids[best_library]].capacity - len(scan_list[best_library])
        for j in range(len(available_libraries) - 1):
            optimality_condition = problem.libraries[chosen_library_ids[j]].capacity - len(scan_list[j])
            if optimality_condition > best_condition:
                best_library = j
                best_condition = optimality_condition
        if best_condition > 0:
            scan_list[best_library].append(interesting_book)
            remaining_scans -= 1
            list_of_books.pop(interesting_book)
        else:
            slice.pop(interesting_book)
            list_of_books.pop(interesting_book)
            slice.append(list_of_books[remaining_scans])

    return scan_list
