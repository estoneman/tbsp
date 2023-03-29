import math

import util

class SlidingWindow:
    def __init__(self, corpus, size):
        self.data = util.take(corpus, size)
        self.size = size
        self.k = math.ceil(0.5*self.get_size())

    def set_data(self, data):
        self.data = data

    def set_size(self, size):
        self.size = size

    def set_k(self, k):
        self.k = k

    def get_data(self):
        return self.data

    def get_size(self):
        return self.size

    def get_k(self):
        return self.k

    def bound(self, n, n_processed, requested):
        if n_processed + requested > n:
            self.set_size(n - n_processed)
        else:
            self.set_size(requested)

        self.set_k(math.ceil(0.5 * self.get_size()))

    def slide(self, corpus, n, n_processed, requested):
        self.bound(n, n_processed, requested)
        self.set_data(util.take(corpus, self.get_size()))
