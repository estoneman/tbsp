"""Domain name similarity using sliding windows and multiprocessing
"""

from itertools import combinations
import multiprocessing as mp
import os
import time

import edit_distance
from sliding_window import SlidingWindow
from win_stat import StatType

def work(function, data, size, n_procs, threshold=0.70):
    """Multiprocessed helper for scoring pairs of domains

    Positional Arguments:
    function    -- scoring function
    data        -- data to score
    size        -- amount of data to score
    n_procs     -- number of processes to spawn

    Keyword Arguments:
    threshold   -- minimum score to keep

    Returns:
    list of word pairs and respective scores
    """
    print("    START worker\n"
          f"      threshold: {threshold}\n"
          f"      processes: {n_procs}\n"
          f"      total: {size}")

    n_skipped = 0
    buf = []

    with mp.Pool(processes=n_procs) as pool:
        for pair in pool.imap(function, data, 2):
            if pair[1] > threshold:
                buf.append(pair)
            else:
                n_skipped += 1

    print(f"      skipped: {n_skipped}")
    print(f"      added: {len(buf)}")

    return buf

def process_windows(domains,
                    n: int,
                    w: int,
                    threshold: int,
                    flags: int) -> None:
    """Scores top k domains per window

    Positional Arguments:
    domains     -- input domains
    n           -- total input domains
    w           -- size of window
    threshold   -- minimum score to keep
    flags  -- window statistics flags, see `util.py` for list of supported
                   statistics

    Returns:
    pairs of domains with their respective similarity scores
    """

    n_procs = int(os.cpu_count() / 2)
    n_processed = 0

    current_window = 0
    window = SlidingWindow(domains, w)

    # === BEGIN WINDOW SCORE COMPUTATION === #
    while n_processed < n:
        assert window.get_size() <= n, \
               "window length > # total domains:" \
               f"({window.get_size()} > {n})"

        current_window += 1

        n_uniq = int(window.get_size() * (window.get_size() - 1) / 2)

        print(f"  current window: {current_window}\n"
              f"    window size: {window.get_size()}")

        unique_pairs = combinations(window.get_data(), r=2)

        start = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
        pair_scores = work(edit_distance.score_pair, unique_pairs,
                           n_uniq, n_procs, threshold)
        end = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)

        print("    END worker")
        print("    START stats_main")
        top_k_scores = {}
        idx = 0
        for pair_score in pair_scores:
            top_k_scores[idx] = (pair_score[0], round(pair_score[1], 3))
            idx += 1

        scores = [pair[1] for pair in top_k_scores.values()]
        len_scores = len(scores)

        stats_list = []
        if flags & StatType.TOP_K.value != 0:
            locs = window.top_k(scores)

            data = []
            for loc in locs:
                data.append(top_k_scores[loc])

            stats_list.append(data)
        if flags & StatType.MEAN.value != 0:
            print("StatType.MEAN unimplemented")
            stats_list.append(None)
        if flags & StatType.MAX.value != 0:
            if len_scores == 0:
                print("\x1b[33m" + "="*6)
                print("Warning: `max` stat not computed. Either the\n"
                      "current window is empty or the threshold filtered all\n"
                      "scores")
                print("\x1b[0m")
            elif len_scores == 1:
                stats_list.append(top_k_scores[0])
            else:
                loc = window.max(scores)
                data = top_k_scores[loc]

                stats_list.append(data)
        if flags & StatType.MIN.value != 0:
            if len_scores == 0:
                print("\x1b[33m" + "="*6)
                print("Warning: `min` stat not computed. Either the current\n"
                      "window is empty or the threshold filtered all scores")
                print("="*6 + "\x1b[0m")
            elif len_scores == 1:
                stats_list.append(top_k_scores[0])
            else:
                loc = window.min(scores)
                data = top_k_scores[loc]

                stats_list.append(data)
        if flags & StatType.STD_DEV.value != 0:
            print("StatType.STD_DEV unimplemented")
            stats_list.append(None)

        for stat in stats_list:
            if stat is not None:
                print(stat)

        n_processed += window.get_size()
        elapsed = round((end - start) / float(10e9), 3)
        window.slide(domains, n, n_processed, elapsed)
        print(f"    processed: {n_processed}\n"
              f"    ttc: {elapsed}s")

        if window.get_size() > 0:
            print(f"    next window size: {window.get_size()}")


    print("END OF DATA")
