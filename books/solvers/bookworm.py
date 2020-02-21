import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

libraries = None
books = None


def solve(problem):
    global libraries, books

    books = {index: value for index, value in enumerate(problem["books"])}

    # sort books by value
    libraries = problem["libraries"]
    for library in libraries:
        library["book_ids"].sort(key=lambda book_id: books[book_id])

    new_signup_at_day = 0
    signed_libraries = set()
    library_order = []
    library_active = 0

    # how many times do we want to do a signup round
    signup_rounds = 4
    signup_round = 0

    for day in tqdm(range(problem["number_of_days"] + 1)):
        if day == new_signup_at_day:
            ranked_library_ids = rank_libraries(
                signed_libraries, problem["number_of_days"] - day
            )
            signup_round += 1
            goal_day = signup_round * (problem["number_of_days"] / signup_rounds)
            while new_signup_at_day < goal_day and ranked_library_ids:
                new_signup_id = ranked_library_ids.pop(0)
                new_signup_at_day += libraries[new_signup_id]["signup_days"]
                library_order.append(
                    {
                        "id": new_signup_id,
                        "book_ids": [],
                        "day_available": new_signup_at_day,
                    }
                )
                signed_libraries.add(new_signup_id)
                logger.debug("Signed up new library %s", new_signup_id)

        if (
            len(library_order) != library_active
            and library_order[library_active]["day_available"] == day
        ):
            library_active += 1
        available_libraries = library_order[:library_active]
        scan_todays_books(available_libraries)

    return library_order


def scan_todays_books(available_libraries):
    global libraries
    for scanning_library in available_libraries:
        library = libraries[scanning_library["id"]]
        scanning_books = library["book_ids"][: library["shipping_capacity"]]
        for book_id in scanning_books:
            remove_book(book_id)
        scanning_library["book_ids"].extend(scanning_books)


def remove_book(book_id):
    """Remove a book from the global variables"""
    global libraries, books
    for library in libraries:
        if book_id in library["book_ids"]:
            library["book_ids"].remove(book_id)
    books.pop(book_id)


def rank_libraries(signed_libraries, days_left):
    global libraries

    ranked_libraries = []

    for library_id, library in enumerate(libraries):
        if library_id not in signed_libraries:
            value = library_value(library_id, signed_libraries, days_left)
            ranked_libraries.append((value, library_id))

    ranked_libraries.sort()
    return [library_id for _, library_id in ranked_libraries]


def library_value(library_id, signed_libraries, days_left):
    global libraries, books
    library = libraries[library_id]

    # how many books can it do
    book_capacity = (days_left - library["signup_days"]) * library["shipping_capacity"]

    # the greatest books should already be stored in front of the library list
    # divide by the number of libraries that are signed up with that book
    total_value = 0.0
    for book_id in library["book_ids"][:book_capacity]:
        amount_of_libraries = 0
        for library_id in signed_libraries:
            library = libraries[library_id]
            if book_id in library["book_ids"]:
                amount_of_libraries += 1
        total_value += float(books[book_id] / (amount_of_libraries + 1))

    logger.debug("Found value %s for library %s", total_value, library_id)
    return total_value
