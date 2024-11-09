from hash_table import HashMap

def test_hashmap():
    # Parameters for hash functions
    collision_type = 'Chain'  # Change as needed (e.g., 'Linear' or 'Double')
    params = [31, 7]  # [z1, z2, c2, initial_size]

    # Initialize HashMap
    hash_map = HashMap(collision_type, params)

    # Test insertions with fruit names and their costs
    fruit_costs = [
        ("apple", ['archie','orange']),
        ("banana", 0.30),
        ("cherry", 0.75),
        ("date", 1.00),
        ("elderberry", 1.50),
        ("apple",1.4)
    ]
    
    print("Inserting fruit and cost pairs:")
    for fruit, cost in fruit_costs:
        hash_map.insert((fruit, cost))
        print(f"Inserted: ({fruit}, {cost})")

    # Display HashMap after insertions
    print("\nHashMap after insertions:")
    print(hash_map.hash_table)
    print(hash_map)

    # Test find function
    print("\nTesting find function:")
    for fruit, _ in fruit_costs:
        result = hash_map.find(fruit)
        print(f"Find '{fruit}': {'Found with cost ' + str(result) if result else 'Not Found'}")

    # Test finding a non-existent fruit
    non_existent_fruit = "fig"
    print(f"\nFind '{non_existent_fruit}': {'Found with cost ' + str(hash_map.find(non_existent_fruit)) if hash_map.find(non_existent_fruit) else 'Not Found'}")

    # Test updating a fruit's cost
    print("\nUpdating cost for 'banana':")
    hash_map.insert(("banana", 0.35))  # Updating the cost for banana
    print(f"Updated cost for 'banana': {hash_map.find('banana')}")  # Expected output: 0.35

    # Test rehashing
    print("\nRehashing the HashMap:")
    hash_map.rehash()
    print(hash_map)

    # Insert more fruit-cost pairs
    print("\nInserting more fruit-cost pairs after rehashing:")
    additional_fruits = [
        ("grape", 2.00),
        ("honeydew", 3.00)
    ]
    for fruit, cost in additional_fruits:
        hash_map.insert((fruit, cost))
        print(f"Inserted: ({fruit}, {cost})")
    
    print(hash_map)

    # Final test of all fruits
    print("\nFinal fruit lookups:")
    for fruit, _ in fruit_costs + additional_fruits:
        print(f"Find '{fruit}': {hash_map.find(fruit)}")

# Run the test function
test_hashmap()