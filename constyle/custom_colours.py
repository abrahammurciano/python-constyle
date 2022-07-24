"""
This module contains classes to create foreground and background attributes which apply custom colours.

Custom colours have less support than standard colours, so it's recommended to prefer standard colours if possible.
"""

from ._style import Style


def _check_rgb(red: int, green: int, blue: int):
    for name, value in (("Red", red), ("Green", green), ("Blue", blue)):
        if not 0 <= value <= 255:
            raise ValueError(f"{name} value must be between 0 and 255. Got {value}.")


class RGB(Style):
    """This class allows you to make attributes for custom foreground and background colours using RGB values.

    Args:
        red: The red value of the colour (0-255).
        green: The green value of the colour (0-255).
        blue: The blue value of the colour (0-255).
        background: Whether this is a foreground or background colour. Defaults to foreground.

    Raises:
        ValueError: If the red, green or blue values are not between 0 and 255.
    """

    def __init__(self, red: int, green: int, blue: int, background: bool = False):
        _check_rgb(red, green, blue)
        super().__init__(48 if background else 38, 2, red, green, blue)


class EightBit(Style):
    """This class allows you to make attributes for custom foreground and background colours using an 8-bit value.

    Args:
        value: The 8-bit value of the colour (0 to 255).
                - 0-7: Standard colours.
                - 8-15: Bright colours.
                - 16-231: RGB values from 0 to 5. Calculated as 16 + (36 * red) + (6 * green) + (blue).
                - 232-255: Grays values. 232 is darkest and 255 is lightest.

    Raises:
        ValueError: If the 8-bit value is not between 0 and 255.
    """

    def __init__(self, value: int, background: bool = False):
        if not 0 <= value <= 255:
            raise ValueError(f"8-bit value {value} is not between 0 and 255")
        super().__init__(48 if background else 38, 5, value)


class EightBitRGB(EightBit):
    """This class facilitates the creation of custom 8-bit colours using RGB values.

    The colour won't be exact, but it will be as close as possible for 8-bit colours.
    The closer the RGB values are to a multiple of 256/6, the more accurate the colour will be.

    Args:
        red: The red value of the colour (0-255).
        green: The green value of the colour (0-255).
        blue: The blue value of the colour (0-255).
        background: Whether this is a foreground or background colour. Defaults to foreground.

    Raises:
        ValueError: If the red, green or blue values are not between 0 and 255.
    """

    def __init__(self, red: int, green: int, blue: int, background: bool = False):
        _check_rgb(red, green, blue)
        red, green, blue = ((val * 6) // 256 for val in (red, green, blue))
        super().__init__(16 + (36 * red) + (6 * green) + blue, background)
