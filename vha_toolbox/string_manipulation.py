
def truncate_with_ellipsis(
        input_string: str,
        max_length: int,
        ellipsis: str = '...',
        del_blank: bool = True,
) -> str:
    """
    Truncates a string with an ellipsis if it exceeds the maximum length.

    Args:
        input_string: The string to truncate.
        max_length: The maximum length of the string.
        ellipsis: The ellipsis to use. Defaults to '...'.
        del_blank: Whether to delete trailing whitespace. Defaults to True.

    Returns:
        The truncated string.

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
