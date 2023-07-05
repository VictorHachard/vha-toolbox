import unittest

from vha_toolbox import format_file_size


class FormatFileSizeTestCase(unittest.TestCase):
    def test_format_file_size(self):
        self.assertEqual(format_file_size(0), "0.0 B")
        self.assertEqual(format_file_size(1023), "1023.0 B")
        self.assertEqual(format_file_size(1024), "1.0 KB")
        self.assertEqual(format_file_size(123456789), "117.7 MB")
        self.assertEqual(format_file_size(1000000000000), "931.3 GB")
        self.assertEqual(format_file_size(999999999999999999), "888.2 PB")

    def test_format_file_size_with_different_decimal_place(self):
        self.assertEqual(format_file_size(1023, decimal_places=0), "1023 B")
        self.assertEqual(format_file_size(1023, decimal_places=2), "1023.00 B")
        self.assertEqual(format_file_size(1024, decimal_places=0), "1 KB")
        self.assertEqual(format_file_size(123456789, decimal_places=1), "117.7 MB")
        self.assertEqual(format_file_size(1000000000000, decimal_places=3), "931.323 GB")
        self.assertEqual(format_file_size(999999999999999999, decimal_places=4), "888.1784 PB")

    def test_format_file_size_error(self):
        self.assertRaises(ValueError, format_file_size, -100)
        self.assertRaises(ValueError, format_file_size, -1)


if __name__ == '__main__':
    unittest.main()
