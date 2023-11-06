import unittest

from vha_toolbox import generate_table


class TableGeneratorTestCase(unittest.TestCase):
    def test_generate_table(self):
        rows = [['Alice', 28, 'USA'], ['Bob', 35, 'Canada']]
        header = ['Name', 'Age', 'Country']
        expected_html_table = '<table><tr><th>Name</th><th>Age</th><th>Country</th></tr><tr><td>Alice</td><td>28</td><td>USA</td></tr><tr><td>Bob</td><td>35</td><td>Canada</td></tr></table>'

        generated_html_table = generate_table(rows, header)
        self.assertEqual(generated_html_table, expected_html_table)

    def test_generate_table_no_header(self):
        rows = [['Alice', 28, 'USA'], ['Bob', 35, 'Canada']]
        expected_html_table = '<table><tr><td>Alice</td><td>28</td><td>USA</td></tr><tr><td>Bob</td><td>35</td><td>Canada</td></tr></table>'

        generated_html_table = generate_table(rows)
        self.assertEqual(generated_html_table, expected_html_table)

    def test_generate_table_no_rows(self):
        rows = []
        header = ['Name', 'Age', 'Country']
        expected_html_table = '<table><tr><th>Name</th><th>Age</th><th>Country</th></tr></table>'

        generated_html_table = generate_table(rows, header)
        self.assertEqual(generated_html_table, expected_html_table)

    def test_generate_table_no_rows_no_header(self):
        rows = []
        expected_html_table = '<table></table>'

        generated_html_table = generate_table(rows)
        self.assertEqual(generated_html_table, expected_html_table)

    def test_generate_table_with_incomplete_rows(self):
        rows = [['Alice', 28], ['Bob', 35, 'Canada']]
        header = ['Name', 'Age', 'Country']
        expected_html_table = '<table><tr><th>Name</th><th>Age</th><th>Country</th></tr><tr><td>Alice</td><td>28</td></tr><tr><td>Bob</td><td>35</td><td>Canada</td></tr></table>'

        generated_html_table = generate_table(rows, header)
        self.assertEqual(generated_html_table, expected_html_table)


if __name__ == '__main__':
    unittest.main()
