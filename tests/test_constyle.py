from dataclasses import dataclass
import re
from typing import Callable, List, Pattern, Union
from constyle import style, Style, Attributes
import pytest

TEST_STR = "Hello World"
RESET_PATTERN = re.compile(r"\033\[0*m")


@dataclass
class TestCase:
    styles: List[Style]
    prefix: Union[str, Pattern]
    suffix: Union[str, Pattern]


@pytest.fixture(
    params=[
        pytest.param(
            TestCase([], RESET_PATTERN, RESET_PATTERN),
            id="NoAttrs",
        ),
        pytest.param(
            TestCase([Attributes.BOLD], "\033[1m", RESET_PATTERN),
            id="OneAttr",
        ),
        pytest.param(
            TestCase(
                [Attributes.BOLD, Attributes.GREEN],
                re.compile(r"\033\[1(m\033\[|;)32m"),
                RESET_PATTERN,
            ),
            id="TwoAttrs",
        ),
    ]
)
def test_case(request) -> TestCase:
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


def test_style_function(test_case: TestCase, method: Callable[[str, List[Style]], str]):
    styled = method(TEST_STR, test_case.styles)
    prefix, suffix = styled.split(TEST_STR)
    for expected, actual in ((test_case.prefix, prefix), (test_case.suffix, suffix)):
        if isinstance(expected, str):
            assert expected == actual
        else:
            assert expected.match(actual)
