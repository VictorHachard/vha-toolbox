import unittest

from vha_toolbox import find_args


class FindArgsTestCase(unittest.TestCase):
    def test_find_args(self):
        self.assertEqual(
            find_args(
                '--arg value',
                {'arg': {'prefix': '--', 'value': True, 'required': True, 'type': 'str'}}
            ),
            {'arg': 'value'}
        )
        self.assertEqual(
            find_args(
                '--arg',
                {'arg': {'prefix': '--', 'value': False}}
            ),
            {'arg': True}
        )

    def test_find_args_type(self):
        self.assertEqual(
            find_args(
                '--arg 1',
                {'arg': {'prefix': '--', 'value': True, 'required': True, 'type': 'int'}}
            ),
            {'arg': 1}
        )
        self.assertEqual(
            find_args(
                '--arg 1.1',
                {'arg': {'prefix': '--', 'value': True, 'required': True, 'type': 'float'}}
            ),
            {'arg': 1.1}
        )
        self.assertEqual(
            find_args(
                '--arg True',
                {'arg': {'prefix': '--', 'value': True, 'required': True, 'type': 'bool'}}
            ),
            {'arg': True}
        )

    def test_find_args_prefix(self):
        self.assertEqual(
            find_args(
                '-arg value',
                {'arg': {'prefix': '-', 'value': True, 'required': True, 'type': 'str'}}
            ),
            {'arg': 'value'}
        )
        self.assertEqual(
            find_args(
                '-arg',
                {'arg': {'prefix': '-', 'value': False}}
            ),
            {'arg': True}
        )

    def test_find_args_multiple(self):
        self.assertEqual(
            find_args(
                '--arg1 value1 --arg2 value2',
                {
                    'arg1': {'prefix': '--', 'value': True, 'required': True, 'type': 'str'},
                    'arg2': {'prefix': '--', 'value': True, 'required': True, 'type': 'str'},
                }
            ),
            {'arg1': 'value1', 'arg2': 'value2'}
        )

    def test_find_args_multiple_prefix(self):
        self.assertEqual(
            find_args(
                '-arg1 value1 -arg2 value2',
                {
                    'arg1': {'prefix': '-', 'value': True, 'required': True, 'type': 'str'},
                    'arg2': {'prefix': '-', 'value': True, 'required': True, 'type': 'str'},
                }
            ),
            {'arg1': 'value1', 'arg2': 'value2'}
        )
        self.assertEqual(
            find_args(
                '-arg1 value1 -arg2 value2',
                {
                    'arg1': {'prefix': '-', 'value': True, 'required': True, 'type': 'str'},
                    'arg2': {'prefix': '-', 'value': True, 'required': True, 'type': 'str'},
                }
            ),
            {'arg1': 'value1', 'arg2': 'value2'}
        )


if __name__ == '__main__':
    unittest.main()
