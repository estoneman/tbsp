import os
import unittest

import win_util

class TestTbsp(unittest.TestCase):
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
        fn = "sample.txt"
        with open(fn, "w") as fp:
            fp.write("google.com\n")
            fp.write("chat.openai.com\n")

        lines = list(win_util.fetch_lines(fn))
        os.unlink(fn)

        self.assertEqual(len(lines), 2)

if __name__ == "__main__":
    unittest.main()
