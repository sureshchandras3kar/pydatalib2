from enum import Enum
from re import Pattern
from re import compile
from typing import Dict

from exceptions import PatternTypeNotFoundError


class PatternType(Enum):
    IPV4: str = "ipv4"
    IPV6 = "ipv6"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    URL = "url"
    ESCAPE_CHARACTER = "escape_character"
    PASSWORD = "password"
    DATE_TIME = "date_time"


class RePatterns:
    IPV4: Pattern[str] = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    IPV6: Pattern[str] = r'^[a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){7}$'
    EMAIL: Pattern[str] = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PHONE_NUMBER: Pattern[str] = r'^\+?[1-9]\d{1,14}$'
    URL: Pattern[str] = r'^(https?|ftp)://[^\s/$.?#][a-zA-Z0-9_-]*(\.[a-zA-Z0-9_-]+)+(/[^\s]*)?$'
    ESCAPE_SEARCH: Pattern[str] = r'(?!"[^"]*)@+(?=[^"]*")|\\@'
    PASSWORD_PATTERN: Pattern[str] = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    DATE_TIME: Pattern[str] = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'

    def __init__(self):
        self.PATTERN_MAPPING: Dict[PatternType, Pattern] = {
            PatternType.EMAIL: compile(self.EMAIL),
            PatternType.ESCAPE_CHARACTER: compile(self.ESCAPE_SEARCH),
            PatternType.IPV4: compile(self.IPV4),
            PatternType.PHONE_NUMBER: compile(self.PHONE_NUMBER),
            PatternType.URL: compile(self.URL),
            PatternType.PASSWORD: compile(self.PASSWORD_PATTERN),
            PatternType.DATE_TIME: compile(self.DATE_TIME)
        }

    @property
    def pattern(self) -> Dict[PatternType, Pattern]:
        return self.PATTERN_MAPPING

    def get_pattern(self, pattern_type: PatternType) -> Pattern:
        pattern = self.pattern.get(pattern_type)
        if pattern is None:
            raise PatternTypeNotFoundError(f"Pattern type '{pattern_type}' not found.")
        return pattern
