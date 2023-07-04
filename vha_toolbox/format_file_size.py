import math


def format_file_size(size: int, decimal_places: int = 1) -> str:
    """
    Format the file size in a human-readable format.

    Args:
        size (int): The size of the file in bytes.
        decimal_places (int, optional): The number of decimal places to round the result to. Defaults to 1.

    Returns:
        str: The formatted file size.

    Example:
        >>> format_file_size(123456789)
        '117.7 MB'

    Raises:
        ValueError: If the size is negative.
    """
    if size < 0:
        raise ValueError("Size cannot be negative.")

    if size == 0:
        return f"0.0 {'B'}"

    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB']
    magnitude = int(math.floor(math.log(size, 1024)))

    # Handle extremely large file sizes
    if magnitude >= len(suffixes):
        magnitude = len(suffixes) - 1

    size /= math.pow(1024, magnitude)
    formatted_size = f"{size:.{decimal_places}f}"

    return f"{formatted_size} {suffixes[magnitude]}"
