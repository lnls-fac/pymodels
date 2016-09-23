import os as _os
from . import LI_V00
from . import TB_V01
from . import BO_V02A
from . import TS_V01
from . import SI_V14
from . import SI_V20_01

from . import coordinate_system

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['LI_V00', 'TB_V01', 'BO_V02A', 'TS_V01', 'SI_V20_01']


li = LI_V00
tb = TB_V01
bo = BO_V02A
ts = TS_V01
si = SI_V20_01
