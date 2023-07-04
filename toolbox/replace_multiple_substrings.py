import re
from typing import Dict


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
        replacements = {
            'apple': 'orange',
            'banana': 'grape',
            'cherry': 'melon'
        }
        original_string = 'I have an apple, a banana, and a cherry.'
        print(replace_multiple_substrings(original_string, replacements))
        # Output: "I have an orange, a grape, and a melon."
    """
    if not replacements:
        return string
    pattern = re.compile("|".join([re.escape(k) for k in sorted(replacements, key=len, reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: replacements[x.group(0)], string)
