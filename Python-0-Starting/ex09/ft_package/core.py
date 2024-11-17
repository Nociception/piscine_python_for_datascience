def count_in_list(input_list: list, item: any) -> int:
    """Counts the occurrence of `item` in `input_list`.
    
    Args:
        input_list (list): The list to search in.
        item: The item to count.
        
    Returns:
        int: The count of `item` in `input_list`."""
    
    if not isinstance(input_list, list):
        raise ValueError("The first argument must be a list.")
    return input_list.count(item)
