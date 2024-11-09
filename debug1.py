from hash_table import HashSet

def test_hashset():
    # Parameters for hash functions
    collision_type = 'Chain'  # Change as needed
    params = [7,10]  # Sample values for hash functions

    # Initialize HashSet
    hash_set = HashSet(collision_type, params)

    # Test insertions with fewer elements
    test_keys = ["apple", "banana","guava",'tara','apple']
    print("Inserting elements:")
    for key in test_keys:
        hash_set.insert(key)
        print(f"Inserted: {key}")

    # Display HashSet after insertions
    print("\nHashSet after insertions:")
    print(hash_set)
    print(hash_set.hash_table)
    # Test find function
    print("\nTesting find function:")
    for key in test_keys:
        result = hash_set.find(key)
        print(f"Find '{key}': {'Found' if result else 'Not Found'}")

    # Test finding a non-existent key
    non_existent_key = "grape"
    print(f"\nFind '{non_existent_key}': {'Found' if hash_set.find(non_existent_key) else 'Not Found'}")

# Run the test function
test_hashset()