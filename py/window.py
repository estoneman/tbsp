import numpy as np
import math
from tqdm import tqdm
import time
from helper import AlgResponse

""" TODO
    - Finish debugging issue with window bounds
    - Finish testing @ 1000 domains
    - Implement helper "structs" (dataclasses) for data send/receive between the
      sliding windows algorithm and edit distance computations
"""

def pairs(window: list[str], threshold: float) -> AlgResponse:
    """Build list of unique pairs of domain names along with their edit distance
    scores

    Arguments:
    window -- list of domain names to compute unique pairs on

    Returns:
    Returns a list of tuples of the form (domain,domain,score)
    """
    window_sz = len(window)
    data = []

    # for i in tqdm(range(window_sz)):
    # t1 = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)
    t1 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
    # num_it = int(window_sz * (window_sz - 1) / 2)
    for i in tqdm(range(window_sz)):
        for j in range(i + 1, window_sz):
            X, X_len = window[i], len(window[i])
            Y, Y_len = window[j], len(window[j])
            S = round(scoring(edit_distance(X, Y), max(X_len, Y_len)), 2)
            if S < threshold:
                continue

            data.append((X, Y, S))

    # t2 = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)
    t2 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
    time_elapsed = (t2 - t1) / 1e9
    # spit = s * math.pow(num_it, -1)
    # itps = math.pow(spit, -1)

    alg_response = AlgResponse(data, time_elapsed)

    return alg_response

def top_k(domains, 
          n: int,
          window_sz: int,
          k: int,
          threshold: float=0.70) -> list[str]:
    """Return top k scores from each window

    Positional Arguments:
    domains     -- list of domains we are computing edit distance scores on
    domains     -- generator object of domains
    k           -- amount of maximum scores to store per window
    window_sz  -- size of window

    Keyword Arguments:
    threshold -- minimum score to keep per window

    Returns:
    top k domains from each sliding window
    """
    # n = len(domains)
    n = n

    if (window_sz > n):
        print(f"ERROR: window length > domain list length ({window_sz} > "
                                                         f"{n})")
        exit(1)
    # if (k >= window_sz):
    #     print(f"ERROR: k >= window length ({k} >= {window_sz})")
    #     exit(1)

    global_max = []

    # print("Begin top-k computation:\n"
    #       f"  # domains = {n}\n"
    #       f"  k = {k}\n"
    #       f"  window size = {window_sz}\n"
    #       f"  threshold = {threshold}")

    mttf = []
    n_windows = math.ceil(n / window_sz)
    n_processed = 0

    for i in range(0, n, window_sz):
        # window = domains[i:i+window_sz]

        # bounds check
        if n_processed + window_sz > n:
            print(f"computing on window {i}\n"
                  f"  n = {n}\n"
                  f"  window size = {window_sz}\n"
                  f"  domains processed = {n_processed}\n"
                  f"  adjusting window size to {n - n_processed}\n"
                  f"  adjusting k to {int(0.5*(n - n_processed))}")
            window_sz = n - n_processed
            k = int(0.5*window_sz)

        window = []
        for w in range(window_sz):
            window.append(next(domains))

        alg_response = pairs(window, threshold)
        mttf.append(alg_response.time_elapsed)

        local_max_len = int((window_sz*(window_sz - 1)) / 2)
        local_max = np.full(local_max_len, -1.0, dtype=np.float32)

        for j in range(len(alg_response.data)):
            local_max[j]  = alg_response.data[j][2]

        idx = np.argpartition(local_max, -k)
        for id in idx[-k:]:
            # return only non-negative max scores
            if local_max[id] > 0:
                global_max.append(alg_response.data[id])

        n_processed += window_sz

        # window_sz += 1

    sum = 0
    for ttf in mttf:
        sum += ttf
    mean = sum / n_windows

    return (global_max, mean)

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

def scoring(ed: int, max_ed: int) -> float:
    """Compute the score of an edit distance metric

    Arguments:
    ed      -- edit distance
    max_ed  -- max edit distance A.K.A length of longest string in computing ed
    """
    if ed == 0:
        return 1.0
    return 1 - (ed / float(max_ed))

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

