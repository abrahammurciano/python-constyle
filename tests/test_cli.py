import shlex
from typing import Callable, Tuple
import pytest
from constyle import Attributes, Style
from constyle.__main__ import main


@pytest.fixture(
    params=[
        "",
        "Hello",
        "Hello World",
    ]
)
def string(request) -> str:
    return request.param


@pytest.fixture(
    params=[
        ("", Style()),
        ("-a red", Attributes.RED),
        ("-a bright_blue -a on-white", Attributes.BRIGHT_BLUE + Attributes.ON_WHITE),
    ]
)
def attrs(request) -> Tuple[str, Callable[[str], str]]:
    return request.param


def test_cli(string: str, attrs: Tuple[str, Callable[[str], str]], capsys) -> None:
    try:
        main(shlex.split(f"{attrs[0]} {string}"))
        captured = capsys.readouterr()
        assert captured.out.strip() == attrs[1](string)
        assert captured.err.strip() == ""
    except SystemExit as e:
        assert e.code == 0
