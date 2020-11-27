import unittest
from routes import *


class PlusOneTests(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(plus_one("1"), "2")

    def test_negative(self):
        self.assertEqual(plus_one("-2"), "-1")

    def test_zero(self):
        self.assertEqual(plus_one("0"), "1")

    def test_letter(self):
        self.assertEqual(plus_one("a"), "Invalid input.")


class SortTests(unittest.TestCase):
    def test_sorted(self):
        self.assertEqual(sort("[1, 2, 3]"), "[1, 2, 3]")

    def test_unsorted(self):
        self.assertEqual(sort("[3, 2, 1]"), "[1, 2, 3]")

    def test_empty(self):
        self.assertEqual(sort(""), "[]")


class Base64Tests(unittest.TestCase):
    def test_full_encode_decode(self):
        in_str = "these tests are so contrived"
        encoded = base64_encode(in_str)
        decoded = base64_decode(encoded)
        self.assertEqual(decoded, in_str)


class ToUpperTests(unittest.TestCase):
    def test_digit(self):
        self.assertEqual(to_upper("1"), "1")

    def test_lower(self):
        self.assertEqual(to_upper("a"), "A")

    def test_upper(self):
        self.assertEqual(to_upper("A"), "A")

    def test_empty(self):
        self.assertEqual(to_upper(""), "")


if __name__ == "__main__":
    unittest.main()
