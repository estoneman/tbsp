import numpy as np

def score(pair):
    """Edit distance score of a pair of strings

    PositionalArguments:
    pair -- tuple of domains

    Returns:
    Similarity score of two domains
    """
    if len(pair) != 2:
        return 0.0

    return scoring(pair[0], pair[1])

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

def scoring(X: str, Y: str) -> float:
    """Compute the score of an edit distance metric

    Arguments:
    ed      -- edit distance
    max_ed  -- max edit distance A.K.A length of longest string in computing ed
    """

    len_X = len(X)
    len_Y = len(Y)

    max_len = len_X if len_X > len_Y else len_Y
    ed = edit_distance(X, Y)

    if ed == 0:
        return 1.0

    return round(1 - (ed / float(max_len)), 3)
