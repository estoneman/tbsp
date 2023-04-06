"""Statistics-computing extension of the sliding windows system
"""

from enum import Enum

import numpy as np

class StatType(Enum):
    """List of supported statistics"""
    TOP_K = 1
    MEAN = 2
    MAX = 4
    MIN = 8
    STD_DEV = 16

class Statistic:
    """Basic container for storing types of window statistics"""
    def __init__(self, Type, data):
        """Non-default constructor

        Positional Arguments:
        Type -- One of StatType statistics
        data -- Data returned from each statistic computation

        **NOTE**: Capitalized `Type` is used to avoid name conflict with
                  `type()` builtin function
        """
        assert isinstance(Type, StatType), \
               f"Expected StatType, got {type}"

        self.Type = Type
        self.data = data

    def get_Type(self):
        """Getter: `Type`"""
        return self.Type

    def get_data(self):
        """Getter `data`"""
        return self.data

def stats_main(pair_scores: dict,
               flags: int) -> list:
    """Main entry point for statistic computing

    Positional Arguments:
    domains     -- window of domains
    flags       -- which stats to compute (bitwise OR format)
                   e.g. (TOP_K | MIN | STD_DEV)

    Returns:
    list of populated `Statistic` objects

    """
    top_k_scores = {}
    idx = 0
    for pair_score in pair_scores:
        top_k_scores[idx] = (pair_score[0], round(pair_score[1], 3))
        idx += 1


    scores = [pair[1] for pair in top_k_scores.values()]
    len_scores = len(scores)

    stats_list = []
    if flags & StatType.TOP_K.value != 0:
        locs = top_k(scores)

        data = []
        for loc in locs:
            data.append(top_k_scores[loc])

        stats_list.append(Statistic(StatType.TOP_K, data))
    if flags & StatType.MEAN.value != 0:
        print("StatType.MEAN unimplemented")
        stats_list.append(None)
    if flags & StatType.MAX.value != 0:
        if len_scores == 0:
            print("\x1b[33m" + "="*6)
            print("Warning: `max` stat not computed. Either the\n"
                  "current window is empty or the threshold kept too many\n"
                  "values out")
            print("\x1b[0m")
        elif len_scores == 1:
            stats_list.append(Statistic(StatType.MAX, top_k_scores[0]))
        else:
            loc = win_max(scores)
            data = top_k_scores[loc]

            stats_list.append(Statistic(StatType.MAX, data))
    if flags & StatType.MIN.value != 0:
        if len_scores == 0:
            print("\x1b[33m" + "="*6)
            print("Warning: `min` stat computed. Either the current\n"
                  "window is empty or the threshold kept too many values\n"
                  "out")
            print("="*6 + "\x1b[0m")
        elif len_scores == 1:
            stats_list.append(Statistic(StatType.MIN, top_k_scores[0]))
        else:
            loc = win_min(scores)
            data = top_k_scores[loc]

            stats_list.append(Statistic(StatType.MIN, data))
    if flags & StatType.STD_DEV.value != 0:
        print("StatType.STD_DEV unimplemented")
        stats_list.append(None)

    return stats_list

def win_min(scores):
    """minimum score from a window of domains"""
    return np.argpartition(scores, 1)[0]

def win_max(scores):
    """maximum score from a window of domains"""
    return np.argpartition(scores, -1)[-1]

def top_k(scores, k: int=5):
    """top k scores from a window of domains"""
    num_scores = len(scores)
    if num_scores < k:
        k = num_scores
    k_top = np.argpartition(scores, -k)

    return k_top[-k:]
