
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('TBMA-B.*')
_quad_re    = _re.compile('TBMA-Q.*')
_corr_re    = _re.compile('TBMA-C.*')
_sept_re  = _re.compile('TBPM-S.*')

def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names()

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None: ec[name] = 'tbma-bend.txt'
        elif _quad_re.match(name) is not None: ec[name] = 'tbma-q.txt'
        elif _corr_re.match(name) is not None: ec[name] = 'tbma-c.txt'
        elif _sept_re.match(name) is not None: ec[name] = 'tbpm-sep.txt'
        else: ec[name] = 'tbma-q.txt'

    return ec
