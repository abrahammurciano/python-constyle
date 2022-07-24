import itertools
from typing import Optional, Tuple, Union


class Style:
    """A collection of attributes defining the style of a string.

    You can call `Style` objects to apply the style to a string.
    ```py
    >>> warning = Style(Attributes.BOLD, Attributes.YELLOW, Attributes.ITALIC)
    >>> print(warning("This is a warning!"))
    ```

    You can add `Style` objects together to create a `Style` with all their attributes combined.
    ```py
    >>> warning = Style(Attributes.YELLOW, Attributes.ITALIC)
    >>> error = warning + Attributes.BOLD + Attributes.ON_RED
    >>> print(error("This is an error!"))
    ```

    You can also convert a `Style` object to a string to get the ANSI escape sequence for the style.
    ```py
    >>> print(f"{Attributes.YELLOW + Attributes.ITALIC + Attributes.BOLD}This is a warning!{Attributes.RESET}")
    ```

    Args:
        *attrs: The attributes to apply. Can be a mix of `Style` objects or `int`s.
        end: The style to apply after each styled string. If None (the default) it will reset all attributes.
    """

    def __init__(
        self, *attrs: "Union[Style, int]", end: "Optional[Style]" = None
    ) -> None:
        self._params: Tuple[int, ...] = tuple(
            itertools.chain.from_iterable(
                attr._params if isinstance(attr, Style) else (attr,) for attr in attrs
            )
        )
        self._prefix = f"\033[{';'.join(str(p) for p in self._params)}m"
        self._end = end

    def __call__(self, string: str) -> str:
        """Apply this style to the given string.

        Args:
            string: The string to apply the style to.
        """
        return f"{self}{string}{self._end or Style()}" if string else string

    def __add__(self, other: "Style") -> "Style":
        """Add the attributes of the left and right `Style` operands, returning a new `Style`.

        NOTE: The returned `Style` will have the default `end` style and not the `end` style of the left or right operands.

        Returns:
            Style: A new `Style` object containing the attributes of the first operand and the second operand.
        """
        return Style(*self._params, *other._params)

    def __str__(self) -> str:
        """Return the ANSI escape sequence for this style."""
        return self._prefix

    def __repr__(self) -> str:
        return f"{type(self).__name__}({', '.join(str(p) for p in self._params)})"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, Style)
            and self._params == __o._params
            and self._end == __o._end
        )


def style(string: str, *attrs: "Style", end: "Optional[Style]" = None) -> str:
    """Apply the given attributes to the given string.

    Args:
        string: The string to style.
        *attrs: The attributes/styles to apply.
        end: The style to apply after the string. If None (the default) it will reset all attributes at the end.
    """
    return Style(*attrs, end=end)(string)
