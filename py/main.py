import numpy as np
import math

def pairs(domains: list[str]) -> tuple[str]:
    """Build list of unique pairs of domain names

    Arguments:
    domains -- list of domain names to compute unique pairs on

    Returns:
    list of domain name pairs represented as a list of tuples
    """
    domain_len = len(domains)
    result = []

    for i in range(domain_len):
        for j in range(i + 1, domain_len):
            result.append((domains[i], domains[j]))
    
    return result

def top_k(domains: list[str], 
          k: int,
          window_len: int,
          threshold: float=0.70) -> list[str]:
    """Return top k scores from each window

    Positional Arguments:
    domains     -- list of domains we are computing edit distance scores on
    k           -- amount of maximum scores to store per window
    window_len  -- size of window

    Keyword Arguments:
    threshold -- minimum score to keep per window

    Returns:
    top k domains from each sliding window
    """
    domain_len = len(domains)

    if (window_len > domain_len):
        print(f"ERROR: window length > domain list length ({window_len} > "
                                                         f"{domain_len})")
        exit(1)

    global_max = []

    print("Begin top-k computation:\n"
          f"  # domains = {domain_len}\n"
          f"  k = {k}\n"
          f"  window size = {window_len}\n"
          f"  threshold = {threshold}")

    for i in range(0, domain_len, window_len):
        window = domains[i:i+window_len]
        uniq_pairs = pairs(window)
        local_max = np.full(len(uniq_pairs), -1.0, dtype=np.float32)

        for j in range(len(uniq_pairs)):
            X, Y = uniq_pairs[j]
            ed = edit_distance(X, Y) 
            score = round(scoring(ed, len(X) if len(X) > len(Y) else len(Y)), 2)
            if score > threshold:
                local_max[j] = score
        idx = np.argpartition(local_max, -k)
        for id in idx[-k:]:
            # this checks if the current window returned at least k max scores
            if local_max[id] > 0:
                global_max.append(uniq_pairs[id])

        # window_len += 1

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

def scoring(ed: int, max_ed: int) -> float:
    """Compute the score of an edit distance metric

    Arguments:
    ed      -- edit distance
    max_ed  -- max edit distance A.K.A length of longest string in computing ed
    """
    if ed == 0:
        return 1.0
    return 1 - (ed / float(max_ed))

if __name__ == "__main__":
    with open("../shubs-subdomains.txt") as wordlist:
        n = 1000
        words = [ word.strip() for word in wordlist.readlines()[:n] ]
        threshold = 0.50
        top = top_k(words, 5, math.floor(0.25*n), threshold)

        print(top)

