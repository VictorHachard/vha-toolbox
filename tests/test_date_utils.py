import unittest
from datetime import date

from vha_toolbox import (
    get_last_day_of_year,
    get_first_day_of_year,
    get_first_day_of_month,
    get_last_day_of_month,
    get_last_day_of_quarter,
    get_first_day_of_quarter,
    is_renewal_due
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

    # Existing tests
    def test_is_renewal_due_same_day(self):
        self.assertFalse(is_renewal_due(date(2023, 6, 15), date(2023, 6, 15)))

    def test_is_renewal_due_next_day(self):
        self.assertFalse(is_renewal_due(date(2023, 6, 15), date(2023, 6, 16)))

    def test_is_renewal_due_next_month(self):
        self.assertTrue(is_renewal_due(date(2023, 6, 15), date(2023, 7, 15)))

    def test_is_renewal_due_next_year(self):
        self.assertTrue(is_renewal_due(date(2023, 6, 15), date(2024, 7, 15)))

    def test_leap_year_feb_29(self):
        self.assertTrue(is_renewal_due(date(2020, 2, 29), date(2021, 2, 28)))
        self.assertFalse(is_renewal_due(date(2020, 2, 29), date(2021, 3, 1)))

    def test_non_leap_year_feb_28(self):
        self.assertFalse(is_renewal_due(date(2023, 2, 28), date(2024, 2, 27)))
        self.assertTrue(is_renewal_due(date(2023, 2, 28), date(2024, 2, 28)))

    def test_30_day_month_to_31_day_month(self):
        self.assertTrue(is_renewal_due(date(2023, 4, 30), date(2024, 4, 30)))
        self.assertFalse(is_renewal_due(date(2023, 4, 30), date(2024, 5, 1)))

    def test_31_day_month_to_30_day_month(self):
        self.assertFalse(is_renewal_due(date(2023, 5, 31), date(2024, 5, 30)))
        self.assertTrue(is_renewal_due(date(2023, 5, 31), date(2024, 5, 31)))

    def test_past_date(self):
        self.assertTrue(is_renewal_due(date(2020, 1, 1), date(2024, 1, 1)))

    def test_future_date(self):
        self.assertFalse(is_renewal_due(date(2025, 1, 1), date(2024, 1, 1)))



if __name__ == '__main__':
    unittest.main()
