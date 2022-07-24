import argparse
from typing import Iterable, List, Optional, Tuple
from . import Attributes, style, Style


def parse_args(argv: Optional[List[str]]) -> Tuple[str, Iterable[Style]]:
    parser = argparse.ArgumentParser(
        description="Print a string to your console WITH STYLE!"
    )
    parser.add_argument("string", help="The string to style.")
    parser.add_argument(
        "attrs",
        nargs="*",
        help="The attributes to apply. The supported attributes are those in the constyle.Attribute enum (case insensitive).",
    )
    args = parser.parse_args(argv)
    return args.string, (
        Attributes[attr.upper().replace("-", "_").replace(" ", "_")]
        for attr in args.attrs
    )


def main(argv: Optional[List[str]] = None):
    string, attrs = parse_args(argv)
    print(style(string, *attrs))


if __name__ == "__main__":
    main()
