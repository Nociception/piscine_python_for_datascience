from array2D import slice_me

def test_slice_me():
    """
    Tests the `slice_me` function with a variety of input scenarios.

    The function evaluates the correctness of `slice_me` using:
    - Standard inputs provided in the exercise instructions.
    - Edge cases such as empty slices and out-of-bound slicing.
    - Error cases where invalid inputs are provided to ensure that
      the function raises appropriate errors.

    Scenarios tested include:
    - Valid slicing of a 2D list with integer and float values.
    - Handling of non-list inputs for `family`.
    - Checking for rows of unequal lengths.
    - Validating the presence of invalid element types in the 2D list.
    - Verifying behavior with invalid `start` or `end` values.
    - Edge cases where slicing results in empty or identical outputs.

    Expected output:
    - Correctly sliced lists for valid inputs.
    - Errors caught and printed for invalid inputs.

    Examples:
        >>> test_slice_me()
        My shape is : (4, 2)
        My new shape is : (2, 2)
        [[1.8, 78.4], [2.15, 102.7]]
        My shape is : (4, 2)
        My new shape is : (1, 2)
        [[2.15, 102.7]]
        ...
        (Output from all other test cases)
    """
    
    # Test 1 : Cas standard donné par le sujet
    family = [[1.80, 78.4], [2.15, 102.7], [2.10, 98.5], [1.88, 75.2]]
    print(slice_me(family, 0, 2))  # [[1.8, 78.4], [2.15, 102.7]]
    print(slice_me(family, 1, -2))  # [[2.15, 102.7]]

    # Test 2 : Cas limite avec une seule ligne conservée
    family = [[1.80, 78.4], [2.15, 102.7], [2.10, 98.5], [1.88, 75.2]]
    print(slice_me(family, 0, 1))  # [[1.8, 78.4]]

    # Test 3 : Slicing avec un index négatif
    print(slice_me(family, -2, None))  # [[2.1, 98.5], [1.88, 75.2]]

    # Test 4 : Cas d'erreur - famille n'est pas une liste
    try:
        slice_me("not a list", 0, 2)
    except SystemExit as e:
        print(f"Caught expected error: {e}")

    # Test 5 : Cas d'erreur - les éléments ne sont pas des listes
    try:
        slice_me([[1.80, 78.4], (2.15, 102.7)], 0, 2)
    except SystemExit as e:
        print(f"Caught expected error: {e}")

    # Test 6 : Cas d'erreur - Les lignes ont des longueurs différentes
    try:
        slice_me([[1.80, 78.4], [2.15]], 0, 2)
    except SystemExit as e:
        print(f"Caught expected error: {e}")

    # Test 7 : Cas d'erreur - Des types non valides dans les sous-listes
    try:
        slice_me([[1.80, "not valid"], [2.15, 102.7]], 0, 2)
    except SystemExit as e:
        print(f"Caught expected error: {e}")

    # Test 8 : Cas d'erreur - Indices de slicing ne sont pas des entiers
    try:
        slice_me(family, "start", 2)
    except SystemExit as e:
        print(f"Caught expected error: {e}")

    try:
        slice_me(family, 0, "end")
    except SystemExit as e:
        print(f"Caught expected error: {e}")

    # Test 9 : Cas limite avec slicing vide
    print(slice_me(family, 1, 1))  # []

    # Test 10 : Cas limite - slicing au-delà des bornes
    print(slice_me(family, 100, 200))  # []

    # Test 11 : Cas limite - slicing sur tout le tableau
    print(slice_me(family, 0, len(family)))  # Identique à `family`

if __name__ == "__main__":
    test_slice_me()
