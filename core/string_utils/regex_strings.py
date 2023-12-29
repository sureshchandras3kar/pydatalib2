from enum import Enum
from re import Pattern
from re import compile
from typing import Dict

from .error_handlings import PatternTypeNotFoundError


class PatternType(Enum):
    IPV4: str = "ipv4"
    IPV6 = "ipv6"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    URL = "url"
    ESCAPE_CHARACTER = "escape_character"


class RePatterns:
    IPV4_PATTERN: Pattern[
        str] = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    IPV6_PATTERN: Pattern[
        str] = r'^[a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){7}$'  # Regular expression to match an IPv6 address
    EMAIL_PATTERN: Pattern[
        str] = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Regular expression to match an email address
    PHONE_NUMBER_PATTERN: Pattern[str] = r'^\+?[1-9]\d{1,14}$'
    URL_PATTERN: Pattern[str] = r'^(https?|ftp)://[^\s/$.?#][a-zA-Z0-9_-]*(\.[a-zA-Z0-9_-]+)+(/[^\s]*)?$'
    ESCAPE_SEARCH_PATTERN: Pattern[str] = r'(?!"[^"]*)@+(?=[^"]*")|\\@'

    def __init__(self):
        self.PATTERN_MAPPING: Dict[PatternType, Pattern] = {
            PatternType.EMAIL: compile(self.EMAIL_PATTERN),
            PatternType.ESCAPE_CHARACTER: compile(self.ESCAPE_SEARCH_PATTERN),
            PatternType.IPV4: compile(self.IPV4_PATTERN),
            PatternType.PHONE_NUMBER: compile(self.PHONE_NUMBER_PATTERN),
            PatternType.URL: compile(self.URL_PATTERN)
        }

    @property
    def pattern(self) -> Dict[PatternType, Pattern]:
        return self.PATTERN_MAPPING

    def get_pattern(self, pattern_type: PatternType) -> Pattern:
        pattern = self.pattern.get(pattern_type)
        if pattern is None:
            raise PatternTypeNotFoundError(f"Pattern type '{pattern_type}' not found.")
        return pattern
