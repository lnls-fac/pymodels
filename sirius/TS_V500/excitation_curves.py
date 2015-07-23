
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('TSMA-B.*')
_quad_re = _re.compile('TSMA-Q.*')
_corr_re = _re.compile('TSMA-C.*')
_sept_re = _re.compile('TSPM-S.*')

def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names()
    magnets.update(_record_names.get_pulsed_magnet_names())

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None:
            ec[name] = 'tsma-b-i2e.txt'
        elif _quad_re.match(name) is not None:
            ec[name] = 'tsma-q-i2gl.txt'
        elif _corr_re.match(name) is not None:
            ec[name] = 'tsma-c-i2bl.txt'
        elif _sept_re.match(name) is not None:
            ec[name] = 'tspm-sep.txt'
        else:
            ec[name] = 'tsma-q-i2gl.txt'

    return ec
