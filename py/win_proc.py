"""Domain name similarity using sliding windows and multiprocessing"""

from itertools import combinations, tee
import time
from types import GeneratorType

import numpy as np
from scipy.sparse import lil_matrix

import edit_distance
from sliding_window import SlidingWindow
from win_stat import compute_stats

def copy_generator(generator, num_copies=2):
    """Generates multiple copies of a given generator

    Positional Arguments:
    generator -- types.GeneratorType iterable to be copied

    Keyword Arguments:
    num_copies -- quantity of copies to construct
    """
    gens: tuple = tee(generator, num_copies)
    for gen in gens:
        yield gen

def uniprocessed_work(function: callable, data: GeneratorType, threshold=0.70):
    """Helper for scoring pairs of domains

    Positional Arguments:
    function    -- scoring function
    data        -- data to score (subdomains)

    Keyword Arguments:
    threshold   -- minimum score to keep

    Returns:
    list of word pairs and respective scores
        e.g. (('domain1.com', 'domain2.com'), 0.900)
    """
    return ((pair, round(score, 3)) for pair,score in \
            map(function, data) if score > threshold)

def process_windows(domains, n: int, threshold: int, flags: int) -> None:
    """Main window processor that includes optional statisical computation

    Positional Arguments:
    domains     -- input subdomains
    n           -- total input subdomains
    threshold   -- minimum score to keep
    flags       -- window statistics flags, see `util.py` for list of supported
                   statistics

    Returns:
    `scipy.lil_matrx` of subdomains and their respective similarities
    """

    n_processed = 0

    current_window = 1

    win_max = 4000
    win_min = 2000

    # make sure we don't compute on data we don't have
    if n <= win_max or n <= win_min:
        win_min = win_max = n

    window = SlidingWindow(domains, win_min, win_min, win_max)

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
        pair_scores = uniprocessed_work(edit_distance.score_pair, unique_pairs,
                                        threshold)

        # needed for both stats and similarity computations
        scores_for_stats, scores_for_sim_mat = copy_generator(pair_scores)

        # === COMPUTE STATS ===
        start = time.process_time()
        compute_stats(scores_for_stats, flags)

        # === POPULATE SIMILARITY MATRIX ===
        sim_mat = lil_matrix((n,n), dtype=np.float32)
        for pair_score in scores_for_sim_mat:
            pair,score = pair_score
            x,y = (hash(pair[0]) % window.get_size()), \
                  (hash(pair[1]) % window.get_size())

            sim_mat[x + n_processed, y + n_processed] = score

        elapsed = round(time.process_time() - start, 3)

        # === PREPARE NEXT WINDOW ===
        n_processed += window.get_size()
        current_window += 1
        print(f"    ttc: {elapsed}s")
        window.slide(domains, n, n_processed, elapsed)

    return sim_mat
