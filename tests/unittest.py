import unittest
from src.PyDataLib2.string_utils.string_validation import is_valid_date_regex


class TestValidDateFormat(unittest.TestCase):
    def test_date_format(self):
        self.assertEqual(is_valid_date_regex("06-01-2024"), False)


unittest.main()
