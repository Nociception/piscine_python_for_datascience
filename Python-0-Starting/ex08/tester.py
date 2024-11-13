# Subject
"""Your tester.py: (you compare your version with the original)
from time import sleep
from tqdm import tqdm
from Loading import ft_tqdm
for elem in ft_tqdm(range(333)):
sleep(0.005)
print()
for elem in tqdm(range(333)):
sleep(0.005)
print()

Expected output:
(you must have a function as close as possible to the original version)
$> python tester.py
100%|[===============================================================>]
| 333/333
100%|                                                                  |
333/333 [00:01<00:00, 191.61it/s]"""


from time import sleep
from tqdm import tqdm
from Loading import ft_tqdm


def main() -> None:
    """DOCSTRING"""
    DELAY = 0.005

    def ft_tqdm_VS_original_tqdm(r: range) -> None:
        print(f"Comparison for range={r}")
        for elem in ft_tqdm(range(r)):
            sleep(DELAY)
            # print(elem)
        print()
        for _ in tqdm(range(r)):
            sleep(DELAY)
        print()

    ft_tqdm_VS_original_tqdm(333)
    ft_tqdm_VS_original_tqdm(500)
    ft_tqdm_VS_original_tqdm(20)
    ft_tqdm_VS_original_tqdm(5)


if __name__ == "__main__":
    main()
