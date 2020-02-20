def scan_choice(chosen_libraries):

    scan_list =[[] for i in range(len(chosen_libraries)-1)]
    
    all_books = [book for book in library["book_ids"] for library in chosen_libraries]
    
    book_unique = uniquelist(all_books) # checking which IDs are repeated and how often
    for j in 0:range(book_unique)-1
        number_options(j) = enumerate(all_books==book_unique)
    
    # sort book unique in decreasing order w.r.t. the value and reshuffle number_options in the appropriate way
    
    # full number of scans
    number_of_scans = sum([n_scans for n_scans in library["shipping_capacity"] for library in chosen_libraries])
    
    remaining_scans  = number_of_scans;
    
    while remaining_scans > 0 and len(book_unique)>0
        
        unscannable_books = [i for i,x in enumerate(number_options[0:remaining_scans]) if x==0]
        book_unique.pop(unscannable_books)
        number_options.pop(unscannable_books)
        
        only_one_chance = [i for i,x in enumerate(number_options[0:remaining_scans]) if x==1]
        
        for book in only_one_chance
            only_library = find_one_library(book, chosen_libraries)
            if chosen_libraries[only_library]["shipping_capacity"]-len(scanned_lists[only_library]) < 1
                book_unique.pop(book)
                number_options.pop(book)
            else
                scan_list[only_library].append(books_unique[book])
                remaining_scans -= 1
                book_unique.pop(book)
                number_options.pop(book)
        
        
        interesting_book = book_unique[0]
        available_libraries = find_library(interesting_book,chosen_libraries)
        best_library = 0
        best_condition = chosen_libraries[best_library]["shipping_capacity"]-len(scanned_lists[best_library])
        for j in range(len(available_libraries)-1)
            optimality_condition = chosen_libraries[j]["shipping_capacity"]-len(scanned_lists[j])
            if optimality_condition > best_condition
                best_library = j
        scan_list[best_library].append(interesting_book)
        remaining_scans -= 1
        book_unique.pop(0)
        number_options.pop(0)
        

    return scan_list



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


def find_one_library(book, list_libraries)
    for j in range(len(list_libraries)-1)
        if book in list_libraries[j]["book_ids"]
            return j
