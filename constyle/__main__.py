import argparse
import ast
import inspect
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple
from . import Attributes, style, Style


class _AttributesDocs(ast.NodeVisitor):
    def __init__(self):
        self.docs = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if node.name != "Attributes":
            return
        statements = node.body
        for name, doc in self._get_enum_values(statements):
            self.docs[name] = doc

    def _get_enum_values(self, statements: List[ast.stmt]) -> Iterable[Tuple[str, str]]:
        i = 0
        while i < len(statements):
            assignment = statements[i]
            if not isinstance(assignment, ast.Assign):
                i += 1
                continue
            assert isinstance(assignment, ast.Assign)
            target = assignment.targets[0]
            if not isinstance(target, ast.Name):
                i += 1
                continue
            assert isinstance(target, ast.Name)
            name = target.id

            i += 1
            expr = statements[i]
            if not isinstance(expr, ast.Expr):
                continue
            const = expr.value
            if not isinstance(const, ast.Constant):
                continue
            doc = const.value
            if not isinstance(doc, str):
                continue
            yield name, doc


def _available_attrs_help() -> str:
    _attrs_docs = _AttributesDocs()
    with Path(inspect.getfile(Attributes)).open() as f:
        _attrs_docs.visit(ast.parse(f.read()))
    valid_attrs = "\n - ".join(
        f"{Attributes[attr_name](attr_name.lower())} - {_attrs_docs.docs[attr_name] or 'No documentation'}"
        for attr_name in sorted(_attrs_docs.docs.keys())
    )
    return f"Valid attributes (case insensitive) are:\n - {valid_attrs}"


def _valid_attr(attr: str) -> Attributes:
    attr = attr.upper().replace("-", "_").replace(" ", "_")
    try:
        return Attributes[attr]
    except KeyError:
        raise argparse.ArgumentTypeError(
            f"Invalid attribute: {attr}.\n{_available_attrs_help()}"
        )


def parse_args(argv: Optional[List[str]]) -> Tuple[str, Iterable[Style]]:
    parser = argparse.ArgumentParser(
        description="Print a string to your console WITH STYLE!",
        epilog=_available_attrs_help(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("string", help="The string to style.")
    parser.add_argument(
        "attrs",
        nargs="*",
        type=_valid_attr,
        help="The attributes to apply. The supported attributes are those in the constyle.Attributes enum (case insensitive).",
    )
    args = parser.parse_args(argv)
    return args.string, args.attrs


def main(argv: Optional[List[str]] = None):
    string, attrs = parse_args(argv)
    print(style(string, *attrs))


if __name__ == "__main__":
    main()
