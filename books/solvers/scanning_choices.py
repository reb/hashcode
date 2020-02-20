def scan_choice(chosen_libraries, already_scanned_books):
    all_books = []
    for book_id in chosen_libraries.book_ids
        all_books.append(book_id)
    [book_unique, number_options] = unique(all_books) # checking which IDs are repeated and how often
    # cancell already_scanned_books from book_unique
    # sort book unique in decreasing order w.r.t. the value and reshuffle number_options in the appropriate way
    number_of_scans =0
    for shipping_capacity in chosen_libraries.shipping_capacity
        number_of_scans += shipping_capacity
    books_possible = book_unique.pop(:number_of_scans)
    for j in 0:length(books_possible)-1
        if number_options(j) <1
            books_possible.pop(j)
            number_options.pop(j)
            books_possible.append = book_unique.pop(0)
            j -=1
        else if number_options(j) == 1
            # add book_possible(j) to the list of scans of the only library available to scan it -- I don't know how to do it (E)
            # cancel the j-th book
    for j in 0:length(books_possible)-1
        # check which libraries has book(j) in their list
        # chose the library with most empty space in their scanning facility
    return scanned_lists
