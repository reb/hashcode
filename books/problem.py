def read(text):
    lines = text.split("\n")
    [number_of_books, number_of_libraries, number_of_days] = [
        int(i) for i in lines[0].split(" ")
    ]
    books = [int(i) for i in lines[1].split(" ")]
    libraries = []

    for index in range(2, len(lines) - 1, 2):
        if not lines[index]:
            continue
        [books_in_library, signup_days, shipping_capacity] = [
            int(i) for i in lines[index].split(" ")
        ]
        book_ids = [int(i) for i in lines[index + 1].split(" ")]

        libraries.append(
            {
                "books_in_library": books_in_library,
                "signup_days": signup_days,
                "shipping_capacity": shipping_capacity,
                "book_ids": book_ids,
            }
        )

    return {
        "number_of_books": number_of_books,
        "number_of_libraries": number_of_libraries,
        "number_of_days": number_of_days,
        "books": books,
        "libraries": libraries,
    }


def write(solution):
    result = f"{len(solution)}\n"
    for library in solution:
        description = f"{library['id']} {len(library['book_ids'])}"
        book_ids = " ".join(str(book_id) for book_id in library["book_ids"])
        result += f"{description}\n{book_ids}\n"

    return result
