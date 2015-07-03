
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('BOMA-B.*')
_qf_re = _re.compile('BOMA-QF.*')
_qd_re = _re.compile('BOMA-QD.*')
_s_re = _re.compile('BOMA-S.*')
_c_re = _re.compile('BOMA-C.*')


def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names()

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None: ec[name] = 'boma-bend.txt'
        elif _qf_re.match(name) is not None: ec[name] = 'boma-qf.txt'
        elif _qd_re.match(name) is not None: ec[name] = 'boma-qd.txt'
        elif _s_re.match(name) is not None: ec[name] = 'boma-s.txt'
        elif _c_re.match(name) is not None: ec[name] = 'boma-c.txt'
        else: ec[name] = 'boma-s.txt'

    return ec
