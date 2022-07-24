from enum import Enum
from ._style import Style


class Attributes(Style, Enum):
    """
    This enum contains almost all ANSI sequences known to man.

    Due to inconsistencies across implementations you may find that there are sometimes conflicting attributes with the same param.

    There are also several common aliases for the same attribute (such as RESET and NORMAL).
    """

    RESET = 0
    """Remove all formatting (same as NORMAL)"""
    NORMAL = 0
    """Remove all formatting (same as RESET)"""
    BLACK = 30
    """Black foreground text"""
    RED = 31
    """Red foreground text"""
    GREEN = 32
    """Green foreground text"""
    YELLOW = 33
    """Yellow foreground text"""
    BLUE = 34
    """Blue foreground text"""
    MAGENTA = 35
    """Magenta foreground text"""
    CYAN = 36
    """Cyan foreground text"""
    WHITE = 37
    """White foreground text"""
    ON_BLACK = 40
    """Black background text"""
    ON_RED = 41
    """Red background text"""
    ON_GREEN = 42
    """Green background text"""
    ON_YELLOW = 43
    """Yellow background text"""
    ON_BLUE = 44
    """Blue background text"""
    ON_MAGENTA = 45
    """Magenta background text"""
    ON_CYAN = 46
    """Cyan background text"""
    ON_WHITE = 47
    """White background text"""
    GREY = 90
    """Grey foreground text (same as BRIGHT_BLACK)"""
    BRIGHT_BLACK = 90
    """Grey foreground text"""
    BRIGHT_RED = 91
    """Bright red foreground text"""
    BRIGHT_GREEN = 92
    """Bright green foreground text"""
    BRIGHT_YELLOW = 93
    """Bright yellow foreground text"""
    BRIGHT_BLUE = 94
    """Bright blue foreground text"""
    BRIGHT_MAGENTA = 95
    """Bright magenta foreground text"""
    BRIGHT_CYAN = 96
    """Bright cyan foreground text"""
    BRIGHT_WHITE = 97
    """Bright white foreground text"""
    ON_GREY = 100
    """Grey background text (same as ON_BRIGHT_BLACK)"""
    ON_BRIGHT_BLACK = 100
    """Grey background text"""
    ON_BRIGHT_RED = 101
    """Bright red background text"""
    ON_BRIGHT_GREEN = 102
    """Bright green background text"""
    ON_BRIGHT_YELLOW = 103
    """Bright yellow background text"""
    ON_BRIGHT_BLUE = 104
    """Bright blue background text"""
    ON_BRIGHT_MAGENTA = 105
    """Bright magenta background text"""
    ON_BRIGHT_CYAN = 106
    """Bright cyan background text"""
    ON_BRIGHT_WHITE = 107
    """Bright white background text"""
    DEFAULT_FOREGROUND = 39
    """Default foreground text colour"""
    NO_COLOUR = 39
    """Default foreground text colour"""
    NO_FOREGROUND = 39
    """Default foreground text colour"""
    DEFAULT_BACKGROUND = 49
    """Default background text colour"""
    NO_BACKGROUND = 49
    """Default background text colour"""
    BOLD = 1
    """Bold text"""
    NO_BOLD = 21
    """Not bold text"""
    FAINT = 2
    """Faint text (same as DIM). May be implemented as a lighter colour or as a thinner font."""
    DIM = 2
    """Dim text (same as FAINT). May be implemented as a lighter colour or as a thinner font."""
    NO_BOLD_FEINT = 22
    """Neither bold nor faint text"""
    ITALIC = 3
    """Italic text. Not widely supported. Sometimes treated as inverse or blink."""
    NO_ITALIC_BLACKLETTER = 23
    """Neither italic nor blackletter text"""
    SLOW_BLINK = 5
    """Sets blinking to less than 150 times per minute. Rarely supported."""
    BLINK = 5
    """Same as SLOW_BLINK"""
    RAPID_BLINK = 6
    """Sets blinking to more than 150 times per minute. Rarely supported."""
    NO_BLINK = 25
    """Sets blinking to off."""
    INVERT = 7
    """Swap foreground and background colors; inconsistent emulation"""
    NO_INVERT = 27
    """Unset invert"""
    CONCEAL = 8
    """Invisible text (same as HIDE). Not widely supported."""
    HIDE = 8
    """Invisible text (same as CONCEAL). Not widely supported."""
    REVEAL = 28
    """Unset conceal/hide (same as NO_CONCEAL and NO_HIDE)"""
    NO_CONCEAL = 28
    """Unset conceal/hide (same as REVEAL and NO_HIDE)"""
    NO_HIDE = 28
    """Unset conceal/hide (same as REVEAL and NO_CONCEAL)"""
    UNDERLINE = 4
    """Underline text. Style extensions exist for Kitty, VTE, mintty and iTerm2."""
    NO_UNDERLINE = 24
    """Unset underline"""
    DOUBE_UNDERLINE = 21
    """Double underline. Rarely supported."""
    DEFAULT_UNDERLINE_COLOUR = 59
    """Set the underline colour to the default. Not in standard; implemented in Kitty, VTE, mintty, and iTerm2."""
    OVERLINE = 53
    """Overline text"""
    NO_OVERLINE = 55
    """Unset overline"""
    CROSSED = 9
    """Crossed out text (same as STRIKE). Characters legible but marked as if for deletion."""
    NO_CROSSED = 29
    """Unset crossed out text (same as NO_STRIKE)"""
    STRIKE = 9
    """Crossed out text (same as CROSSED). Characters legible but marked as if for deletion."""
    NO_STRIKE = 29
    """Unset crossed out text (same as NO_CROSSED)"""
    RIGHT_LINE = 60
    """Line on right of text. Rarely supported."""
    RIGHT_DOUBLE_LINE = 61
    """Double line on right of text. Rarely supported."""
    LEFT_LINE = 62
    """Line on left of text. Rarely supported."""
    LEFT_DOUBLE_LINE = 63
    """Double line on left of text. Rarely supported."""
    IDEOGRAM_UNDERLINE = 60
    """Ideogram underline. Rarely supported."""
    IDEOGRAM_DOUBLE_UNDERLINE = 61
    """Ideogram double underline. Rarely supported."""
    IDEOGRAM_OVERLINE = 62
    """Ideogram overline. Rarely supported."""
    IDEOGRAM_DOUBLE_OVERLINE = 63
    """Ideogram double overline. Rarely supported."""
    IDEOGRAM_STRESS_MARK = 64
    """Ideogram stress mark. Rarely supported."""
    NO_IDEOGRAM = 65
    """Unset ideogram underline/overline/stress mark."""
    SUPERSCRIPT = 73
    """Superscript text. Implemented in mintty"""
    SUBSCRIPT = 74
    """Subscript text. Implemented in mintty"""
    NO_SUPERSCRIPT_SUBSCRIPT = 75
    """Unset superscript/subscript text"""
    PRIMARY_FONT = 10
    """Select primary font."""
    ALT_FONT_1 = 11
    """Select alternate font 1. Rarely supported."""
    ALT_FONT_2 = 12
    """Select alternate font 2. Rarely supported."""
    ALT_FONT_3 = 13
    """Select alternate font 3. Rarely supported."""
    ALT_FONT_4 = 14
    """Select alternate font 4. Rarely supported."""
    ALT_FONT_5 = 15
    """Select alternate font 5. Rarely supported."""
    ALT_FONT_6 = 16
    """Select alternate font 6. Rarely supported."""
    ALT_FONT_7 = 17
    """Select alternate font 7. Rarely supported."""
    ALT_FONT_8 = 18
    """Select alternate font 8. Rarely supported."""
    ALT_FONT_9 = 19
    """Select alternate font 9. Rarely supported."""
    FRAKTUR = 20
    """Fraktur font (same as GOTHIC). Rarely supported."""
    GOTHIC = 20
    """Gothic font (same as FRAKTUR). Rarely supported."""
    PROPORTIONAL_SPACING = 26
    """Proportional spacing. Not known to be used on terminals."""
    NO_PROPORTIONAL_SPACING = 50
    """Unset proportional spacing"""
    FRAMED = 51
    """Framed text. Implemented as "emoji variation selector" in mintty."""
    ENCIRCLED = 52
    """Encircled text. Implemented as "emoji variation selector" in mintty."""
    NO_FRAMED_ENCIRCLED = 54
    """Unset framed/encircled text"""

    def __repr__(self) -> str:
        return self.name
