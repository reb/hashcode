from operator import itemgetter
from typing import List
from books.problem import Problem


def scan_choice(problem: Problem, chosen_libraries: List[int]):

    scan_list = {}

    # cancelling libraries with no book
    for j in chosen_libraries:
        if not j["book_ids"]:
            chosen_libraries.pop(j)

    # creating a dictionary of books - where they are, their value, id, how many libraries
    dict_of_books = {}
    for library in chosen_libraries:
        library_id = library["id"]
        for book in library["book_ids"]:
            if book in dict_of_books:
                dict_of_books[book]["libraries"].append(library_id)
                dict_of_books[book]["number_of_libraries"] += 1
            else:
                value_loc = problem.books[book]
                dict_of_books[book] = {"libraries": library_id,
                                       "value": value_loc,
                                       "book_id": book,
                                       "number_of_libraries": 1}

    # how many scans are there between all the libraries
    number_of_scans = 0
    for library in chosen_libraries:
        number_of_scans += library["shipping_capacity"]

    remaining_scans = number_of_scans

    # change dictionary of books to list ordered by values of book
    list_of_books = list(dict_of_books.values())
    list_of_books.sort(key=itemgetter("value"))

    # best books to scan
    slice_books = list_of_books[0:remaining_scans]

    for book in slice_books:
        if book["number_of_libraries"] == 1:
            only_library = book["libraries"]
            # library can still scan?
            if chosen_libraries[only_library]["shipping_capacity"] - len(scan_list[only_library]) < 1:
                slice_books.pop(book)
                list_of_books.pop(book)
                slice_books.append(list_of_books[remaining_scans])
            else:
                scan_list[only_library].append(book["book_id"])
                remaining_scans -= 1
                slice_books.pop(book)
                list_of_books.pop(book)

    while remaining_scans > 0 and len(list_of_books) > 0:

        interesting_book = list_of_books[0]
        available_libraries = interesting_book["libraries"]
        best_library = available_libraries[0]
        best_condition = chosen_libraries[best_library]["shipping_capacity"] - len(scan_list[best_library])
        for j in range(len(available_libraries) - 1):
            optimality_condition = chosen_libraries[j]["shipping_capacity"] - len(scan_list[j])
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
