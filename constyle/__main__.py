import argparse
import ast
import inspect
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from . import Attributes, style, Style


class _AttributesDocs(ast.NodeVisitor):
    def __init__(self):
        self.docs: Dict[str, Optional[str]] = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == "Attributes":
            self._set_enum_docs(node.body)

    def _set_enum_docs(self, statements: Sequence[ast.stmt]):
        for doc, names in (
            (_get_doc(statements, i + 1), _get_names(s))
            for i, s in enumerate(statements)
            if isinstance(s, ast.Assign)
        ):
            self.docs.update({name: doc for name in names})


def _get_doc(statements: Sequence[ast.stmt], index: int) -> Optional[str]:
    try:
        stmt = statements[index]
        assert isinstance(stmt, ast.Expr)
        assert isinstance(stmt.value, ast.Constant)
        assert isinstance(stmt.value.value, str)
        return stmt.value.value
    except (IndexError, AssertionError):
        return None


def _get_names(assignment: ast.Assign) -> Iterable[str]:
    return (target.id for target in assignment.targets if isinstance(target, ast.Name))


def _available_attrs_help() -> str:
    _attrs_docs = _AttributesDocs()
    with Path(inspect.getfile(Attributes)).open() as f:
        _attrs_docs.visit(ast.parse(f.read()))
    docs = {
        k: v
        for k, v in _attrs_docs.docs.items()
        if not k.startswith("_") and k.upper() == k
    }
    valid_attrs = (
        f"\n\n - {Attributes[name](name.lower())}\n{' ' * 5}{docs[name] or '[missing documentation]'}"
        for name in sorted(docs, key=lambda n: Attributes[n].value)
    )
    return f"Valid attributes (case insensitive) are:{''.join(valid_attrs)}"


def _valid_attr(attr: str) -> Attributes:
    attr = attr.upper().replace("-", "_").replace(" ", "_")
    try:
        return Attributes[attr]
    except KeyError:
        raise argparse.ArgumentTypeError(
            f"Invalid attribute: {attr}. Use --help to see the available attributes."
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
