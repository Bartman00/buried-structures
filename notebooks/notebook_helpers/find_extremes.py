
def find_extreme(iterable, func=max) -> float:
    """
    Recursively find the min or max in nested iterables.
    :param iterable: The nested collection (list, tuple, etc.)
    :param func: The built-in min or max function
    """

    flat_elements = []
    
    for item in iterable:
        # Check if the item is a nested iterable (excluding strings if desired)
        if isinstance(item, (list, tuple, set)):
            # Recursive call to drill into the nested structure
            inner_extreme = find_extreme(item, func)
            if inner_extreme is not None:
                flat_elements.append(inner_extreme)
        else:
            # Base case: item is a single value (int, float, etc.)
            flat_elements.append(item)

    assert (flat_elements is not None), "find_extreme flat elements is None"

    return func(flat_elements)

if __name__ == "__main__":
    # Example usage:
    nested_data = [1, [5, [10, -2]], 8, [0]]
    print(f"Maximum: {find_extreme(nested_data, max)}") # Output: 10
    print(f"Minimum: {find_extreme(nested_data, min)}") # Output: -2