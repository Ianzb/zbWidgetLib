from qtpy.QtGui import QIntValidator, QValidator


class StrictIntValidator(QIntValidator):
    """Strict integer validator that blocks out-of-range input at keystroke level.

    Unlike QIntValidator, which tolerates typing values outside the range
    (returning QValidator.Intermediate for any valid integer regardless of
    range), this validator returns QValidator.Invalid for values exceeding
    the configured bounds, preventing the characters from appearing in the
    field at all.

    Example:
        lineEdit.setValidator(StrictIntValidator(0, 100))
        # Typing "1" "0" "1" → "101" is rejected at the third keystroke,
        # the field stays at "10".
    """

    _allowed_chars = frozenset("0123456789")

    def validate(self, input_str: str, pos: int):
        """Validate input at the given cursor position.

        :param input_str: The current input string (after the proposed edit)
        :param pos: Cursor position
        :return: (state, input_str, pos) tuple
        """
        # Allow empty string so the user can clear the field
        if not input_str:
            return (QValidator.Intermediate, input_str, pos)

        # Handle lone minus sign: only valid if the range includes negatives
        if input_str == '-':
            return (QValidator.Intermediate if self.bottom() < 0
                    else QValidator.Invalid, input_str, pos)

        # Character-level fast rejection (JoinMarket pattern)
        # Avoids int() ValueError for clearly invalid inputs like "abc", "12cm"
        has_leading_minus = self.bottom() < 0 and input_str.startswith('-')
        body = input_str[1:] if has_leading_minus else input_str
        if not body or not set(body).issubset(self._allowed_chars):
            return (QValidator.Invalid, input_str, pos)

        try:
            value = int(input_str)
        except ValueError:
            return (QValidator.Invalid, input_str, pos)

        if self.bottom() <= value <= self.top():
            return (QValidator.Acceptable, input_str, pos)
        return (QValidator.Invalid, input_str, pos)

    def fixup(self, input_str: str) -> str:
        """Clamp a committed value to the valid range (safety fallback)."""
        try:
            value = int(input_str)
            return str(max(self.bottom(), min(self.top(), value)))
        except ValueError:
            return str(self.bottom())
