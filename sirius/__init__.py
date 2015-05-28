import os as _os
from . import LI_V00
from . import BO_V901
from . import SI_V07
from . import TI_V00

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['LI_V00', 'BO_V901', 'SI_V07', 'TI_V00']

li = LI_V00
bo = BO_V901
si = SI_V07
ti = TI_V00
