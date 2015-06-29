
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('BOMA-B.*')
_quad_re = _re.compile('BOMA-Q.*')
_corr_re = _re.compile('MOMA-C.*')


def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_record_names('boma')

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None:
            ec[name] = 'boma-b-i2e.txt'
        elif _quad_re.match(name) is not None:
            ec[name] = 'boma-q-i2gl.txt'
        elif _corr_re.match(name) is not None:
            ec[name] = 'boma-c-i2bl.txt'
        else:
            ec[name] = 'boma-q-i2gl.txt'

    return ec
