"""Various helper functions for topk computation
"""

from types import GeneratorType
from math import exp

def fetch_lines(file_path: str):
    """Read a file line by line

    Positional Arguments:
    file_path -- path to file to be read

    Returns:
    Generator of a files' lines
    """
    with open(file_path, mode="rb") as infile:
        for line in infile:
            yield line.strip()

def take(iterable, size):
    """Build a window with specified size

    Positional Arguments:
    iterable    -- collection to pull from
    size        -- number of items to read

    Returns:
    subset of domain names
    """
    assert isinstance(iterable, GeneratorType), \
            "TypeError: iterable must be a generator object" \
            f", got {type(iterable)}"

    cnt = 0
    for elem in iterable:
        if cnt == size:
            break

        yield elem
        cnt += 1

def sigmoid(x) -> float:
    return 1 / float(1 + exp(-x))
