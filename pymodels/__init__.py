"""PyModels package."""

import os as _os
from . import coordinate_system
from .version_symbols import li, tb, bo, ts, si

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ('li', 'tb', 'bo', 'ts', 'si', 'coordinate_system')
