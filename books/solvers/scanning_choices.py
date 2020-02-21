from operator import itemgetter




def scan_choice(chosen_libraries,values):

    scan_list = {}

    for j in chosen_libraries
        if j["book_ids"] == []
            chosen_libraries.pop(j)
    
    dict_of_books = {}
    for library in chosen_libraries:
        library_id = library["id"]
        for book in library["book_ids"]:
            if book in dict_of_books:
                dict_of_books[book]["libraries"].append(library_id)
                dict_of_books[book]["number_of_libraries"] +=1
            else:
                dict_of_books[book] = {"libraries":[library_id],"value": values[book],"book_id" = book,"number_of_libraries":1}

    
    number_of_scans = 0
    for library in chosen_libraries
        number_of_scans += library["shipping_capacity"]
    
    remaining_scans = number_of_scans
    
    list_of_books = list(dict_of_books.values())
    list_of_books.sort(key = itemgetter("value"))
    
    slice = list_of_books[0:remaining_scans]
    
    while remaining_scans > 0 and len(list_of_books)>0:
        
        #for book in slice:
        #    if book["number_of_libraries"] < 1:
        #        slice.pop(book)
        #        list_of_books.pop(book)
        #        slice.append(list_of_books[remaining_scans])


        for book in slice:
            if book["number_of_libraries"] == 1:
                only_library = book["libraries"]
                if chosen_libraries[only_library]["shipping_capacity"]-len(scan_lists[only_library]) < 1:
                    slice.pop(book)
                    list_of_books.pop(book)
                    slice.append(list_of_books[remaining_scans])
                else:
                    scan_list[only_library].append(book["book_id"])
                    remaining_scans -= 1
                    slice.pop(book)
                    list_of_books.pop(book)
        
        interesting_book = list_of_books[0]
        available_libraries = interesting_book["libraries"]
        best_library = available_libraries[0]
        best_condition = chosen_libraries[best_library]["shipping_capacity"] - len(scanned_lists[best_library])
        for j in range(len(available_libraries)-1):
            optimality_condition = chosen_libraries[j]["shipping_capacity"] - len(scanned_lists[j])
            if optimality_condition > best_condition:
                best_library = j
                best_condition = optimality_condition
        if best_condition > 0 :
            scan_list[best_library].append(interesting_book)
            remaining_scans -= 1
            list_of_books.pop(book)
        else :
            slice.pop(book)
            list_of_books.pop(book)
            slice.append(list_of_books[remaining_scans])

    return scan_list
