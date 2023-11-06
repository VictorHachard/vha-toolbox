from typing import List


def generate_table(rows: List[List[str]], header: List[str] = None) -> str:
    """
    Convert a list of rows to an HTML table with a header row.

    Args:
        rows (list of lists): The rows of data for the table.
        header (list): The header row for the table.

    Returns:
        str: The HTML representation of the table.

    Example:
        >>> generate_table([['a', 'b'], ['c', 'd']])
        '<table><tr><th>a</th><th>b</th></tr><tr><td>c</td><td>d</td></tr></table>'
    """
    if header is None:
        header = []

    table = '<table>'

    if header:
        table += '<tr>'
        for column in header:
            table += f'<th>{column}</th>'
        table += '</tr>'

    for row in rows:
        table += '<tr>'
        for column in row:
            table += f'<td>{column}</td>'
        table += '</tr>'

    table += '</table>'
    return table
