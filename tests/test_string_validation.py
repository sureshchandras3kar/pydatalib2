import unittest
from pydatalib2 import string_utils


class TestValidDateFormat(unittest.TestCase):
    def test_date_format(self):
        self.assertEqual(string_utils.is_valid_datetime_format("06-01-2024"), False)


if __name__ == '__main__':
    unittest.main()
