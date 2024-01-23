import pytest
from pydatalib2 import string_utils


# noinspection SpellCheckingInspection
@pytest.mark.parametrize(
    "test_name, input_data, expected_output, silence_typeerror",
    [
        ("concatenates_list_of_strings", ["hello", "world"], "helloworld", True),
        ("returns_empty_string_with_empty_list", [], "", True),
        ("returns_input_string_with_single_string", ["hello"], "hello", True),
        ("returns_concatenated_string_with_multiple_strings", ["hello", "world"], "helloworld", True),
        ("handles_input_with_special_characters_and_spaces", ["hello!", "world"], "hello!world", True),
        ("handles_input_with_non_ascii_characters", ["héllö", "wörld"], "héllöwörld", True),
        ("raises_type_error_with_non_iterable_input", 123, TypeError, False),
        ("raises_type_error_with_non_string_elements", ["hello", 123], TypeError, False),
        ("returns_concatenated_string_with_non_string_elements", ["hello", 123], "hello123", True),
        (
            "handles_input_with_leading_and_trailing_special_characters",
            ["!hello!", "!world!"],
            "!hello!!world!",
            True,
        ),
        (
            "handles_non_ascii_characters",
            ["¡Hola!", "こんにちは", "안녕하세요"],
            "¡Hola!こんにちは안녕하세요",
            True,
        ),
        ("treats_input_string_as_iterable_of_characters", "hello", "hello", True),
        ("handles_empty_input_iterable", ["", "", ""], "", True),
        ("handles_whitespace_input_iterable", [" ", " ", " "], "   ", True),
        ("handles_input_with_leading_and_trailing_whitespace", [" hello ", " world "], " hello  world ", True),
        (
            "handles_input_with_leading_and_trailing_special_characters",
            ["!hello!", "!world!"],
            "!hello!!world!",
            True,
        ),
        (
            "handles_input_with_leading_and_trailing_digits",
            ["123abc", "456def", "789ghi"],
            "123abc456def789ghi",
            True,
        ),
        (
            "handles_input_with_leading_and_trailing_punctuation_marks",
            ["!abc!", "?def?", ".ghi."],
            "!abc!?def?.ghi.",
            True,
        ),
    ],
)
def test_concat(test_name, input_data, expected_output, silence_typeerror):
    if expected_output == TypeError:
        with pytest.raises(TypeError):
            string_utils.concat(input_data, silence_typeerror)
    else:
        result = string_utils.concat(input_data, silence_typeerror)
        assert result == expected_output, f"Test '{test_name}' failed. Expected '{expected_output}', got '{result}'."


@pytest.mark.parametrize(
    "test_name, string, matches, expected_output",
    [
        ("all_substrings_present", "hello world", ["hello", "world"], True),
        ("some_substrings_missing", "hello world", ["hello", "goodbye"], False),
        ("no_substrings_present", "hello world", ["goodbye", "bye"], False),
        ("empty_string_and_empty_matches", "", [], True),
        ("duplicates_of_some_matches", "hello hello world", ["hello", "world"], True),
        ("matches_with_different_cases", "Hello World", ["hello", "world"], False),
        ("matches_not_strings", "hello world", [1, 2, 3], TypeError),
        ("matches_with_empty_strings", "hello world", ["", "hello"], False),
        ("matches_with_none", "hello world", [None, "hello"], False),
        ("matches_not_hashable", "hello world", [[1], [2], [3]], TypeError),
    ],
)
def test_contain_all(test_name, string, matches, expected_output):
    if expected_output == TypeError:
        with pytest.raises(TypeError):
            string_utils.contain_all(string, matches)
    else:
        result = string_utils.contain_all(string, matches)
        assert result == expected_output, f"Test '{test_name}' failed. Expected '{expected_output}', got '{result}'."
