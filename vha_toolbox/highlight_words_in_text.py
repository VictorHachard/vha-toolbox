import re
from typing import List


def highlight_words_in_text(
        text: str,
        words: List[str],
        replace_start: str='<span>',
        replace_end: str='</span>',
        case_insensitive: bool=False
) -> str:
    """
    Highlights specified words in a given text by wrapping them with start_tag and end_tag.

    Args:
        text (str): The input text to be processed.
        words (list): A list of words to be highlighted.
        start_tag (str, optional): The starting HTML tag to wrap around the highlighted words. Default is '<span>'.
        end_tag (str, optional): The ending HTML tag to wrap around the highlighted words. Default is '</span>'.
        case_insensitive (bool, optional): If True, performs case-insensitive matching. Default is False.

    Returns:
        str: The text with the specified words highlighted using the provided HTML tags.

    Example:
        text = "Hello world! This is a sample text."
        words = ["hello", "sample"]
        print(highlight_words_in_text(text, words, start_tag='<strong>', end_tag='</strong>', case_insensitive=True))
        # Output: "<strong>Hello</strong> world! This is a <strong>sample</strong> text."
    """
    positions = []
    replaced_text = text

    flags = re.IGNORECASE if case_insensitive else 0

    for word in words:
        pattern = re.compile(re.escape(word), flags)
        matches = pattern.finditer(replaced_text)
        for match in matches:
            start, end = match.start(), match.end()

            # Check if the current match overlaps with any existing positions
            is_overlapping = False
            overlapping_positions = []

            for pos_start, pos_end in positions:
                if start <= pos_end and end >= pos_start:
                    is_overlapping = True
                    overlapping_positions.append((pos_start, pos_end))

            if is_overlapping:
                # Find the smallest start and largest end among the overlapping positions
                min_start = min(start, min([pos_start for pos_start, _ in overlapping_positions]))
                max_end = max(end, max([pos_end for _, pos_end in overlapping_positions]))

                # Remove the overlapping positions from the list
                for pos in overlapping_positions:
                    positions.remove(pos)

                # Add the aggregated position to the list
                positions.append((min_start, max_end))
            else:
                positions.append((start, end))

    # Replace words in reverse order to avoid modifying newly added <span> tags
    positions.sort(key=lambda pos: pos[0], reverse=True)
    for start, end in positions:
        replaced_text = replaced_text[:start] + replace_start + replaced_text[start:end] + replace_end + replaced_text[end:]

    return replaced_text
