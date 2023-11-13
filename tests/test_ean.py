import unittest

from vha_toolbox import EAN


class EanTestCase(unittest.TestCase):
    def test_ean_1(self):
        ean = EAN('5449000021199')
        result = ean.break_down_ean()
        self.assertEqual(result, [
            'Prefix: 544', 'Manufacturer/Product: 900002119', 'Check digit: 9'
        ])
        result = ean.format()
        self.assertEqual(result, '5449000021199')

    def test_ean_2(self):
        ean = EAN('9783161484100')
        result = ean.break_down_ean()
        self.assertEqual(result, [
            'Prefix: 978', 'Manufacturer/Product: 316148410', 'Check digit: 0'
        ])
        result = ean.format()
        self.assertEqual(result, '9783161484100')

    def test_invalid_ean(self):
        with self.assertRaises(ValueError):
            EAN('12345678901234')

    def test_equal(self):
        ean = EAN('5449000021199')
        self.assertFalse(ean == EAN('9783161484100'))
        self.assertTrue(ean == EAN('5449000021199'))

    def test_equal_str(self):
        ean = EAN('5449000021199')
        self.assertFalse(ean == '9783161484100')
        self.assertTrue(ean == '5449000021199')


if __name__ == '__main__':
    unittest.main()
