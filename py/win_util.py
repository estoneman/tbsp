"""Various helper functions for topk computation"""

import sys

from math import exp

def remove_tld(d: str) -> str:
    """Remove the TLD from a domain

    Positional Arguments:
    d -- domain to be stripped
    """
    d_len = len(d)
    r = d_len - 1
    sub_d = list(d)

    while d[r] != ".":
        sub_d.pop()
        r -= 1

    sub_d.pop() # for that pesky period

    return "".join(sub_d)

def fetch_lines(file_path: str):
    """Read a file line by line

    Positional Arguments:
    file_path -- path to file to be read

    Returns:
    Generator of a files' lines
    """
    with open(file_path, mode="r", encoding="utf-8") as infile:
        for line in infile:
            yield remove_tld(line).encode("utf-8")

def is_iterable(iterable):
    """Check whether a sequence of data can be iterated
    
    Positional Arguments:
    iterable -- collection to be judged as iterable or not

    Returns:
    bool
    """
    try:
        iter(iterable)
        return True
    except TypeError:
        return False

def take(iterable, size):
    """Build a window with specified size

    Positional Arguments:
    iterable    -- collection to pull from
    size        -- number of items to read

    Returns:
    subset of domain names
    """
    if not is_iterable(iterable):
        print("passed object is not iterable. Aborting...")
        sys.exit(1)

    cnt = 0
    for elem in iterable:
        if cnt == size:
            break

        yield elem
        cnt += 1

def sigmoid(x) -> float:
    """Sigmoid function: https://en.wikipedia.org/wiki/Sigmoid_function

    Positional Arguments:
    x -- number to be scaled

    Returns:
    scaled version of input, `x`
    """
    return 1 / float(1 + exp(-x))
