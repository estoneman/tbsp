"""Domain name similarity using sliding windows and multiprocessing
"""

from itertools import combinations
import math
import multiprocessing as mp
import os

import numpy as np

import edit_distance
import util

def top_k(domains,
          n_domains: int,
          window_size: int,
          k: int,
          threshold: float=0.70) -> list[str]:
    """Scores top k domains per window

    Positional Arguments:
    domains     -- input domains
    n_domains   -- total input domains
    k           -- number of maximum scores to store per window
    window_size -- size of window

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
        for _ in range(0, n_domains, window_size):
            assert window_size <= n_domains, \
                   "window length > # total domains:" \
                   f"({window_size} > {n_domains})"
            assert k <= window_size, f"k > window length: ({k} > {window_size})"

            if n_processed + window_size > n_domains:
                window_size = n_domains - n_processed
                k = math.ceil(0.5*window_size)

            n_uniq = int(window_size * (window_size - 1) / 2)
            window_scores = np.empty(n_uniq, dtype=np.float32)

            print(f"  current window: {current_window}\n"
                  f"    window size: {window_size}")

            window = util.take(domains, window_size)
            unique_pairs = list(combinations(window, r=2))

            scores = pool.imap(edit_distance.score, unique_pairs)
            for j in range(n_uniq):
                current_score = next(scores)
                if current_score > threshold:
                    window_scores[j] = current_score

            k_top = np.argpartition(window_scores, -k)
            for idx in k_top[-k:]:
                global_max.append(unique_pairs[idx])

            n_processed += window_size
            current_window += 1

    return global_max
