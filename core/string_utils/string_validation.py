from typing import List
from typing import Union
from typing import Iterable

from regex_strings import PatternType
from regex_strings import RePatterns

re_patterns = RePatterns()


def concat(strings: Iterable[str]) -> str:
    """
    Concatenate a list of strings into a single string.

    :param strings: A list of strings to be concatenated.
    :return: A single string composed of the concatenated input strings.
    """
    if not isinstance(strings, Iterable):
        raise TypeError("Input must be an iterable.")
    strings = map(str, strings)
    return ''.join(strings)


def contains(string: str, matches: Union[str, List[str]]) -> bool:
    """
    Check if a string contains any of the given values. `matches` may be a single string or a list of strings.

    :param string: The string to check for matches.
    :param matches: A single string or a list of strings to check within the input string.
    :return: True if any of the matches are found in the string, False otherwise.
    """
    matches = [matches] if isinstance(matches, str) else matches
    string = string.lower()
    matches = list(filter(None, matches))
    return any(m in string for m in matches)


def contain_all(string: str, matches: Iterable[str]) -> bool:
    """
    Determine if a string contains all the given values.

    :param string: The string to check for matches.
    :param matches: An iterable of strings to check within the input string.
    :return: True if all the matches are found in the string, False otherwise.

    Example:
    >>> contain_all("hello world",["hello", "world"])
    True

    >>> contain_all("hello world",["hello", "goodbye"])
    False
    """
    if not isinstance(string, str):
        raise TypeError("string parameter must be of type str")
    if not isinstance(matches, Iterable):
        raise TypeError("matches parameter must be iterable")
    if not matches:
        return True
    return all(match in string for match in matches)


def count_vowels(input_string: str) -> int:
    """
    Count the number of vowels in a string.

    This function counts the number of vowels (a, e, i, o, u) in the input string.

    :param input_string: count vowels from input string to.

    :return: The count of vowels in the string.
    """
    vowels: set = set("aeiouAEIOU")
    if not input_string:
        return 0
    return sum(char in vowels for char in input_string)


def count_consonants(input_string: str) -> int:
    """
    Count the number of consonants in the input_string
    :param input_string: count consonants from input string.

    :return:  count of consonants in the string
    """
    # noinspection SpellCheckingInspection
    consonants: str = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    count = 0
    for char in input_string:
        if char in consonants:
            count += 1
    return count


def convert_string_to_bool(input_string: str) -> bool:
    """
    Convert a string to boolean

    This function takes a string as input and returns a boolean value based on the string.
    The string is converted to lowercase and checked against a set of accepted values:
    "true", "yes", "y", "1". If the string matches any of these values, the function returns True.
    Otherwise, it returns False.

    :param input_string: string to convert to boolean
    :return: return boolean value
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    if input_string is None:
        return False
    return input_string.strip().lower() in {"true", "yes", "y", "1"}


def is_valid_string(obj: str) -> bool:
    """
    Check if object is a valid string

    :param obj: object to check
    :return: boolean value true or false
    """
    return isinstance(obj, str) and obj.strip() != ''


def is_valid_ipv4_address(obj: str) -> bool:
    """
    Check if object is a valid IPv4 address IPv4 string

    :param obj: object to check
    :return: boolean value true or false
    """
    if not is_valid_string(obj):
        return False

    pattern = re_patterns.get_pattern(PatternType.IPV4)
    if pattern.fullmatch(obj) is None:
        return False

    return all(0 <= int(token) <= 255 for token in obj.split('.'))


def is_valid_ipv6_address(obj: str) -> bool:
    """
    Check if object is a valid IPv6
    :param obj: object to check
    :return: boolean value true or false
    """

    if not is_valid_string(obj):
        return False

    pattern = re_patterns.get_pattern(PatternType.IPV6)
    if pattern.fullmatch(obj) is None:
        return False

    return True  # Address matches the IPv6 pattern


def is_valid_ip_address(obj: str) -> bool:
    """
    Check if object is a valid IP address
    :param obj: object to check against the IP address

    :return:  boolean value true or false
    """
    
    return is_valid_ipv4_address(obj) or is_valid_ipv6_address(obj)


def is_valid_url(obj: str) -> bool:
    """
    Check if object is a valid URL
    :param obj: object to check
    :return:  boolean value true or false
    """

    pattern = re_patterns.get_pattern(PatternType.URL)
    if pattern.fullmatch(obj) is None:
        return False

    return True


def is_email_address(obj: str) -> bool:
    """
    Check if object is a valid email address
    :param obj: object to check against the email address

    :return:  boolean value true or false
    """
    email_pattern = re_patterns.get_pattern(PatternType.EMAIL)

    if not is_valid_string(obj) or len(obj) > 320 or obj.startswith('.'):
        return False

    try:
        # we expect 2 tokens, one before "@" and one after, otherwise we have an exception and the email is not valid
        head, tail = obj.split('@')

        # head's size must be <= 64, tail <= 255, head must not start with a dot or contain multiple consecutive dots
        if len(head) > 64 or len(tail) > 255 or head.endswith('.') or ('..' in head):
            return False

        # removes escaped spaces, so that later on the test regex will accept the string
        head = head.replace('\\ ', '')
        if head.startswith('"') and head.endswith('"'):
            head = head.replace(' ', '')[1:-1]

        return email_pattern.match(head + '@' + tail) is not None

    except ValueError:
        escape_pattern = re_patterns.get_pattern(PatternType.ESCAPE_CHARACTER)
        # borderline case in which we have multiple "@" signs but the head part is correctly escaped
        if escape_pattern.search(obj) is not None:
            # replace "@" with "a" in the head
            return is_email_address(escape_pattern.sub('a', obj))

        return False


def is_strong_password(password: str) -> bool:
    """
    Check if the password is strong
    :param password: Password to check
    :return: Boolean value, True if the password is strong, False otherwise
    """

    # pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    # return bool(pattern.fullmatch(password))

    pattern = re_patterns.get_pattern(PatternType.PASSWORD)
    return bool(pattern.fullmatch(password))


def is_valid_date_regex(date_str: str) -> bool:
    """
    Check if the string represents a valid date in the "YYYY-MM-DD" format using regex
    :param date_str: String representing a date
    :return: Boolean value, True if the date is valid, False otherwise
    """

    date_regex = re_patterns.get_pattern(PatternType.DATE_TIME)
    return bool(date_regex.match(date_str))
