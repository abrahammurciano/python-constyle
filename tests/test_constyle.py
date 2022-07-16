from typing import List, Tuple
from constyle import style, Style, Attributes, Attribute
import pytest

TEST_STR = "Hello World"
TEST_CASE_T = Tuple[List[Attribute], str, str]


@pytest.fixture(
    params=[
        pytest.param(([], "", ""), id="NoAttrs"),
        pytest.param(([Attributes.BOLD], "\033[1m", "\033[0m"), id="OneAttr"),
        pytest.param(
            ([Attributes.BOLD, Attributes.GREEN], "\033[1m\033[32m", "\033[0m"),
            id="TwoAttrs",
        ),
    ]
)
def test_case(request) -> TEST_CASE_T:
    """The list of attributes to use, the prefix to expect, and the suffix to expect."""
    return request.param


def test_style_function(test_case: TEST_CASE_T):
    attrs, prefix, suffix = test_case
    assert style(TEST_STR, *attrs) == prefix + TEST_STR + suffix


def test_style_class(test_case: TEST_CASE_T):
    attrs, prefix, suffix = test_case
    assert Style(*attrs)(TEST_STR) == prefix + TEST_STR + suffix
