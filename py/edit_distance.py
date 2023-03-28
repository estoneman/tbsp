"""Collection of string computation distance tools
"""

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

def edit_distance(src: str, dst: str) -> int:
    """Compute the edit distance of src and dest

    Arguments:
    src -- Original word
    dest -- Word to transform src into

    Returns:
    Minimum number of operations to transform src into dest
    """
    len_src = len(src)
    len_dst = len(dst)

    if len_src == 0:
        return len_dst
    if len_dst == 0:
        return len_src

    substr_edits: np.ndarray = np.zeros((len_src + 1, len_dst + 1),
                                        dtype=np.uint8)
    substr_edits[0] = np.arange(len_dst + 1)
    substr_edits[:,0] = np.arange(len_src + 1)

    for i in range(1, len_src + 1):
        for j in range(1, len_dst + 1):
            # deletion
            delete = substr_edits[i - 1, j] + 1
            # insertion
            ins = substr_edits[i, j - 1] + 1
            # substitution
            sub = substr_edits[i - 1, j - 1] + \
            (1 if src[i - 1] != dst[j - 1] else 0)

            substr_edits[i, j] = min(delete,ins,sub)

    return substr_edits[len_src, len_dst]

def reconstruct(substr_edits: np.ndarray, src: str, dst: str) -> list[str]:
    """Create the sequence of edits that transformed src -> dst

    Arguments:
    substr_edits -- matrix of edit distances of substrings of src and dst
    src -- Original string to be edited
    dst -- Transformed string

    Returns:
    For now, it returns a sequence of executed operations.
    """
    i = len(src)
    j = len(dst)

    reconstr_seq: list[str] = []
    while (i > 0 or j > 0):
        if i == 0:
            reconstr_seq.insert(0, f"Insert {dst[j - 1]} at beginning")
            j -= 1
        elif j == 0 or substr_edits[i, j] == 1 + substr_edits[i - 1, j]:
            reconstr_seq.insert(0, f"Delete {src[i - 1]}")
            i -= 1
        elif substr_edits[i, j] == 1 + substr_edits[i, j - 1]:
            reconstr_seq.insert(0, f"Insert {dst[j - 1]} after {src[i - 1]}")
            j -= 1
        elif src[i - 1] == dst[j - 1]:
            i -= 1
            j -= 1
        else:
            reconstr_seq.insert(0, f"Substitute {dst[j - 1]} for {src[i - 1]}")
            i -= 1
            j -= 1

    return reconstr_seq

def scoring(src: str, dst: str) -> float:
    """Compute the score of an edit distance metric

    Arguments:
    distance      -- edit distance
    max_distance  -- max edit distance 
    """

    len_src = len(src)
    len_dst = len(dst)

    max_len = len_src if len_src > len_dst else len_dst
    distance = edit_distance(src, dst)

    if distance == 0:
        return 1.0

    return round(1 - (distance / float(max_len)), 3)
