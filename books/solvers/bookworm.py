import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

libraries = None
books = None
sorted_book_ids = None


def solve(problem):
    global libraries, books, sorted_book_ids
    libraries = problem["libraries"]
    books = problem["books"]
    sorted_books = sorted([(value, book_id) for book_id, value in enumerate(books)])
    sorted_book_ids = [book_id for (_, book_id) in sorted_books]

    new_signup_at_day = 0
    scanned_books = set()
    signed_libraries = set()
    library_order = []
    for day in tqdm(range(problem["number_of_days"] + 1)):
        if day == new_signup_at_day:
            new_signup_id = find_best_library(
                signed_libraries, scanned_books, problem["number_of_days"] - day
            )
            if new_signup_id is not None:
                day_available = libraries[new_signup_id]["signup_days"] + day
                new_signup_at_day = day_available
                library_order.append(
                    {
                        "id": new_signup_id,
                        "book_ids": [],
                        "day_available": day_available,
                    }
                )
                signed_libraries.add(new_signup_id)
                logger.debug("Signed up new library %s", new_signup_id)

        for library in library_order:
            if library["day_available"] >= day:
                for _ in range(libraries[library["id"]]["shipping_capacity"]):
                    for book_id in libraries[library["id"]]["book_ids"]:
                        if book_id not in scanned_books:
                            library["book_ids"].append(book_id)
                            scanned_books.add(book_id)

    return library_order


def find_best_library(signed_libraries, scanned_books, days_left):
    global libraries
    best_library_id = None
    best_library_value = 0
    for library_id, library in enumerate(libraries):
        if library_id not in signed_libraries:
            value = library_value(
                library_id, signed_libraries, scanned_books, days_left
            )
            if value > best_library_value:
                best_library_value = value
                best_library_id = library_id

    logger.debug("Found library %s to be the best", best_library_id)
    return best_library_id


def library_value(library_id, signed_libraries, scanned_books, days_left):
    global libraries, books
    library = libraries[library_id]

    # how many books can it do
    book_capacity = (days_left - library["signup_days"]) * library["shipping_capacity"]

    # what are the greatest values
    available_books = set(library["book_ids"]) - scanned_books

    book_values = sorted([(books[book_id], book_id) for book_id in available_books])

    # divide by the number of libraries that are signed up with that book
    total_value = 0.0
    for value, book_id in book_values[:book_capacity]:
        amount_of_libraries = 0
        for library_id in signed_libraries:
            library = libraries[library_id]
            if book_id in library["book_ids"]:
                amount_of_libraries += 1
        total_value += float(value / (amount_of_libraries + 1))

    logger.debug("Found value %s for library %s", total_value, library_id)
    return total_value
