import os as _os
from . import LI_V01_01
from . import TB_V01_03
from . import BO_V03_02
from . import TS_V03_03
from . import SI_V21_02
from . import coordinate_system
from . import discs

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['LI_V01_01', 'TB_V01_03', 'BO_V03_02', 'TS_V03_03', 'SI_V21_02']


li = LI_V01_01
tb = TB_V01_03
bo = BO_V03_02
ts = TS_V03_03
si = SI_V21_02
