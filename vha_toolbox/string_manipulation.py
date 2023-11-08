from typing import Dict
import re


def truncate_with_ellipsis(
        input_string: str,
        max_length: int,
        ellipsis: str = '...',
        del_blank: bool = True,
) -> str:
    """
    Truncates a string with an ellipsis if it exceeds the maximum length.

    Args:
        input_string (str): The string to truncate.
        max_length (int): The maximum length of the string.
        ellipsis (str, optional): The ellipsis to use. Defaults to '...'.
        del_blank (bool, optional): Whether to delete trailing whitespace. Defaults to True.

    Returns:
        str: The truncated string.

    Examples:
        >>> truncate_with_ellipsis('Hello world!', 5)
        'Hello...'
        >>> truncate_with_ellipsis('Hello world! ', 6)
        'Hello...' # trailing whitespace is deleted by default (instead of 'Hello ...')
    """
    if len(input_string) <= max_length:
        return input_string
    else:
        input_string = input_string[:max_length]
        if del_blank:
            input_string = input_string.rstrip()
        return input_string + ellipsis


def replace_multiple_substrings(
        string: str,
        replacements: Dict[str, str]
) -> str:
    """
    Replaces multiple substrings in a string based on a dictionary of replacements.

    Args:
        string (str): The original string to perform replacements on.
        replacements (dict): A dictionary where keys are substrings to be replaced and values are their replacements.

    Returns:
        str: The modified string with all replacements applied.

    Example:
        >>> replacements = {
            'apple': 'orange',
            'banana': 'grape',
            'cherry': 'melon'
        }
        >>>  original_string = 'I have an apple, a banana, and a cherry.'
        >>> replace_multiple_substrings(original_string, replacements)
        'I have an orange, a grape, and a melon.'
    """
    if not replacements:
        return string
    pattern = re.compile("|".join([re.escape(k) for k in sorted(replacements, key=len, reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: replacements[x.group(0)], string)
