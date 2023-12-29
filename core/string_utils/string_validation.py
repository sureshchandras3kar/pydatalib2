from .regex_strings import RePatterns
from .regex_strings import PatternType


re_patterns = RePatterns()


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
