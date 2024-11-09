import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    

class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        # Make deep copies of book_titles and texts to avoid modifying the original data
        self.texts = [element.copy() for element in texts]
        self.books_titles = book_titles.copy()

        self.distinct_words_lists = []

        # Sort each text array in self.texts
        for idx in range(len(self.texts)):
            self.texts[idx] = self.mergesort(self.texts[idx])

        # Zip book_titles and texts, then sort by book titles
        ziped_list = list(zip(self.books_titles, self.texts))
        sorted_list = self.mergesort(ziped_list)  # Ensure mergesort sorts by the first item (book_titles)

        # Unzip sorted list back into self.books_titles and self.texts
        self.books_titles, self.texts = map(list, zip(*sorted_list))

        # Generate distinct words lists
        for i in range(len(self.books_titles)):
            lst = [self.texts[i][0]]  # Start distinct list with first element
            for j in range(1, len(self.texts[i])):
                if self.texts[i][j] != lst[-1]:  # Only add if it's different from the last distinct element
                    lst.append(self.texts[i][j])
            self.distinct_words_lists.append(lst)

    def distinct_words(self, book_title):
        index_book_title = self.binary_search(self.books_titles,x=book_title) # index of given book_title in book_titles .
        return self.distinct_words_lists[index_book_title]
    
    def count_distinct_words(self, book_title):
        index_book_title = self.binary_search(self.books_titles,book_title) # index of given book_title in book_titles .
        return len(self.distinct_words_lists[index_book_title])
    
    def search_keyword(self, keyword):
        # print(self.books_titles)
        books_contain_key = [] # initialise list for book_titles contain the given keyword.
        for i in range(len(self.books_titles)):
            if self.binary_search(self.texts[i],keyword) != -1:
                books_contain_key.append(self.books_titles[i])
        
        return books_contain_key

    def print_books(self):
        all_books_data = ""
        for i in range(len(self.books_titles)):
            st = str(self.books_titles[i])+': '
            for j in self.distinct_words_lists[i]:
                st += j+' | '
            st = st[:-3]
            all_books_data += st+'\n'
        all_books_data = all_books_data[:-1]
        print(all_books_data)  

    def mergesort(self,arr):
        if len(arr)>1:
            m=len(arr)//2
            L=arr[:m]
            R=arr[m:]
            self.mergesort(L)
            self.mergesort(R)
            i=j=k=0
            while i<len(L) and j<len(R):
                if L[i]<=R[j]:
                    arr[k]=L[i]
                    k+=1
                    i+=1
                else:
                    arr[k]=R[j]
                    k+=1
                    j+=1
            while i<len(L):
                arr[k]=L[i]
                k+=1
                i+=1
            while j<len(R):
                arr[k]=R[j]
                k+=1
                j+=1
        return arr
    
    def binary_search(self,arr, x):
        low = 0
        high = len(arr) - 1
        while low <= high:
            mid = (high + low) // 2
            if arr[mid] < x:
                low = mid + 1
            elif arr[mid] > x:
                high = mid - 1
            else:
                return mid
        return -1

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Comp                
                ression function for second hash: mod c2
        '''
        self.name = name
        self.params = params
        self.books = []

        if name == "Jobs":
            collision_type = "Chain"
        elif name == "Gates":
            collision_type = "Linear"
        else:
            collision_type = "Double"

        self.hm = ht.HashMap(collision_type,params)

    def add_book(self, book_title, text):
        # Initialize a new HashSet instance for storing distinct words
        collision_type = self.hm.collision_type
        params = self.params
        hs = ht.HashSet(collision_type=collision_type, params=params)

        # Insert unique words into the HashSet
        for word in text:
            if hs.find(word) == None :
                hs.insert(word)

        # Extract distinct words based on the collision type
        if collision_type == "Chain":
            for t in hs.hash_table:
                if t is not None:
                    hs.distinct_words.extend(t)  # Add all items in the chain
        else:
            for t in hs.hash_table:
                if t is not None:
                    hs.distinct_words.append(t)  # Add directly if not using chaining

        # Insert the book and its HashSet into the main hash map
        self.hm.insert((book_title, hs))

        self.books = [] # reset to empty list .

        # Add each book title only once
        if collision_type == "Chain":
            for content in self.hm.hash_table:
                if content is not None:
                    for book in content:
                        self.books.append(book)
        else:
            for book in self.hm.hash_table:
                if book is not None:
                    self.books.append(book)

    def distinct_words(self, book_title):
        book_title_text = self.hm.find(book_title)
        if book_title_text is not None:
            return book_title_text.distinct_words

    def count_distinct_words(self, book_title):
        book_title_text = self.hm.find(book_title)
        if book_title_text is not None:
            distinct_words = len(book_title_text.distinct_words)
            return distinct_words
    
    def search_keyword(self, keyword):
        books = self.books
        all_books_with_keyword = []

        for book in books:
            book_title = book[0]
            book_title_text = self.hm.find(book_title)
            if book_title_text.find(keyword) == True:
                all_books_with_keyword.append(book_title)
        
        return all_books_with_keyword
    
    def print_books(self):
        all_book_data = ""
        collision_type = self.hm.collision_type

        if collision_type == "Chain":
            # Iterate over each entry in the hash table for chain-based collision handling
            for book in self.books:
                all_book_data += f"{book[0]}: "  # Add book title
                
                hash_table_slots = book[1].hash_table  # Access hash table

                # Prepare output for each slot in the hash table
                slot_outputs = []
                for slot in hash_table_slots:
                    if slot is None:
                        slot_outputs.append("<EMPTY>")
                    else:
                        if isinstance(slot, list):
                            # Join each word in a chained slot with "; " as separator
                            slot_outputs.append(" ; ".join(str(word) for word in slot))
                        else:
                            slot_outputs.append(str(slot))

                # Join slots with " | " as separator for the final format
                all_book_data += " | ".join(slot_outputs) + "\n"

        else:
            # Non-chain handling case
            for book in self.books:
                all_book_data += f"{book[0]}: "  # Add book title
                slot_outputs = []
                for slot in book[1].hash_table:
                    if slot is None:
                        slot_outputs.append("<EMPTY>")
                    else:
                        slot_outputs.append(slot)
                all_book_data += " | ".join(slot_outputs) + "\n"

        # Print the formatted book data output
        print(all_book_data)