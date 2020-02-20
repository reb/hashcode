def scan_choice(chosen_libraries):

    scan_list =[[] for i in range(chosen_libraries)]
    
    all_books = [book for book in library["book_ids"] for library in chosen_libraries]
    
    book_unique = uniquelist(all_books) # checking which IDs are repeated and how often
    for j in 0:range(book_unique)-1
        number_options(j) = enumerate(all_books==book_unique)
    
    # sort book unique in decreasing order w.r.t. the value and reshuffle number_options in the appropriate way
    
    # full number of scans
    number_of_scans = sum([n_scans for n_scans in library["shipping_capacity"] for library in chosen_libraries])
    
    #books_possible = book_unique[0:number_of_scans]
    #book_unique = book_unique[number_of_scans+1:]
    remaining_scans  = number_of_scans;
    
    while remaining_scans > 0 and len(book_unique)>0
        for j in range(number_of_scans-1)
            if number_options[j] < 1
                book_unique.pop(j)
                number_options.pop(j)
                j -= 1
            else if number_options[j] == 1
                # find which library has the book
                scan_list[only_library].append(books_possible[j])
                remaining_scans -= 1
                book_unique.pop(j)
                number_options.pop(j)
                j -= 1
        for j in range(len(books_possible)-1)
            # check which libraries has book(j) in their list
            # chose the library with most empty space in their scanning facility

    return scanned_lists



def uniquelist(list, idfunc=lambda x: x):
"""uniquify a list of lists"""

seen = {}
result = []

for item in list:
    marker = idfunc(tuple(item))
    if marker in seen: continue
    seen[marker] = 1
    result.append(item)
return result