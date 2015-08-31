
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('TSMA-B.*')
_quad_re = _re.compile('TSMA-Q.*')
_ch_re = _re.compile('TSMA-CH.*')
_cv_re = _re.compile('TSMA-CV.*')
_sept_re = _re.compile('TSPM-S.*')

def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names()

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None:
            ec[name] = 'tsma-bend.txt'
        elif _quad_re.match(name) is not None:
            ec[name] = 'tsma-q.txt'
        elif _ch_re.match(name) is not None:
            ec[name] = 'tsma-ch.txt'
        elif _cv_re.match(name) is not None:
            ec[name] = 'tsma-cv.txt'
        elif _sept_re.match(name) is not None:
            ec[name] = 'tspm-sep.txt'

    return ec
