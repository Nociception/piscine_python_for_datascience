# Subject
"""
Exercice 08: Loading ...
Turn-in directory : ex08/
Files to turn in : Loading.py
Allowed functions : None

So let's create a function called ft_tqdm.
The function must copy the function tqdm with the yield operator.

Here's how it should be prototyped:
def ft_tqdm(lst: range) -> None:
#your code here
"""


def ft_tqdm(lst: range):
    """
    A mini tqdm, inspired from the original tqdm.
    Prints a progressing load bar, according to the parameter lst.

    For more details :
    >>> from tqdm import tqdm
    >>> print(help(tqdm))

    Usage:
    for elem in ft_tqdm(range(333)):
        sleep(0.005)
    """

    WIDTH = 61
    total = len(lst)

    for i, elem in enumerate(lst, start=1):
        progress = i / total
        filled = int(WIDTH * progress)
        bar = '=' * filled + '>' + ' ' * (WIDTH - filled)
        percent = int(progress * 100)

        print(f"\r{percent}%|[{bar}]| {i}/{total}", end='', flush=True)
        yield elem

    print()
