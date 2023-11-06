import unittest
from datetime import date

from vha_toolbox import (
    get_last_day_of_year,
    get_first_day_of_year,
    get_first_day_of_month,
    get_last_day_of_month,
    get_last_day_of_quarter,
    get_first_day_of_quarter
)


class DateUtilsTestCase(unittest.TestCase):
    def test_get_first_day_of_year(self):
        dt = date(2023, 6, 15)
        result = get_first_day_of_year(dt)
        self.assertEqual(result, date(2023, 1, 1))

    def test_get_last_day_of_year(self):
        dt = date(2023, 6, 15)
        result = get_last_day_of_year(dt)
        self.assertEqual(result, date(2023, 12, 31))

    def test_get_first_day_of_quarter(self):
        dt = date(2023, 6, 15)
        result = get_first_day_of_quarter(dt)
        self.assertEqual(result, date(2023, 4, 1))

    def test_get_last_day_of_quarter(self):
        dt = date(2023, 6, 15)
        result = get_last_day_of_quarter(dt)
        self.assertEqual(result, date(2023, 6, 30))

    def test_get_first_day_of_month(self):
        dt = date(2023, 6, 15)
        result = get_first_day_of_month(dt)
        self.assertEqual(result, date(2023, 6, 1))

    def test_get_first_day_of_month_2(self):
        dt = date(2024, 2, 10)
        result = get_first_day_of_month(dt)
        self.assertEqual(result, date(2024, 2, 1))

    def test_get_last_day_of_month(self):
        dt = date(2023, 6, 15)
        result = get_last_day_of_month(dt)
        self.assertEqual(result, date(2023, 6, 30))

    def test_get_last_day_of_month_2(self):
        dt = date(2024, 2, 10)
        result = get_last_day_of_month(dt)
        self.assertEqual(result, date(2024, 2, 29))

    def test_get_last_day_of_month_3(self):
        dt = date(2021, 2, 10)
        result = get_last_day_of_month(dt)
        self.assertEqual(result, date(2021, 2, 28))


if __name__ == '__main__':
    unittest.main()
