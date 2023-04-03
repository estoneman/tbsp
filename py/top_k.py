"""Domain name similarity using sliding windows and multiprocessing
"""

from itertools import combinations
import multiprocessing as mp
import os
import time

import numpy as np

import edit_distance
from sliding_window import SlidingWindow

def top_k(domains,
          n: int,
          w: int,
          k: int,
          threshold: float=0.70) -> list[str]:
    """Scores top k domains per window

    Positional Arguments:
    domains     -- input domains
    n           -- total input domains
    k           -- number of maximum scores to store per window
    w           -- size of window

    Keyword Arguments:
    threshold -- minimum score to keep per window

    Returns:
    list of top k domains
    """

    n_procs = int(os.cpu_count() / 2)
    n_processed = 0

    current_window = 0
    window = SlidingWindow(domains, w, k)

    global_max = []
    with mp.Pool(processes=n_procs) as pool:
        while n_processed < n:
            assert window.get_size() <= n, \
                   "window length > # total domains:" \
                   f"({window.get_size()} > {n})"
            assert window.get_k() <= window.get_size(), \
                   "k > window length: " \
                   f"({window.get_k()} > {window.get_size()})"

            current_window += 1

            n_uniq = int(window.get_size() * (window.get_size() - 1) / 2)

            print(f"  current window: {current_window}\n"
                  f"    window size: {window.get_size()}")

            unique_pairs = combinations(window.get_data(), r=2)
            scores = pool.imap(edit_distance.score_pair,
                               unique_pairs,
                               int(n_uniq / 4))

            t1 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
            top_k_scores = {}
            idx = 0
            for pair_score in scores:
                if pair_score[1] > threshold:
                    # top_k_scores.append((pair, sc))
                    top_k_scores[idx] = pair_score[0], round(pair_score[1], 3)
                    idx += 1

            t2 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
            elapsed = round((t2 - t1) / 10e9, 3)
            print("    ttc: {0:.3f}s".format(elapsed))

            window.set_k(
                len(top_k_scores) if len(top_k_scores) < k else k
            )
            print(f"    k: {window.get_k()}")

            scores = [pair[1] for pair in top_k_scores.values()]
            k_top = np.argpartition(scores, window.get_k()*-1)
            for idx in k_top[window.get_k()*-1:]:
                # global_max.append(float("{0:.3f}".format(top_k_scores[idx])))
                global_max.append(top_k_scores[idx])

            n_processed += window.get_size()
            request = window.get_size() << 1
            window.slide(domains, n, n_processed, request)

    return global_max
