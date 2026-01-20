import unittest
from solve import supports_tls, supports_ssl


class TestSolve(unittest.TestCase):
    def test_supports_tls(self):
        # abba[mnop]qrst supports TLS (abba outside square brackets).
        self.assertTrue(supports_tls("abba[mnop]qrst"))

        # abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
        self.assertFalse(supports_tls("abcd[bddb]xyyx"))

        # aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
        self.assertFalse(supports_tls("aaaa[qwer]tyui"))

        # ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).
        self.assertTrue(supports_tls("ioxxoj[asdfgh]zxcvbn"))

    def test_supports_ssl(self):
        # aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
        self.assertTrue(supports_ssl("aba[bab]xyz"))

        # xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
        self.assertFalse(supports_ssl("xyx[xyx]xyx"))

        # aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet;
        # the aaa sequence is not related, because the interior character must be different).
        self.assertTrue(supports_ssl("aaa[kek]eke"))

        # zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb,
        # even though zaz and zbz overlap).
        self.assertTrue(supports_ssl("zazbz[bzb]cdb"))


if __name__ == "__main__":
    unittest.main()
