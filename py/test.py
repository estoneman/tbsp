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

if __name__ == "__main__":
    unittest.main()
