import os
import unittest

from edit_distance import edit_distance
from sliding_window import SlidingWindow
import win_util

class TestTbsp(unittest.TestCase):
    def setUp(self):
        domains = [
            "google.com",
            "nike.com",
            "chat.openai.com",
            "colorado.edu",
            "www.thebikerack.com",
            "flu.me",
            "wikipedia.org",
            "dns1.microsoft.com",
            "example.com",
            "youtube.com",
        ]
        global n, fn
        n = len(domains)
        fn = "corpus.txt"

        with open(fn, "w") as fp:
            for d in domains:
                fp.write(d + "\n")

    def tearDown(self):
        os.unlink(fn)

    def test_take(self):
        xs = (x for x in range(100))

        subset = list(win_util.take(xs, n))
        self.assertEqual(len(subset), n)

    def test_remove_tld(self):
        domain = "dns1.google.com"
        stripped = win_util.remove_tld(domain)

        self.assertEqual(stripped, "dns1.google")

    def test_is_iterable(self):
        x = 10
        is_it = win_util.is_iterable(x)

        self.assertFalse(is_it)

    def test_fetch_lines(self):
        lines = list(win_util.fetch_lines(fn))

        self.assertEqual(len(lines), n)

    def test_sliding_window_get_data(self):
        window_len = 6

        corpus = win_util.fetch_lines(fn)

        window = SlidingWindow(corpus, window_len)
        self.assertListEqual(list(window.get_data()),
                             [b"google", b"nike", b"chat.openai",
                              b"colorado", b"www.thebikerack", b"flu"])

    def test_sliding_window_get_size(self):
        window_len = 6

        corpus = win_util.fetch_lines(fn)
        window = SlidingWindow(corpus, window_len)
        self.assertEqual(window.get_size(), window_len)

    def test_sliding_window_set_data(self):
        window_len = 6

        corpus = win_util.fetch_lines(fn)
        window = SlidingWindow(corpus, window_len)
        previous_data = window.get_data()
        window.set_data([b"foo",b"bar"])

        self.assertNotEqual(window.get_data(), previous_data)

    def test_sliding_window_set_size(self):
        window_len = 6

        corpus = win_util.fetch_lines(fn)
        window = SlidingWindow(corpus, window_len)
        
        previous_size = window.get_size()
        window.set_size(1000)

        self.assertNotEqual(window.get_size(), previous_size)

    def test_sliding_window_max(self):
        window_len = 6
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)
        
        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_max = window.max(scores)

        self.assertEqual(window_max, 5)

    def test_sliding_window_min(self):
        window_len = 6
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)

        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_min = window.min(scores)

        self.assertEqual(window_min, 0)

    def test_sliding_window_mean(self):
        window_len = 6 
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)

        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_mean = window.mean(scores)

        self.assertEqual(window_mean, sum(scores) / window_len)

    def test_sliding_window_std_dev(self):
        window_len = 6
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)

        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_std_dev = round(window.std_dev(scores), 3)

        self.assertEqual(window_std_dev, 1.871)

    def test_sliding_window_top_k(self):
        corpus = win_util.fetch_lines(fn)

        window_len = 6
        window = SlidingWindow(corpus, window_len)

        scores = range(window_len)
        window_top_k = window.top_k(scores)

        # k is set at 5
        self.assertListEqual(list(window_top_k), [1, 2, 3, 4, 5])

    def test_sliding_window_resize(self):
        corpus = win_util.fetch_lines(fn)

        window_len = 6
        window = SlidingWindow(corpus, window_len)
        
        # simulate we are at end of last window
        n_processed = n

        # request another window, should not give any data to new window
        request = window_len
        window.resize(n, n_processed, request)
        self.assertEqual(window.get_size(), 0)

    def test_sliding_window_slide(self):
        corpus = win_util.fetch_lines(fn)

        window_len = 6
        window = SlidingWindow(corpus, window_len)

        # simulate we are at offset 4 from start of corpus
        #     i.e. the last window length + n_processed < 4
        n_processed = 4

        # suppose our last window took 0 seconds to compute
        elapsed = 0

        previous_size = window.get_size()
        window.slide(corpus, n, n_processed, elapsed)

        self.assertEqual(window.get_size(), previous_size * 2)

    def test_edit_distance(self):
        subdomain1 = b"google"
        subdomain2 = b"dns.google"

        ed = edit_distance(subdomain1, subdomain2)

        # add 4 characters to beginning of `subdomain1` to equal `subodmain2`
        self.assertEqual(ed, 4)

if __name__ == "__main__":
    unittest.main()
