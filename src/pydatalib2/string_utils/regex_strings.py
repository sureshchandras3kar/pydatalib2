import re
from enum import Enum
from typing import Dict, List, Pattern

from .exceptions import PatternTypeNotFoundError


class PatternType(Enum):
    """Enumeration representing different pattern types.

    :ivar IPV4: Represents the IPV4 pattern.
    :var type IPV4: str
    :ivar IPV6: Represents the IPV6 pattern.
    :var type IPV6: str
    :ivar EMAIL: Represents the EMAIL pattern.
    :var type EMAIL: str
    :ivar PHONE_NUMBER: Represents the PHONE_NUMBER pattern.
    :var type PHONE_NUMBER: str
    :ivar URL: Represents the URL pattern.
    :var type URL: str
    :ivar ESCAPE_CHARACTER: Represents the ESCAPE_CHARACTER pattern.
    :var type ESCAPE_CHARACTER: str
    :ivar PASSWORD: Represents the PASSWORD pattern.
    :var type PASSWORD: str
    :ivar DATE_TIME: Represents the DATE_TIME pattern.
    :var type DATE_TIME: str
    """

    IPV4: str = "ipv4"
    IPV6: str = "ipv6"
    EMAIL: str = "email"
    PHONE_NUMBER: str = "phone_number"
    URL: str = "url"
    ESCAPE_CHARACTER: str = "escape_character"
    PASSWORD: str = "password"
    DATE_TIME: str = "date_time"


class RePatterns:
    """Collection of compiled regular expression patterns.

    This class contains precompiled regular expression patterns for various types of data validation.

    :ivar IPV4: Represents the IPV4 pattern.
    :type IPV4: str

    :ivar IPV6: Represents the IPV6 pattern.
    :type IPV6: str

    :ivar EMAIL: Represents the EMAIL pattern.
    :type EMAIL: str

    :ivar PHONE_NUMBER: Represents the PHONE_NUMBER pattern.
    :type PHONE_NUMBER: str

    :ivar URL: Represents the URL pattern.
    :type URL: str

    :ivar ESCAPE_SEARCH: Represents the ESCAPE_SEARCH pattern.
    :type ESCAPE_SEARCH: str

    :ivar PASSWORD_PATTERN: Represents the PASSWORD_PATTERN pattern.
    :type PASSWORD_PATTERN: str

    :ivar DATE_TIME: Represents the DATE_TIME pattern.
    :type DATE_TIME: str
    """

    IPV4: str = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    IPV6: str = r"^[a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){7}$"
    EMAIL: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    PHONE_NUMBER: str = r"^\+?[1-9]\d{1,14}$"
    URL: str = r"^(https?|ftp)://[^\s/$.?#][a-zA-Z0-9_-]*(\.[a-zA-Z0-9_-]+)+(/[^\s]*)?$"
    ESCAPE_SEARCH: str = r'(?!"[^"]*)@+(?=[^"]*")|\\@'
    PASSWORD_PATTERN: str = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    DATE_TIME: str = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

    def __init__(self):
        self.PATTERN_MAPPING: Dict[PatternType, Pattern] = {
            PatternType.EMAIL: re.compile(self.EMAIL),
            PatternType.ESCAPE_CHARACTER: re.compile(self.ESCAPE_SEARCH),
            PatternType.IPV4: re.compile(self.IPV4),
            PatternType.PHONE_NUMBER: re.compile(self.PHONE_NUMBER),
            PatternType.URL: re.compile(self.URL),
            PatternType.PASSWORD: re.compile(self.PASSWORD_PATTERN),
            PatternType.DATE_TIME: re.compile(self.DATE_TIME),
        }

    @property
    def patterns(self) -> Dict[PatternType, Pattern]:
        """Get all compiled patterns.

        :return: A dictionary containing all compiled patterns.
        """
        return self.PATTERN_MAPPING

    def get_pattern(self, pattern_type: PatternType) -> Pattern:
        """Get a specific compiled pattern by type.

        :param pattern_type: The type of pattern to retrieve.
        :return: The compiled pattern.
        :raises PatternTypeNotFoundError: If the pattern type is not found.
        """
        pattern = self.patterns.get(pattern_type)
        if pattern is None:
            raise PatternTypeNotFoundError(f"Pattern type '{pattern_type}' not found.")
        return pattern


class RegexUtils:
    """A utility class providing various regular expression operations."""

    @staticmethod
    def is_match(pattern: str, text: str) -> bool:
        """Check if there is any match of a pattern in the given text.

        :param pattern: The regular expression pattern to search for.
        :param text: The input text in which to check for a match.
        :return: True if there is a match, False otherwise.
        """
        return bool(re.search(pattern, text))

    @staticmethod
    def replace_matches(pattern: str, replacement: str, text: str) -> str:
        """Replace all matches of a pattern with a specified replacement in the given text.

        :param pattern: The regular expression pattern to search for.
        :param replacement: The string to replace each match with.
        :param text: The input text in which to perform replacements.
        :return: The text after replacing all matches with the specified replacement.
        """
        return re.sub(pattern, replacement, text)

    @staticmethod
    def split_by_pattern(pattern: str, text: str) -> List[str]:
        """Split the text using the specified pattern.

        :param pattern: The regular expression pattern to use for splitting.
        :param text: The input text to split.
        :return: A list of substrings obtained by splitting the text using the pattern.
        """
        return re.split(pattern, text)
