
class EAN:
    """
    A class used to represent an EAN-13.
    """
    def __init__(self, ean):
        """
        Args:
            ean (str): The EAN-13 to validate and format.

        Examples:
            >>> EAN('9783161484100')
            EAN(9783161484100)
            >>> EAN('978-3-16-148410-0')
            EAN(9783161484100)

        Raises:
            ValueError: If the EAN-13 is invalid (either format is incorrect or check digit is incorrect).
        """
        self.ean = self._sanitize_and_normalize_ean(ean)
        is_valid = self.is_valid()
        if not is_valid:
            raise ValueError("Invalid EAN, check digit is incorrect")

    def _sanitize_and_normalize_ean(self, ean):
        # Sanitize and normalize the provided EAN-13
        ean = ean.replace("-", "").replace(" ", "").lower()
        normalize = ''.join(char for char in ean if char.isdigit())
        if len(normalize) == 13:
            return normalize
        else:
            raise ValueError("Invalid EAN, format is incorrect")

    def break_down_ean(self) -> list[str]:
        """
        Breaks down an EAN-13 into its parts.

        Returns:
            list[str]: A list of strings containing the EAN-13 parts.
        """
        parts = [
            "Prefix: " + self.ean[:3],
            "Manufacturer/Product: " + self.ean[3:12],
            "Check digit: " + self.ean[12]
        ]

        return parts

    def is_valid(self) -> bool:
        """
        Validates an EAN-13 by checking if the check digit is correct.

        Returns:
            bool: True if the EAN-13 is valid, False otherwise.

        Examples:
            >>> EAN('9783161484100').is_valid()
            True
            >>> EAN('9783161484105').is_valid()
            False
        """
        check_digit = sum(int(self.ean[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
        check_digit = (10 - (check_digit % 10)) % 10
        return check_digit == int(self.ean[-1])

    def format(self) -> str:
        """
        Formats an EAN-13 by adding dashes.

        Returns:
            str: The formatted EAN-13.
        """
        return self.ean

    def __str__(self):
        return self.format()

    def __repr__(self):
        return f"EAN({self.format()})"
