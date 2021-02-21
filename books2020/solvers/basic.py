def solve(problem):
    library_order = []
    for library_id, library in enumerate(problem["libraries"]):
        library_order.append({"id": library_id, "book_ids": [library["book_ids"][0]]})

    return library_order
