
"""Interactive sirius module

Use this module to define variables and functions to be globally available when
using

    'from sirius.interactive import *'
"""

from pyaccel.interactive import *
from . import si
from . import bo
from . import tb
from . import ts


__all__ = [name for name in dir() if not name.startswith('_')]

print('Names defined in sirius.interactive: ' + ', '.join(__all__) + '.\n')
