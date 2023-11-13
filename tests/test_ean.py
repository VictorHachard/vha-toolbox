import unittest

from vha_toolbox import EAN


class EanTestCase(unittest.TestCase):
    def test_ean_1(self):
        ean = EAN('5449000021199')
        result = ean.break_down_ean()
        self.assertEqual(result, ['Prefix: 544', 'Manufacturer/Product: 900002119', 'Check digit: 9'])
        result = ean.format()
        self.assertEqual(result, '5449000021199')


if __name__ == '__main__':
    unittest.main()
