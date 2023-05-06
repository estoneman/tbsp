"""Statistic computation module"""

from types import GeneratorType
from enum import Enum
from statistics import fmean, stdev

import numpy as np

class StatType(Enum):
    """Set of supported statistics"""
    TOP_K = 1
    MEAN = 2
    MAX = 4
    MIN = 8
    STD_DEV = 16

def compute_stats(pair_scores: GeneratorType, flags: int) -> None:
    """Compute a variety of statistics (see above for supported flags)

    PositionalArguments:
    pair_scores -- unique pairs of a window with respective scores
    flags -- bit mask of desired statistics to compute
    """
    pair_score_index = {idx:(ps[0], round(ps[1], 3))
                        for idx,ps in enumerate(pair_scores)}

    scores = [pair[1] for pair in pair_score_index.values()]
    len_scores = len(scores)

    if flags & StatType.TOP_K.value != 0:
        locs = win_top_k(scores)
        max_len = 0
        for loc in locs:
            pair,_ = pair_score_index[loc]
            max_pair_len = max(len(pair[0]), len(pair[1]))
            if max_pair_len > max_len:
                max_len = max_pair_len

        print("    Top 5 Scores:")
        for loc in locs:
            pair,score = pair_score_index[loc]
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
            pair,score = pair_score_index[0]
            print("      - {} | {} | {:.3f}".format(pair[0].decode(),
                                                    pair[1].decode(),
                                                    score))
        else:
            print("    Max Score:")
            loc = win_max(scores)
            pair,score = pair_score_index[loc]
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
            pair,score = pair_score_index[0]
            print("      - {} | {} | {:.3f}".format(pair[0].decode(),
                                                    pair[1].decode(),
                                                    score))
        else:
            print("    Min Score:")
            loc = win_min(scores)
            pair,score = pair_score_index[loc]
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
            print("      - {:.3f}".format(win_std_dev(scores)))

    if flags & StatType.MEAN.value != 0:
        if len_scores < 1:
            print("\x1b[33m+")
            print("| Warning: `mean` stat not computed. Either the\n"
                  "| current window is empty or the threshold filtered\n"
                  "| all scores")
            print("+\x1b[0m")
        else:
            print("    Mean Score:")
            print("      - {:.3f}".format(win_mean(scores)))

def win_top_k(scores, k: int=5):
    """top k scores from window"""
    num_scores = len(scores)
    if num_scores < k:
        k = num_scores
    k_top = np.argpartition(scores, -k)

    return k_top[-k:]

def win_min(scores):
    """minimum score from window"""
    return np.argpartition(scores, 1)[0]

def win_max(scores):
    """maximum score from window"""
    return np.argpartition(scores, -1)[-1]

def win_mean(scores):
    """average score"""
    return fmean(scores)

def win_std_dev(scores):
    """standard deviation of scores"""
    return stdev(scores)
