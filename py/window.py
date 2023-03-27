import numpy as np
import math
from tqdm import tqdm
import time
from helper import PairsResponse, TopKResponse
from itertools import combinations
import multiprocessing as mp
import os

""" TODO
    - Finish debugging issue with window bounds
    - Finish testing @ 1000 domains
    - Implement helper "structs" (dataclasses) for data send/receive between the
      sliding windows algorithm and edit distance computations
"""

def score(pair):
    if len(pair) != 2:
        return 0.0

    return scoring(pair[0], pair[1])

def construct_window(domains, w):
    for i in range(w):
        yield next(domains)

def top_k(domains, 
          n: int,
          w: int,
          k: int,
          threshold: float=0.70) -> list[str]:
    """Scores top k domains per window

    Positional Arguments:
    domains     -- generator object of domains
    k           -- amount of maximum scores to store per window
    w           -- size of window

    Keyword Arguments:
    threshold -- minimum score to keep per window

    Returns:
    list of top k domains
    """

    n_procs = int(os.cpu_count() / 2)
    n_processed = 0
    
    # log actions
    print(f"# domains: {n}")

    global_max = []
    with mp.Pool(processes=n_procs) as pool:
        # window_scores = mp.Queue(maxsize=n_uniq)
        for i in range(0, n, w):
            assert w <= n, f"window length > # total domains: ({w} > {n})"

            if n_processed + w > n:
                w = n - n_processed
                k = math.ceil(0.5*w)

            n_uniq = int(w * (w - 1) / 2)
            window_scores = np.empty(n_uniq, dtype=np.float32) 

            print(f"  window size: {w}\n"
                  f"  unique_pairs: {n_uniq}\n"
                  f"  k: {k}")

            window = construct_window(domains, w)
            unique_pairs = list(combinations(window, r=2))

            scores = pool.imap(score, unique_pairs)
            for j in range(n_uniq):
                window_scores[j] = next(scores)

            k_top = np.argpartition(window_scores, -k)
            for idx in k_top[-k:]:
                global_max.append(unique_pairs[idx])

            n_processed += w

    return global_max 

def my_min(*args) -> int:
    """Utility function to compute the min of a variable amount of arguments

    Arguments:
    *args -- collection of all arguments passed to the function

    Returns:
    minimum of all function arguments

    Notes:
    Assumes data type of arguments are real numbers
    """
    min = args[0]
    for v in args:
        if v < min:
            min = v
    
    return min

def edit_distance(X: str, Y: str) -> int:
    """Compute the edit distance of X and Y

    Arguments:
    X -- Original word
    Y -- Word to transform X into

    Returns:
    Minimum number of operations to transform X into Y
    """
    len_X = len(X)
    len_Y = len(Y)

    if (len_X == 0):
        return len_Y
    elif (len_Y == 0):
        return len_X

    E: np.ndarray = np.zeros((len_X + 1, len_Y + 1), dtype=np.uint8)
    E[0] = np.arange(len_Y + 1)
    E[:,0] = np.arange(len_X + 1)

    for i in range(1, len_X + 1):
        for j in range(1, len_Y + 1):
            # deletion
            a = E[i - 1, j] + 1
            # insertion
            b = E[i, j - 1] + 1
            # substitution
            c = E[i - 1, j - 1] + (1 if X[i - 1] != Y[j - 1] else 0)

            E[i, j] = min(a,b,c)

    return E[len_X, len_Y]

# TODO: Research if there is something valuable with the sequence of edits to
#   transform X -> Y
def reconstruct(E: np.ndarray, X: str, Y: str) -> list[str]:
    """Create the sequence of edits that transformed X -> Y

    Arguments:
    E -- matrix of edit distances of substrings of X and Y
    X -- Original string to be edited
    Y -- Transformed string

    Returns:
    For now, it returns a sequence of executed operations.
    """
    i = len(X)
    j = len(Y)

    L: list[str] = []

    while (i > 0 or j > 0):
        if i == 0:
            L.insert(0, f"Insert {Y[j - 1]} at beginning")
            j -= 1
        elif j == 0 or E[i, j] == 1 + E[i - 1, j]:
            L.insert(0, f"Delete {X[i - 1]}")
            i -= 1
        elif E[i, j] == 1 + E[i, j - 1]:
            L.insert(0, f"Insert {Y[j - 1]} after {X[i - 1]}") 
            j -= 1
        elif X[i - 1] == Y[j - 1]:
            i -= 1; j -= 1
        else:
            L.insert(0, f"Substitute {Y[j - 1]} for {X[i - 1]}")
            i -= 1; j -= 1

    return L

# def scoring(ed: int, max_ed: int) -> float:
def scoring(X: str, Y: str) -> float:
    """Compute the score of an edit distance metric

    Arguments:
    ed      -- edit distance
    max_ed  -- max edit distance A.K.A length of longest string in computing ed
    """
    # if ed == 0:
    #     return 1.0
    # return 1 - (ed / float(max_ed))

    len_X = len(X)
    len_Y = len(Y)

    max_len = len_X if len_X > len_Y else len_Y
    ed = edit_distance(X, Y)

    if ed == 0:
        return 1.0

    return round(1 - (ed / float(max_len)), 3)

def fetch_lines(fn: str):
    result = []
    with open(fn, "r") as fp:
        for line in fp:
            # result.append(line.strip())
            yield line.strip()

    # return result

def naive(domains, n, threshold):
    # result = np.empty((n,n), dtype=np.float64)
    result = []
    for i in tqdm(range(n)):
        for j in range(i + 1, n):
            x = len(domains[i])
            y = len(domains[j])
            s = round(scoring(edit_distance(domains[i], domains[j]),
                              x if x > y else y), 2)
            if s > threshold:
                result.append((domains[i],domains[j],s))

    return result

