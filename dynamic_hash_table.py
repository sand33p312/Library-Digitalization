from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # Store old hash table and prepare new, larger table
        old_table = self.hash_table
        new_size = get_next_size()
        
        lst = list(self.params) # changing params as change table size.
        lst[-1] = new_size
        self.params = tuple(lst)

        self.hash_table = [None] * new_size
        self.total_element = 0  # Reset count to avoid duplicates


        for item in old_table:
            if item is not None:
                if isinstance(item, list):  # For chaining
                    for sub_item in item:
                        self.insert(sub_item)
                else:
                    self.insert(item)

    def insert(self, key):
        super().insert(key)
        if self.get_load() >= 0.5:
            self.rehash()
          
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # Store old hash table and prepare new, larger table
        old_hash_table = self.hash_table
        new_size = get_next_size()
        self.hash_table = [None] * new_size

        lst = list(self.params) # changing params as change table size.
        lst[-1] = new_size
        self.params = tuple(lst)

        self.total_element = 0
        
        # Re-insert items based on collision handling method
        if self.collision_type in ("Linear", "Double"):
            for content in old_hash_table:
                if content is not None:
                    self.insert(content)
        else:
            for slot in old_hash_table:
                if slot is not None:
                    for content in slot:
                        self.insert(content)
        
    def insert(self, key):
        # Calls base class insert and triggers rehash if load exceeds 0.5
        super().insert(key)
        if self.get_load() >= 0.5:
            self.rehash()