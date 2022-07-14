"""
.. include:: ../README.md
"""


import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    import toml

    __version__ = (
        toml.load("pyproject.toml")
        .get("tool", {})
        .get("poetry", {})
        .get("version", "unknown")
        + "-dev"
    )
