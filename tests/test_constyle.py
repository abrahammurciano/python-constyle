import re
from dataclasses import dataclass
from typing import Callable, List, Pattern, Union

import pytest

from constyle import Attributes, Style, style

TEST_STR = "Hello World"
RESET_PATTERN = re.compile(r"\033\[0*m")


@dataclass
class TstCase:
    styles: List[Style]
    prefix: Union[str, Pattern]
    suffix: Union[str, Pattern]


@pytest.fixture(
    params=[
        pytest.param(
            TstCase([], RESET_PATTERN, RESET_PATTERN),
            id="NoAttrs",
        ),
        pytest.param(
            TstCase([Attributes.BOLD], "\033[1m", RESET_PATTERN),
            id="OneAttr",
        ),
        pytest.param(
            TstCase(
                [Attributes.BOLD, Attributes.GREEN],
                re.compile(r"\033\[1(m\033\[|;)32m"),
                RESET_PATTERN,
            ),
            id="TwoAttrs",
        ),
    ]
)
def test_case(request) -> TstCase:
    """The list of attributes to use, the prefix to expect, and the suffix to expect."""
    return request.param


@pytest.fixture(
    params=[
        pytest.param(lambda string, styles: style(string, *styles), id="func"),
        pytest.param(lambda string, styles: Style(*styles)(string), id="class"),
    ]
)
def method(request) -> Callable[[str, List[Style]], str]:
    return request.param


def test_style_function(test_case: TstCase, method: Callable[[str, List[Style]], str]):
    styled = method(TEST_STR, test_case.styles)
    prefix, suffix = styled.split(TEST_STR)
    for expected, actual in ((test_case.prefix, prefix), (test_case.suffix, suffix)):
        if isinstance(expected, str):
            assert expected == actual
        else:
            assert expected.match(actual)


def test_add() -> None:
    assert (
        Attributes.BOLD + Style(Attributes.ITALIC, Attributes.RED)
        == Style(Attributes.BOLD, Attributes.ITALIC, Attributes.RED)
        == Attributes.BOLD + Attributes.ITALIC + Attributes.RED
    )


def test_attribute_call() -> None:
    assert Attributes.BOLD("Hello World") == style("Hello World", Attributes.BOLD)


def test_non_string() -> None:
    assert style(None, Attributes.BOLD) == style("None", Attributes.BOLD)
