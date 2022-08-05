import argparse
from typing import Iterable, List, Optional, Tuple
from . import Attributes, style, Style


def _available_attrs_help() -> str:
    valid_attrs = (
        (
            "\n\n"
            f" - {attr(attr.name.lower())}\n"
            f"     {getattr(attr, f'__doc_{attr.name}__')}"
        )
        for attr in sorted(Attributes.__members__.values(), key=lambda a: a.value)
        if not attr.name.startswith("_") and attr.name.upper() == attr.name
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
