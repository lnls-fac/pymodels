"""PyModels package."""

import os as _os
from . import LI_V01_01
from . import TB_V04_01
from . import BO_V05_04
from . import TS_V03_03
from . import SI_V24_04
from . import coordinate_system
from . import middlelayer

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ('LI_V01_01', 'TB_V04_01', 'BO_V05_04', 'TS_V03_03', 'SI_V24_04')


li = LI_V01_01
tb = TB_V04_01
bo = BO_V05_04
ts = TS_V03_03
si = SI_V24_04
