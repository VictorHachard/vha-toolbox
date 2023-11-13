import unittest

from vha_toolbox import ISBN


class IsbnTestCase(unittest.TestCase):
    def test_valid_isbn_13(self):
        valid_isbn_13 = ISBN('978-1-86197-876-9')
        self.assertTrue(valid_isbn_13.is_valid())
        self.assertEqual(valid_isbn_13.break_down_isbn(), [
            'Prefix: 978', 'Registration group: 1', 'Registrant: 86197', 'Publication: 876', 'Check digit: 9'
        ])
        self.assertEqual(valid_isbn_13.format(), '978-1-86-197876-9')
        self.assertEqual(valid_isbn_13.to_isbn_13(), '978-1-86-197876-9')
        self.assertEqual(valid_isbn_13.to_ean_13(), '9781861978769')

    def test_valid_isbn_10(self):
        valid_isbn_10 = ISBN('0-306-40615-2')
        self.assertTrue(valid_isbn_10.is_valid())
        self.assertEqual(valid_isbn_10.break_down_isbn(), [
            'Group: 03', 'Publisher: 0640', 'Title: 615', 'Check digit: 2'
        ])
        self.assertEqual(valid_isbn_10.format(), '0-306-40615-2')
        self.assertEqual(valid_isbn_10.to_isbn_13(), '978-0-30-640615-7')
        self.assertEqual(valid_isbn_10.to_ean_13(), '9780306406157')

    def test_invalid_isbn(self):
        with self.assertRaises(ValueError):
            ISBN('3-16-148410-X1')  # Incorrect check digit
        with self.assertRaises(ValueError):
            ISBN('12345678901234')  # Invalid format

    def test_invalid_prefix(self):
        with self.assertRaises(ValueError):
            ISBN('0306406152').to_isbn_13("123")  # Invalid prefix
        with self.assertRaises(ValueError):
            ISBN('0306406152').to_ean_13("123")

    def test_string_representation(self):
        isbn_13 = ISBN('978-1-86197-876-9')
        self.assertEqual(str(isbn_13), '978-1-86-197876-9')
        self.assertEqual(repr(isbn_13), "ISBN(978-1-86-197876-9)")

    def test_valid_isbn_10_2(self):
        isbn = '2-9512774-2-3'
        isbn = ISBN(isbn)
        self.assertTrue(isbn.is_valid())
        self.assertEqual(isbn.break_down_isbn(), [
            'Group: 29', 'Publisher: 5127', 'Title: 742', 'Check digit: 3'
        ])
        self.assertEqual(isbn.format(), '2-951-27742-3')
        self.assertEqual(isbn.to_isbn_13(), '978-2-95-127742-7')
        self.assertEqual(isbn.to_ean_13(), '9782951277427')
        a = 0


if __name__ == '__main__':
    unittest.main()
