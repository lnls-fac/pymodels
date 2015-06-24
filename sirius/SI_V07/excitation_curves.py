
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('SIMA-B.*')
_quad_re = _re.compile('SIMA-Q.*')
_corr_re = _re.compile('SIMA-C.*')


def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_record_names('sima')

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None:
            ec[name] = 'sima-b-i2e.txt'
        elif _quad_re.match(name) is not None:
            ec[name] = 'sima-q-i2gl.txt'
        elif _corr_re.match(name) is not None:
            ec[name] = 'sima-c-i2bl.txt'
        else:
            ec[name] = 'sima-q-i2gl.txt'

    return ec
