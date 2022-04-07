"""PyModels package."""

import os as _os
from . import LI_V01_01
from . import TB_V04_01
from . import BO_V06_01
from . import TS_V04_01
from . import SI_V25_04
from . import coordinate_system

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ('LI_V01_01', 'TB_V04_01', 'BO_V06_01', 'TS_V04_01', 'SI_V25_04')


li = LI_V01_01
tb = TB_V04_01
bo = BO_V06_01
ts = TS_V04_01
si = SI_V25_04
