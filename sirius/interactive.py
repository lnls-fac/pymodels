
"""Interactive sirius module

Use this module to define variables and functions to be globally available when
using

    'from sirius.interactive import *'
"""

from pyaccel.interactive import *
import sirius.SI_V07 as si_model
import sirius.BO_V901 as bo_model


__all__ = [name for name in dir() if not name.startswith('_')]

print('Names defined in sirius.interactive: ' + ', '.join(__all__) + '.\n')
