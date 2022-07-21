"""
.. include:: ../README.md
"""


from enum import Enum
from abc import ABC, abstractmethod
from functools import singledispatch
import re
from typing import Any, Union, Iterator
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


class Stylist(ABC):
    """A common interface for anything which can apply a style to a string, e.g. `Attribute` and `Style`.

    Classes which implement it fulfill the following contract:
    - Calling an intance with a string as the first argument shall return a string differing only in the ANSI codes it contains or does not.
    - Converting an instance to a string will result in a string of pure ANSI codes.
    - `.end` gives something which when converted to a string, is the ANSI codes to reset the style.
    """

    @abstractmethod
    def __call__(self, string: str) -> str:
        """Apply the given attributes to the given string.

        Args:
            string: The string to apply the style to.
        """
        raise NotImplementedError()

    @abstractmethod
    def __str__(self) -> str:
        """The ANSI escape codes to apply the style."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def end(self) -> Any:
        """When converted to a string, these are the ANSI codes to reset the style being applied."""
        raise NotImplementedError()


class Attribute(Stylist):
    """These are the ANSI escape codes used to set the style of text.

    Otherwise known as SGR (Select Graphic Rendition) parameters. More on that [here](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters).

    Attribute objects are callable and will convert their input string into one forammted with this attribute.

    Adding two attributes together will result in a `constyle.Style` object containing both attributes.

    Args:
        params: A string (or something that can be converted to a string) that contains the ANSI escape code parameter. Typically this is a number, but for example for RGB colours it can be something like `"38;2;255;0;0"`.
        end_params: The ANSI escape code parameter to reset this `Attribute`. By default it's 0 (which resets all attributes). If the attribute is of a resetting nature (e.g. `Attributes.DEFAULT_FOREGROUND or Attributes.NO_BOLD), then `end_params` should be `None`.
    """

    def __init__(self, params: Any, end_params: Any = 0):
        self.params = params
        self._end_params = end_params

    @property
    def ansi(self) -> str:
        """The ANSI escape code for this attribute."""
        return f"\033[{self.params}m"

    @property
    def end(self) -> str:
        return Attribute(self._end_params).ansi

    def __str__(self) -> str:
        return self.ansi

    def __call__(self, string: str) -> str:
        return Style(self)(string)

    def __add__(self, other: "Attribute") -> "Style":
        if not isinstance(other, Attribute):
            return NotImplemented
        return Style(self, other)


class Attributes(Attribute, Enum):
    """
    This enum contains almost all ANSI escape codes known to man.

    Due to inconsistencies across implementations you may find that there are sometimes conflicting attributes with the same param.

    There are also several common aliases for the same attribute (such as RESET and NORMAL).
    """

    RESET = 0, None
    """Remove all formatting (same as NORMAL)"""
    NORMAL = 0, None
    """Remove all formatting (same as RESET)"""
    BLACK = 30, 39
    """Black foreground text"""
    RED = 31, 39
    """Red foreground text"""
    GREEN = 32, 39
    """Green foreground text"""
    YELLOW = 33, 39
    """Yellow foreground text"""
    BLUE = 34, 39
    """Blue foreground text"""
    MAGENTA = 35, 39
    """Magenta foreground text"""
    CYAN = 36, 39
    """Cyan foreground text"""
    WHITE = 37, 39
    """White foreground text"""
    ON_BLACK = 40, 49
    """Black background text"""
    ON_RED = 41, 49
    """Red background text"""
    ON_GREEN = 42, 49
    """Green background text"""
    ON_YELLOW = 43, 49
    """Yellow background text"""
    ON_BLUE = 44, 49
    """Blue background text"""
    ON_MAGENTA = 45, 49
    """Magenta background text"""
    ON_CYAN = 46, 49
    """Cyan background text"""
    ON_WHITE = 47, 49
    """White background text"""
    GREY = 90, 39
    """Grey foreground text (same as BRIGHT_BLACK)"""
    BRIGHT_BLACK = 90, 39
    """Grey foreground text"""
    BRIGHT_RED = 91, 39
    """Bright red foreground text"""
    BRIGHT_GREEN = 92, 39
    """Bright green foreground text"""
    BRIGHT_YELLOW = 93, 39
    """Bright yellow foreground text"""
    BRIGHT_BLUE = 94, 39
    """Bright blue foreground text"""
    BRIGHT_MAGENTA = 95, 39
    """Bright magenta foreground text"""
    BRIGHT_CYAN = 96, 39
    """Bright cyan foreground text"""
    BRIGHT_WHITE = 97, 39
    """Bright white foreground text"""
    ON_GREY = 100, 49
    """Grey background text (same as ON_BRIGHT_BLACK)"""
    ON_BRIGHT_BLACK = 100, 49
    """Grey background text"""
    ON_BRIGHT_RED = 101, 49
    """Bright red background text"""
    ON_BRIGHT_GREEN = 102, 49
    """Bright green background text"""
    ON_BRIGHT_YELLOW = 103, 49
    """Bright yellow background text"""
    ON_BRIGHT_BLUE = 104, 49
    """Bright blue background text"""
    ON_BRIGHT_MAGENTA = 105, 49
    """Bright magenta background text"""
    ON_BRIGHT_CYAN = 106, 49
    """Bright cyan background text"""
    ON_BRIGHT_WHITE = 107, 49
    """Bright white background text"""
    DEFAULT_FOREGROUND = 39, None
    """Default foreground text colour"""
    NO_COLOUR = 39, None
    """Default foreground text colour"""
    NO_FOREGROUND = 39, None
    """Default foreground text colour"""
    DEFAULT_BACKGROUND = 49, None
    """Default background text colour"""
    NO_BACKGROUND = 49, None
    """Default background text colour"""
    BOLD = 1, 21
    """Bold text"""
    NO_BOLD = 21, None
    """Not bold text"""
    FAINT = 2, 21
    """Faint text (same as DIM). May be implemented as a lighter colour or as a thinner font."""
    DIM = 2, 21
    """Dim text (same as FAINT). May be implemented as a lighter colour or as a thinner font."""
    NO_BOLD_FEINT = 22, None
    """Neither bold nor faint text"""
    ITALIC = 3, 23
    """Italic text. Not widely supported. Sometimes treated as inverse or blink."""
    NO_ITALIC_BLACKLETTER = 23, None
    """Neither italic nor blackletter text"""
    SLOW_BLINK = 5, 25
    """Sets blinking to less than 150 times per minute. Rarely supported."""
    BLINK = 5, 25
    """Same as SLOW_BLINK"""
    RAPID_BLINK = 6, 25
    """Sets blinking to more than 150 times per minute. Rarely supported."""
    NO_BLINK = 25, None
    """Sets blinking to off."""
    INVERT = 7, 27
    """Swap foreground and background colors; inconsistent emulation"""
    NO_INVERT = 27, None
    """Unset invert"""
    CONCEAL = 8, 28
    """Invisible text (same as HIDE). Not widely supported."""
    HIDE = 8, 28
    """Invisible text (same as CONCEAL). Not widely supported."""
    REVEAL = 28, None
    """Unset conceal/hide (same as NO_CONCEAL and NO_HIDE)"""
    NO_CONCEAL = 28, None
    """Unset conceal/hide (same as REVEAL and NO_HIDE)"""
    NO_HIDE = 28, None
    """Unset conceal/hide (same as REVEAL and NO_CONCEAL)"""
    UNDERLINE = 4, 24
    """Underline text. Style extensions exist for Kitty, VTE, mintty and iTerm2."""
    NO_UNDERLINE = 24, None
    """Unset underline"""
    DOUBE_UNDERLINE = 21, 24
    """Double underline. Rarely supported."""
    DEFAULT_UNDERLINE_COLOUR = 59, None
    """Set the underline colour to the default. Not in standard; implemented in Kitty, VTE, mintty, and iTerm2."""
    OVERLINE = 53, 55
    """Overline text"""
    NO_OVERLINE = 55, None
    """Unset overline"""
    CROSSED = 9, 29
    """Crossed out text (same as STRIKE). Characters legible but marked as if for deletion."""
    NO_CROSSED = 29, None
    """Unset crossed out text (same as NO_STRIKE)"""
    STRIKE = 9, 29
    """Crossed out text (same as CROSSED). Characters legible but marked as if for deletion."""
    NO_STRIKE = 29, None
    """Unset crossed out text (same as NO_CROSSED)"""
    RIGHT_LINE = 60
    """Line on right of text. Rarely supported."""
    RIGHT_DOUBLE_LINE = 61
    """Double line on right of text. Rarely supported."""
    LEFT_LINE = 62
    """Line on left of text. Rarely supported."""
    LEFT_DOUBLE_LINE = 63
    """Double line on left of text. Rarely supported."""
    IDEOGRAM_UNDERLINE = 60, 65
    """Ideogram underline. Rarely supported."""
    IDEOGRAM_DOUBLE_UNDERLINE = 61, 65
    """Ideogram double underline. Rarely supported."""
    IDEOGRAM_OVERLINE = 62, 65
    """Ideogram overline. Rarely supported."""
    IDEOGRAM_DOUBLE_OVERLINE = 63, 65
    """Ideogram double overline. Rarely supported."""
    IDEOGRAM_STRESS_MARK = 64, 65
    """Ideogram stress mark. Rarely supported."""
    NO_IDEOGRAM = 65, None
    """Unset ideogram underline/overline/stress mark."""
    SUPERSCRIPT = 73, 75
    """Superscript text. Implemented in mintty"""
    SUBSCRIPT = 74, 75
    """Subscript text. Implemented in mintty"""
    NO_SUPERSCRIPT_SUBSCRIPT = 75, None
    """Unset superscript/subscript text"""
    PRIMARY_FONT = 10, None
    """Select primary font."""
    ALT_FONT_1 = 11, 10
    """Select alternate font 1. Rarely supported."""
    ALT_FONT_2 = 12, 10
    """Select alternate font 2. Rarely supported."""
    ALT_FONT_3 = 13, 10
    """Select alternate font 3. Rarely supported."""
    ALT_FONT_4 = 14, 10
    """Select alternate font 4. Rarely supported."""
    ALT_FONT_5 = 15, 10
    """Select alternate font 5. Rarely supported."""
    ALT_FONT_6 = 16, 10
    """Select alternate font 6. Rarely supported."""
    ALT_FONT_7 = 17, 10
    """Select alternate font 7. Rarely supported."""
    ALT_FONT_8 = 18, 10
    """Select alternate font 8. Rarely supported."""
    ALT_FONT_9 = 19, 10
    """Select alternate font 9. Rarely supported."""
    FRAKTUR = 20, 10
    """Fraktur font (same as GOTHIC). Rarely supported."""
    GOTHIC = 20, 10
    """Gothic font (same as FRAKTUR). Rarely supported."""
    PROPORTIONAL_SPACING = 26, 50
    """Proportional spacing. Not known to be used on terminals."""
    NO_PROPORTIONAL_SPACING = 50, None
    """Unset proportional spacing"""
    FRAMED = 51, 54
    """Framed text. Implemented as "emoji variation selector" in mintty."""
    ENCIRCLED = 52, 54
    """Encircled text. Implemented as "emoji variation selector" in mintty."""
    NO_FRAMED_ENCIRCLED = 54, None
    """Unset framed/encircled text"""

    def __repr__(self) -> str:
        return self.name


class Style(Stylist):
    """A collection of attributes which can be used to style a string.

    You can add `Style`s together to create a style with all their attributes combined. You can also add a single `Attribute` to a `Style`.

    Args:
        *attrs: The attributes to apply.
    """

    def __init__(self, *attrs: Attribute) -> None:
        self._attrs = tuple(attrs)
        self._prefix = "".join(attr.ansi for attr in self._attrs)

    def __call__(self, string: str) -> str:
        return (
            f"{self._prefix}{string}{Attributes.RESET.ansi}" if self._attrs else string
        ) # TODO: Insert correct suffix

    @property
    def end(self) -> "Style":
        pass # TODO: Implement

    def __add__(self, obj: Union["Style", Attribute]) -> "Style":
        """Add either another `Style` or an `Attribute` to a style, returning the new style.

        Args:
            obj: Either the style whose attributes to add, or a single attribute to add.

        Returns:
            Style: A new style object containing the attributes of the first operand and the second operand.
        """
        if not isinstance(obj, (Style, Attribute)):
            return NotImplemented
        other_attrs = obj._attrs if isinstance(obj, Style) else (obj,)
        return Style(*self._attrs, *other_attrs)

    def __iter__(self) -> Iterator[Attribute]:
        return iter(self._attrs)

    def __str__(self) -> str:
        return self._prefix

    def __repr__(self) -> str:
        return f"Style({', '.join(repr(attr) for attr in self._attrs)})"


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
