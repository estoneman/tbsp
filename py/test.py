import os
import unittest

from sliding_window import SlidingWindow
import win_util

class TestTbsp(unittest.TestCase):
    def setUp(self):
        fn = "corpus.txt"
        
        domains = [
            "google.com",
            "nike.com",
            "chat.openai.com",
            "colorado.edu",
            "www.thebikerack.com",
        ]

        with open(fn, "w") as fp:
            for d in domains:
                fp.write(d + "\n")

    def tearDown(self):
        os.unlink("corpus.txt")

    def test_take(self):
        xs = (x for x in range(100))
        n = 10

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
        fn = "corpus.txt"

        lines = list(win_util.fetch_lines(fn))

        self.assertEqual(len(lines), 5)

    def test_sliding_window_get_data(self):
        fn = "corpus.txt"
        window_len = 2

        corpus = win_util.fetch_lines(fn)

        window = SlidingWindow(corpus, window_len)
        self.assertListEqual(list(window.get_data()),
                             [b"google", b"nike"])


    def test_sliding_window_get_size(self):
        fn = "corpus.txt"
        window_len = 2

        corpus = win_util.fetch_lines(fn)
        window = SlidingWindow(corpus, window_len)
        self.assertEqual(window.get_size(), window_len)

    def test_sliding_window_set_data(self):
        fn = "corpus.txt"
        window_len = 2

        corpus = win_util.fetch_lines(fn)
        window = SlidingWindow(corpus, window_len)
        previous_data = window.get_data()
        window.set_data([b"foo",b"bar"])

        self.assertNotEqual(window.get_data(), previous_data)

    def test_sliding_window_set_size(self):
        fn = "corpus.txt"
        window_len = 2

        corpus = win_util.fetch_lines(fn)
        window = SlidingWindow(corpus, window_len)
        
        previous_size = window.get_size()
        window.set_size(1000)

        self.assertNotEqual(window.get_size(), previous_size)

    def test_sliding_window_max(self):
        fn = "corpus.txt"
        window_len = 10
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)
        
        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_max = window.max(scores)

        self.assertEqual(window_max, 9)

    def test_sliding_window_min(self):
        fn = "corpus.txt"
        window_len = 10
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)

        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_min = window.min(scores)

        self.assertEqual(window_min, 0)

    def test_sliding_window_mean(self):
        fn = "corpus.txt"
        window_len = 10 
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)

        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_mean = window.mean(scores)

        self.assertEqual(window_mean, sum(scores) / 10)

    def test_sliding_window_std_dev(self):
        fn = "corpus.txt"
        window_len = 10
        scores = range(window_len)
        corpus = win_util.fetch_lines(fn)

        # dummy window
        window = SlidingWindow(corpus, window_len)
        window_std_dev = window.std_dev(scores)

        self.assertEqual(int(window_std_dev), 3)

    def test_sliding_window_resize(self):
        fn = "corpus.txt"
        corpus = win_util.fetch_lines(fn)

        n = 100
        window_len = 10
        window = SlidingWindow(corpus, window_len)
        
        # simulate we are at end of last window
        n_processed = n

        # request another window, should not give any data to new window
        request = window_len
        window.resize(n, n_processed, request)
        self.assertEqual(window.get_size(), 0)


    """
    slide,
    top_k
    """

if __name__ == "__main__":
    unittest.main()
