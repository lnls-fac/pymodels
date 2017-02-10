import os as _os
from . import LI_V01_01
from . import TB_V01_03
from . import BO_V03_02
from . import TS_V01
from . import SI_V17_01
from . import SI_V20_01
from . import coordinate_system

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['LI_V01_01', 'TB_V01_03', 'BO_V03_02', 'TS_V01', 'SI_V20_01']


li = LI_V01_01
tb = TB_V01_03
bo = BO_V03_02
ts = TS_V01
si = SI_V20_01
