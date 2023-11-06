import unittest

from vha_toolbox import format_readable_size, to_bytes


class FormatSizeTestCase(unittest.TestCase):
    def test_format_readable_size(self):
        self.assertEqual(format_readable_size(0), "0.0 B")
        self.assertEqual(format_readable_size(1023), "1023.0 B")
        self.assertEqual(format_readable_size(1024), "1.0 KB")
        self.assertEqual(format_readable_size(123456789), "117.7 MB")
        self.assertEqual(format_readable_size(1000000000000), "931.3 GB")
        self.assertEqual(format_readable_size(999999999999999999), "888.2 PB")

    def test_format_readable_size_with_different_decimal_place(self):
        self.assertEqual(format_readable_size(1023, decimal_places=0), "1023 B")
        self.assertEqual(format_readable_size(1023, decimal_places=2), "1023.00 B")
        self.assertEqual(format_readable_size(1024, decimal_places=0), "1 KB")
        self.assertEqual(format_readable_size(123456789, decimal_places=1), "117.7 MB")
        self.assertEqual(format_readable_size(123456789, decimal_places=2), "117.74 MB")
        self.assertEqual(format_readable_size(1000000000000, decimal_places=3), "931.323 GB")
        self.assertEqual(format_readable_size(999999999999999999, decimal_places=4), "888.1784 PB")

    def test_format_readable_size_error(self):
        self.assertRaises(ValueError, format_readable_size, -100)
        self.assertRaises(ValueError, format_readable_size, -1)

    def test_to_bytes(self):
        self.assertEqual(to_bytes("0 B"), 0)
        self.assertEqual(to_bytes("1023 B"), 1023)
        self.assertEqual(to_bytes("1 KB"), 1024)
        self.assertEqual(to_bytes("117.73 MB"), 123448852)
        self.assertEqual(to_bytes("117.7 MB"), 123417395)
        self.assertEqual(to_bytes("931.3 GB"), 999975760691)
        self.assertEqual(to_bytes("888.1784 PB"), 999999977819630848)

    def test_to_bytes_error(self):
        self.assertRaises(ValueError, to_bytes, "0")
        self.assertRaises(ValueError, to_bytes, "1")
        self.assertRaises(ValueError, to_bytes, "1.0 B B")
        self.assertRaises(ValueError, to_bytes, "-1")
        self.assertRaises(ValueError, to_bytes, "-1.0 B")


if __name__ == '__main__':
    unittest.main()
