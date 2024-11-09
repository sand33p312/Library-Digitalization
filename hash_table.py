from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.hash_table = [None] * params[-1]
        self.collision_type = collision_type
        self.params = params
        self.total_element = 0
    
    def insert(self, x):
        slot_idx = self.get_slot(x[0] if type(x) is tuple else x)
        
        table_size = self.params[-1]

        if self.collision_type == "Chain" :
            if self.hash_table[slot_idx] is None:
                self.hash_table[slot_idx] = [x]
            else:
                self.hash_table[slot_idx].append(x)
        
        elif self.collision_type == "Linear":
            temp = slot_idx
            i = 0
            while self.hash_table[slot_idx] is not None:
                i += 1
                slot_idx = (temp + i) % table_size
                if slot_idx == temp:  # Full loop means table is full
                    raise Exception("Table is full")
            self.hash_table[slot_idx] = x
        
        else:  # Double hashing
            step_size = self.get_step_size(x[0] if type(x) is tuple else x)
            temp = slot_idx
            i = 0
            while self.hash_table[slot_idx] is not None:
                i += step_size
                slot_idx = (temp + i) % table_size
                if slot_idx == temp:  # Full loop means table is full
                    raise Exception("Table is full")
            self.hash_table[slot_idx] = x
            
    def find(self, key):
        slot_idx = self.get_slot(key)
        table_size = self.params[-1]

        if self.collision_type == "Chain":
            slot = self.hash_table[slot_idx]
            if slot is not None:
                for entry in slot:
                    if type(entry) != tuple :
                        if entry == key:
                            return True
                    elif entry[0] == key:
                        return entry[1] if isinstance(entry, tuple) else True
            return None  # Key not found

        elif self.collision_type == "Linear":
            return self._find(slot_idx, self.hash_table[slot_idx], 1, key, table_size)

        else:  # Double hashing
            element = self.hash_table[slot_idx]
            step_size = self.get_step_size(key)
            return self._find(slot_idx, element, step_size, key, table_size)

    
    def get_slot(self, key):
        params = self.params
        table_size = params[-1]

        count = 0
        current_power = 1  # Start with params[0]^0 = 1
        for i in range(len(key)):
            unicode_value = self.custom_ord(key[i])
            count += current_power * unicode_value
            current_power *= params[0]  # Update to params[0]^(i+1) for the next iteration
        slot_index = count % table_size
        return slot_index  # This returns the slot index to the caller
    
    def get_step_size(self, key):
        params = self.params
        count = 0
        current_power = 1
        for i in range(len(key)):
            unicode_value = self.custom_ord(key[i])
            count += current_power * unicode_value
            current_power *= params[1]  # Update to params[1]^(i+1) for the next iteration
        step_size = params[2]-count%params[2]
        return step_size # return the step size
    
    def get_load(self):
        return self.total_element/len(self.hash_table)
    
    def __str__(self):
        st = ""
        for i in self.hash_table:
            if i is None:
                st += "<EMPTY>"
            else:
                if isinstance(i, list):
                    st += " ; ".join(str(entry) for entry in i)
                else:
                    st += f"{i}"
            st += ' | '
        return st[:-3]  # Remove the last pipe

    def custom_ord(self, char):
        if 'a' <= char <= 'z':
            return ord(char) - ord('a')
        elif 'A' <= char <= 'Z':
            return 26 + ord(char) - ord('A')
        else:
            return None  # Return -1 for invalid characters
    
    def _find(self, slot_idx, element, step_size, key, table_size):
        temp = slot_idx
        while element is not None:
            if isinstance(element, tuple):
                if element[0] == key:  # Key found
                    return element[1]
            else:
                if element == key:  # Key found
                    return True
            slot_idx = (slot_idx + step_size) % table_size
            if slot_idx == temp:
                break
            element = self.hash_table[slot_idx]
        return None  # Key not found
    
    def rehash(self):
        pass
        
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.distinct_words = []
    
    def insert(self, key):
        if not self.find(key):  # Only increment if key is new
            super().insert(key)
            self.total_element += 1

    def find(self, key):
        return super().find(key)
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    # def __str__(self):
    #     return super().__str__()

    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        self.book_titles = []
    
    def insert(self, x):
        # x = (key, value)
        if not self.find(x[0]):  # Only increment if key is new
            super().insert(x)
            self.total_element += 1

    def find(self, key):
        return super().find(key)
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    # def __str__(self):
    #     return super().__str__()
