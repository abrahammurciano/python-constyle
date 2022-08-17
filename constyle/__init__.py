"""
.. include:: ../README.md
"""

import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

__version__ = metadata.version(__package__ or __name__)

from ._style import Style, style
from ._attributes import Attributes

__all__ = ["Style", "Attributes", "style"]
