"""Definition and specification of a sliding window in my current 
implementation
"""

import math
from statistics import fmean, stdev

import numpy as np

import win_util

class SlidingWindow:
    """Discrete type for processing large sets of data"""
    def __init__(self, corpus, size):
        """Non-default constructor"""
        self.data = win_util.take(corpus, size)
        self.size = size

    def set_data(self, data):
        """Setter"""
        self.data = data

    def set_size(self, size):
        """Setter"""
        self.size = size

    def get_data(self):
        """Getter"""
        return self.data

    def get_size(self):
        """Getter"""
        return self.size

    def resize(self, n, n_processed, request):
        """Ensure proper access of corpus data

        Positional Arguments:
        n           -- total amount of data to be read
        n_processed -- total amount of data read so far
        requested   -- total amount of data requested to be read

        Returns:
        None
        """
        if n_processed + request > n:
            self.set_size(n - n_processed)
        else:
            self.set_size(self.get_size() + request)

    def slide(self, corpus, n, n_processed, elapsed):
        """Move window given an amount to advance by

        Positional Arguments:
        corpus      -- original data to read from
        n           -- total amount of data in corpus
        n_processed -- total amount of data read so far
        elapsed     -- total amount of time to compute current window
        """
        request = int(self.get_size() * math.exp(elapsed))
        # request = self.get_size() + \
        #           int(self.get_size() * win_util.sigmoid(-elapsed + 6))

        self.resize(n, n_processed, request)
        self.set_data(win_util.take(corpus, self.get_size()))

    def top_k(self, scores, k: int=5):
        """top k scores from window"""
        num_scores = len(scores)
        if num_scores < k:
            k = num_scores
        k_top = np.argpartition(scores, -k)

        return k_top[-k:]

    def min(self, scores):
        """minimum score from window"""
        return np.argpartition(scores, 1)[0]

    def max(self, scores):
        """maximum score from window"""
        return np.argpartition(scores, -1)[-1]

    def mean(self, scores):
        """average score"""
        return fmean(scores)

    def std_dev(self, scores):
        """standard deviation of scores"""
        return stdev(scores)
