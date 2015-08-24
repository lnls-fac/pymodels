
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('SIMA-B.*')
_qfa_re = _re.compile('SIMA-QFA.*')
_qfb_re = _re.compile('SIMA-QFB.*')
_qf1_re = _re.compile('SIMA-QF1.*')
_qf2_re = _re.compile('SIMA-QF2.*')
_qf3_re = _re.compile('SIMA-QF3.*')
_qf4_re = _re.compile('SIMA-QF4.*')
_qda_re = _re.compile('SIMA-QDA.*')
_qdb1_re = _re.compile('SIMA-QDB1.*')
_qdb2_re = _re.compile('SIMA-QDB2.*')
_qs_re = _re.compile('SIMA-QS.*')
_s_re = _re.compile('SIMA-S.*')
_c_re = _re.compile('SIMA-C.*')


def get_excitation_curve_mapping():
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names()

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None: ec[name] = 'sima-bend.txt'
        elif _qda_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdb1_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdb2_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qf1_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf2_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf3_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf4_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qfb_re.match(name) is not None: ec[name] = 'sima-q30.txt'
        elif _qs_re.match(name) is not None: ec[name] = 'sima-qs.txt'
        elif _s_re.match(name) is not None: ec[name] = 'sima-s.txt'
        elif _c_re.match(name) is not None: ec[name] = 'sima-c.txt'
        else: ec[name] = 'sima-q14.txt'

    return ec
