"""Domain name similarity using sliding windows and multiprocessing"""

from itertools import combinations
import multiprocessing as mp
import os
import time

import numpy as np

import edit_distance
from sliding_window import SlidingWindow
from win_stat import StatType

def work(function, data, n_procs, threshold=0.70):
    """Multiprocessed helper for scoring pairs of domains

    Positional Arguments:
    function    -- scoring function
    data        -- data to score (subdomains)
    n_procs     -- number of processes to spawn

    Keyword Arguments:
    threshold   -- minimum score to keep

    Returns:
    list of word pairs and respective scores
        e.g. (('domain1.com', 'domain2.com'), 0.900)
    """

    buf = []

    with mp.Pool(processes=n_procs) as pool:
        for pair in pool.imap(function, data, 2):
            if pair[1] > threshold:
                buf.append(pair)

    return buf

def process_windows(domains,
                    n: int,
                    threshold: int,
                    flags: int) -> None:
    """Scores top k subdomains per window

    Positional Arguments:
    domains     -- input subdomains
    n           -- total input subdomains
    threshold   -- minimum score to keep
    flags       -- window statistics flags, see `util.py` for list of supported
                   statistics

    Returns:
    matrix of subdomains and their respective similarities
    """

    n_procs = int(os.cpu_count() / 2)
    n_processed = 0

    current_window = 1

    win_max = 1000
    win_min = 600
    if n <= win_max:
        win_min = win_max = n

    window = SlidingWindow(domains, win_min, win_min, win_max)

    sim_mat = np.full((n,n), 0.000, dtype=np.float64)

    # === BEGIN WINDOW PROCESSING === #
    while n_processed < n:
        assert window.get_size() <= n, \
               "window length > # total domains: " \
               f"({window.get_size()} > {n})"

        # === GENERATE UNIQUE PAIRS ===
        n_uniq = int(window.get_size() * (window.get_size() - 1) / 2)

        print(f"  Window {current_window}\n"
              f"    Size: {window.get_size()} Domains\n"
              f"    Unique Pairs: {n_uniq}")

        unique_pairs = combinations(window.get_data(), r=2)

        # === SCORE PAIRS OF DOMAINS ===
        start = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
        pair_scores = work(edit_distance.score_pair, unique_pairs,
                           n_procs, threshold)
        end = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)

        # === COMPUTE STATS ===
        top_k_scores = {idx:(ps[0], round(ps[1], 3))
                        for idx,ps in enumerate(pair_scores)}

        scores = [pair[1] for pair in top_k_scores.values()]
        len_scores = len(scores)

        if flags & StatType.TOP_K.value != 0:
            locs = window.top_k(scores)
            max_len = 0
            for loc in locs:
                pair,_ = top_k_scores[loc]
                max_pair_len = max(len(pair[0]), len(pair[1]))
                if max_pair_len > max_len:
                    max_len = max_pair_len

            print("    Top 5 Scores:")
            for loc in locs:
                pair,score = top_k_scores[loc]
                print("      - {:{}} | {:{}} | {:.3f}".format(pair[0].decode(),
                                                         max_len,
                                                         pair[1].decode(),
                                                         max_len,
                                                         score))

        if flags & StatType.MAX.value != 0:
            if len_scores == 0:
                print("\x1b[33m+")
                print("| Warning: `max` stat not computed. Either the\n"
                      "| current window is empty or the threshold filtered\n"
                      "| all scores")
                print("+\x1b[0m")
            elif len_scores == 1:
                print("    Max Score:")
                pair,score = top_k_scores[0]
                print("      - {} | {} | {:.3f}".format(pair[0].decode(),
                                                        pair[1].decode(),
                                                        score))
            else:
                print("    Max Score:")
                loc = window.max(scores)
                pair,score = top_k_scores[loc]
                print("      - {} | {} | {:.3f}".format(pair[0].decode(),
                                                        pair[1].decode(),
                                                        score))
        if flags & StatType.MIN.value != 0:
            if len_scores == 0:
                print("\x1b[33m+")
                print("| Warning: `min` stat not computed. Either the current\n"
                      "| window is empty or the threshold filtered all scores")
                print("+\x1b[0m")
            elif len_scores == 1:
                print("    Min Score:")
                pair,score = top_k_scores[0]
                print("      - {} | {} | {:.3f}".format(pair[0].decode(),
                                                        pair[1].decode(),
                                                        score))
            else:
                print("    Min Score:")
                loc = window.min(scores)
                pair,score = top_k_scores[loc]
                print("      - {} | {} | {:.3f}".format(pair[0].decode(),
                                                        pair[1].decode(),
                                                        score))
        if flags & StatType.STD_DEV.value != 0:
            if len_scores < 2:
                print("\x1b[33m+")
                print("| Warning: `std_dev` stat not computed. Either the\n"
                      "| current window is empty or the threshold\n"
                      "| filtered all scores")
                print("+\x1b[0m")
            else:
                print("    Standard Deviation:")
                print("      - {:.3f}".format(window.std_dev(scores)))

        if flags & StatType.MEAN.value != 0:
            if len_scores < 1:
                print("\x1b[33m+")
                print("| Warning: `mean` stat not computed. Either the\n"
                      "| current window is empty or the threshold filtered\n"
                      "| all scores")
                print("+\x1b[0m")
            else:
                print("    Mean Score:")
                print("      - {:.3f}".format(window.mean(scores)))

        # === POPULATE SIMILARITY MATRIX ===
        for pair_score in pair_scores:
            pair,score = pair_score
            x,y = (hash(pair[0]) % window.get_size()), \
                  (hash(pair[1]) % window.get_size())

            sim_mat[x + n_processed,y + n_processed] = score

        # === PREPARE NEXT WINDOW ===
        n_processed += window.get_size()
        current_window += 1
        elapsed = round((end - start) / float(10e9), 3)
        window.slide(domains, n, n_processed, elapsed)

    return sim_mat
