import argparse
from typing import Iterable, List, Optional, Tuple
from attributes_doc import get_doc
from . import Attributes, style, Style


def _available_attrs_help() -> str:
    valid_attrs = (
        f"\n\n - {attr(name.lower())}\n     {get_doc(Attributes, name)}"
        for name, attr in sorted(
            Attributes.__members__.items(), key=lambda a: a[1].value
        )
        if not name.startswith("_") and name.upper() == name
    )
    return f"Valid attributes (case insensitive) are:{''.join(valid_attrs)}"


def _valid_attr(name: str) -> Attributes:
    name = name.upper().replace("-", "_").replace(" ", "_")
    try:
        return Attributes[name]
    except KeyError:
        raise argparse.ArgumentTypeError(
            f"Invalid attribute: {name}. Use --help to see the available attributes."
        )


def parse_args(argv: Optional[List[str]]) -> Tuple[Iterable[str], Iterable[Style]]:
    parser = argparse.ArgumentParser(
        description="Print a string to your console WITH STYLE!",
        epilog=_available_attrs_help(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "STRING",
        nargs="*",
        type=lambda s: s[1:] if s.startswith("\\-") else s,
        help="A string to style.",
    )
    parser.add_argument(
        "-a",
        "--attr",
        "--attribute",
        action="append",
        dest="attrs",
        default=[],
        type=_valid_attr,
        help="The attributes to apply. The supported attributes are those in the constyle.Attributes enum (case insensitive).",
    )
    args = parser.parse_args(argv)
    return args.STRING, args.attrs


def main(argv: Optional[List[str]] = None):
    strings, attrs = parse_args(argv)
    print(style(" ".join(strings), *attrs))


if __name__ == "__main__":
    main()
