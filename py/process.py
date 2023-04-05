"""Domain name similarity using sliding windows and multiprocessing
"""

from itertools import combinations
import multiprocessing as mp
import os
import time

import numpy as np

import edit_distance
from sliding_window import SlidingWindow

def work(function, data, size, n_procs=1):
    with mp.Pool(processes=n_procs) as pool:
        scores = pool.imap(function, data, int(size / 4))

    return scores

def top_k(domains,
          n: int,
          w: int,
          threshold: float=0.70,
          k: int=5) -> None:
    """Scores top k domains per window

    Positional Arguments:
    domains     -- input domains
    n           -- total input domains
    k           -- number of maximum scores to store per window
    w           -- size of window

    Keyword Arguments:
    threshold   -- minimum score to keep per window
    k           -- for top-k computation, if selected 

    Returns:
    list of top k domains
    """

    n_procs = int(os.cpu_count() / 2)
    n_processed = 0

    current_window = 0
    window = SlidingWindow(domains, w, k)

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

            t1 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
            # scores = pool.imap(edit_distance.score_pair,
            #                    unique_pairs,
            #                    int(n_uniq / 4))
            work(edit_distance.score_pair, unique_pairs, n_uniq, n_procs)

            t2 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
            n_processed += window.get_size()

            elapsed = round((t2 - t1) / float(10e9), 3)
            window.slide(domains, n, n_processed, elapsed)
            print(f"    ttc: {elapsed}s")
            if window.get_size() > 0:
                print(f"    next window size: {window.get_size()}")
            else:
                print("END OF DATA")

if __name__ == "__main__":
    import util

    words = util.fetch_lines("/usr/local/opt/wordlists/rockyou/rockyou.txt")
    n = 100000
    w = int(0.25*n)

    print(f"# domains: {n}")
    top_k(words, n, w)
