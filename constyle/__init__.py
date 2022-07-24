"""
.. include:: ../README.md
"""

import importlib_metadata

try:
    __version__ = importlib_metadata.version(__package__ or __name__)
except importlib_metadata.PackageNotFoundError:
    import toml

    __version__ = (
        toml.load("pyproject.toml")
        .get("tool", {})
        .get("poetry", {})
        .get("version", "unknown")
        + "-dev"
    )

from ._style import Style, style
from ._attributes import Attributes

__all__ = ["Style", "Attributes", "style"]
