from calendar import monthrange
from datetime import date, timedelta


def get_first_day_of_year(dt: date = date.today()) -> date:
    """
    Get the first day of the year for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the first day of the year (default: current date).

    Returns:
        date: The first day of the year as a date object.

    Example:
        >>> get_first_day_of_year(date(2023, 6, 15))
        datetime.date(2023, 1, 1)
    """
    return date(dt.year, 1, 1)


def get_last_day_of_year(dt: date = date.today()) -> date:
    """
    Get the last day of the year for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the last day of the year (default: current date).

    Returns:
        date: The last day of the year as a date object.

    Example:
        >>> get_last_day_of_year(date(2023, 6, 15))
        datetime.date(2023, 12, 31)
    """
    return date(dt.year, 12, monthrange(dt.year, 12)[1])


def get_first_day_of_quarter(dt: date = date.today()) -> date:
    """
    Get the first day of the quarter for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the first day of the quarter (default: current date).

    Returns:
        date: The first day of the quarter as a date object.

    Example:
        >>> get_first_day_of_quarter(date(2023, 6, 15))
        datetime.date(2023, 4, 1)
    """
    return date(dt.year, (dt.month - 1) // 3 * 3 + 1, 1)


def get_last_day_of_quarter(dt: date = date.today()) -> date:
    """
    Get the last day of the quarter for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the last day of the quarter (default: current date).

    Returns:
        date: The last day of the quarter as a date object.

    Example:
        >>> get_last_day_of_quarter(date(2023, 6, 15))
        datetime.date(2023, 6, 30)
    """
    next_qt_yr = dt.year + (1 if dt.month > 9 else 0)
    next_qt_first_mo = (dt.month - 1) // 3 * 3 + 4
    next_qt_first_mo = 1 if next_qt_first_mo == 13 else next_qt_first_mo
    next_qt_first_dy = date(next_qt_yr, next_qt_first_mo, 1)
    return next_qt_first_dy - timedelta(days=1)


def get_first_day_of_month(dt: date = date.today()) -> date:
    """
    Get the first day of the month for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the first day of the month (default: current date).

    Returns:
        date: The first day of the month as a date object.

    Example:
        >>> get_first_day_of_month(date(2023, 6, 15))
        datetime.date(2023, 6, 1)
    """
    return date(dt.year, dt.month, 1)


def get_last_day_of_month(dt: date = date.today()) -> date:
    """
    Get the last day of the month for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the last day of the month (default: current date).

    Returns:
        date: The last day of the month as a date object.

    Example:
        >>> get_last_day_of_month(date(2023, 6, 15))
        datetime.date(2023, 6, 30)
    """
    return date(dt.year, dt.month, monthrange(dt.year, dt.month)[1])
