"""Domain name similarity using sliding windows and multiprocessing
"""

from itertools import combinations
import math
import multiprocessing as mp
import os

import numpy as np

import edit_distance
import util

def adjust_window(w: int, k: int, n: int, n_processed: int) -> int:
    """Window size check (TODO: scale window)

    Positional Arguments:
    w           -- current window size
    k           -- current amount of domains to store per window
    n           -- total number of domains
    n_processed -- total number of domains already read

    Returns updated w and k
    """
    if n_processed + w > n:
        w = n - n_processed
        k = math.ceil(0.5*w)

    return (w,k)

def top_k(domains,
          n: int,
          w: int,
          k: int,
          threshold: float=0.70) -> list[str]:
    """Scores top k domains per window

    Positional Arguments:
    domains     -- input domains
    n   -- total input domains
    k           -- number of maximum scores to store per window
    w -- size of window

    Keyword Arguments:
    threshold -- minimum score to keep per window

    Returns:
    list of top k domains
    """

    n_procs = int(os.cpu_count() / 2)
    n_processed = 0

    global_max = []
    with mp.Pool(processes=n_procs) as pool:
        current_window = 1
        for _ in range(0, n, w):
            assert w <= n, \
                   "window length > # total domains:" \
                   f"({w} > {n})"
            assert k <= w, f"k > window length: ({k} > {w})"

            w,k = adjust_window(w, k, n, n_processed)

            n_uniq = int(w * (w - 1) / 2)
            window_scores = np.empty(n_uniq, dtype=np.float32)

            print(f"  current window: {current_window}\n"
                  f"    window size: {w}")

            window = util.take(domains, w)
            unique_pairs = list(combinations(window, r=2))

            scores = pool.imap(edit_distance.score, unique_pairs)
            for j in range(n_uniq):
                current_score = next(scores)
                if current_score > threshold:
                    window_scores[j] = current_score

            k_top = np.argpartition(window_scores, -k)
            for idx in k_top[-k:]:
                global_max.append(unique_pairs[idx])

            n_processed += w
            current_window += 1

    return global_max
