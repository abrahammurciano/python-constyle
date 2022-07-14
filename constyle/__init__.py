"""
.. include:: ../README.md
"""


from enum import Enum
from typing import Any
import importlib_metadata

try:
    __version__ = importlib_metadata.version(__package__ or __name__)
except importlib_metadata.PackageNotFoundError:
    import toml

    __version__ = (
        toml.load("pyproject.toml")
        .get("tool", {})
        .get("poetry", {})
        .get("version", "unknown")
        + "-dev"
    )


class Attribute:
    """These are the ANSI escape codes used to set the style of text.

    Otherwise known as SGR (Select Graphic Rendition) parameters. More on that [here](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters).

    Args:
        params: A string (or something that can be converted to a string) that contains the ANSI escape code. Typically this is a number, but for example for RGB colours it can be something like `"38;2;255;0;0"`.
    """

    def __init__(self, params: Any):
        self.params = params

    @property
    def ansi(self) -> str:
        """The ANSI escape code for this attribute."""
        return f"\033[{self.params}m"


class Attributes(Attribute, Enum):
    """
    This enum contains almost all ANSI escape codes known to man.

    Due to inconsistencies across implementations you may find that there are sometimes conflicting attributes with the same param.

    There are also several common aliases for the same attribute (such as RESET and NORMAL).
    """

    RESET = 0
    NORMAL = 0

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    ON_BLACK = 40
    ON_RED = 41
    ON_GREEN = 42
    ON_YELLOW = 43
    ON_BLUE = 44
    ON_MAGENTA = 45
    ON_CYAN = 46
    ON_WHITE = 47

    GREY = 90
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97

    ON_GREY = 100
    ON_BRIGHT_BLACK = 100
    ON_BRIGHT_RED = 101
    ON_BRIGHT_GREEN = 102
    ON_BRIGHT_YELLOW = 103
    ON_BRIGHT_BLUE = 104
    ON_BRIGHT_MAGENTA = 105
    ON_BRIGHT_CYAN = 106
    ON_BRIGHT_WHITE = 107

    DEFAULT_FOREGROUND = 39
    DEFAULT_BACKGROUND = 49

    BOLD = 1
    NO_BOLD = 21
    FAINT = 2
    NO_BOLD_FEINT = 22
    DIM = 2
    ITALIC = 3
    NO_ITALIC_BLACKLETTER = 23
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    NO_BLINK = 25
    INVERT = 7
    NO_INVERT = 27
    CONCEAL = 8
    HIDE = 8
    REVEAL = 28
    NO_CONCEAL = 28
    NO_HIDE = 28

    UNDERLINE = 4
    NO_UNDERLINE = 24
    DOUBE_UNDERLINE = 21
    DEFAULT_UNDERLINE_COLOUR = 59
    OVERLINE = 53
    NO_OVERLINE = 55
    CROSSED = 9
    NO_CROSSED = 29
    STRIKE = 9
    NO_STRIKE = 29
    RIGHT_LINE = 60
    RIGHT_DOUBLE_LINE = 61
    LEFT_LINE = 62
    LEFT_DOUBLE_LINE = 63

    IDEOGRAM_UNDERLINE = 60
    IDEOGRAM_DOUBLE_UNDERLINE = 61
    IDEOGRAM_OVERLINE = 62
    IDEOGRAM_DOUBLE_OVERLINE = 63
    IDEOGRAM_STRESS_MARK = 64
    NO_IDEOGRAM = 65

    SUPERSCRIPT = 73
    SUBSCRIPT = 74
    NO_SUPERSCRIPT_SUBSCRIPT = 75

    PRIMARY_FONT = 10
    ALT_FONT_1 = 11
    ALT_FONT_2 = 12
    ALT_FONT_3 = 13
    ALT_FONT_4 = 14
    ALT_FONT_5 = 15
    ALT_FONT_6 = 16
    ALT_FONT_7 = 17
    ALT_FONT_8 = 18
    ALT_FONT_9 = 19
    FRAKTUR = 20
    GOTHIC = 20

    PROPORTIONAL_SPACING = 26
    NO_PROPORTIONAL_SPACING = 50
    FRAMED = 51
    ENCIRCLED = 52
    NO_FRAMED_ENCIRCLED = 54


class Style:
    """This class can be used to style a string.

    Args:
        *attrs: The attributes to apply.
        enable_nesting: If true (the default), when applying attributes to a string all reset sequences in the string will be replaced with the attributes. This should facilitate nesting styles.
    """

    def __init__(self, *attrs: Attribute, enable_nesting: bool = True) -> None:
        self._attrs = attrs
        self._enable_nesting = enable_nesting

    def __call__(self, string: str) -> str:
        """Apply the given attributes to the given string.

        Args:
            string: The string to style.
        """
        if not self._attrs:
            return string  # No need to append the reset attribute if there are no attributes

        prefix = "".join(attr.ansi for attr in self._attrs)
        reset = Attributes.RESET.ansi
        string = string.replace(reset, prefix) if self._enable_nesting else string
        return f"{prefix}{string}{reset}"


def style(string: str, *attrs: Attribute) -> str:
    """Apply the given attributes to the given string.

    Args:
        string: The string to style.
        *attrs: The attributes to apply.
    """
    return Style(*attrs)(string)


class _BaseRGB(Attribute):
    def __init__(self, ansi: int, red: int, green: int, blue: int):
        for name, value in (("red", red), ("green", green), ("blue", blue)):
            if not 0 <= value <= 255:
                raise ValueError(f"{name} value {value} is not between 0 and 255")
        super().__init__(f"{ansi};2;{red};{green};{blue}")


class ForegroundRGB(_BaseRGB):
    """This class allows you to make attributes for custom foreground colours using RGB values.

    Args:
        red: The red value of the colour (0-255).
        green: The green value of the colour (0-255).
        blue: The blue value of the colour (0-255).

    Raises:
        ValueError: If the red, green or blue values are not between 0 and 255.
    """

    def __init__(self, red: int, green: int, blue: int):
        super().__init__(38, red, green, blue)


class BackgroundRGB(_BaseRGB):
    """This class allows you to make attributes for custom background colours using RGB values.

    Args:
        red: The red value of the colour (0-255).
        green: The green value of the colour (0-255).
        blue: The blue value of the colour (0-255).

    Raises:
        ValueError: If the red, green or blue values are not between 0 and 255.
    """

    def __init__(self, red: int, green: int, blue: int):
        super().__init__(48, red, green, blue)


class _Base8Bit(Attribute):
    def __init__(self, ansi: int, value: int):
        if not 0 <= value <= 255:
            raise ValueError(f"8-bit value {value} is not between 0 and 255")
        super().__init__(f"{ansi};5;{value}")


class Foreground8Bit(_Base8Bit):
    """This class allows you to make attributes for custom foreground colours using 8-bit values.

    Args:
        value: The 8-bit value of the colour (0 to 255).

    Raises:
        ValueError: If the 8-bit value is not between 0 and 255.
    """

    def __init__(self, value: int):
        super().__init__(38, value)


class Background8Bit(_Base8Bit):
    """This class allows you to make attributes for custom background colours using 8-bit values.

    Args:
        value: The 8-bit value of the colour (0 to 255).

    Raises:
        ValueError: If the 8-bit value is not between 0 and 255.
    """

    def __init__(self, value: int):
        super().__init__(48, value)
