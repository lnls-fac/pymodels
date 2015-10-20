
import re as _re
from . import record_names as _record_names


_bend_re = _re.compile('BOMA-B.*')
_qf_re = _re.compile('BOMA-QF.*')
_qd_re = _re.compile('BOMA-QD.*')
_s_re = _re.compile('BOMA-S.*')
_ch_re = _re.compile('BOMA-CH.*')
_cv_re = _re.compile('BOMA-CV.*')


def get_excitation_curve_mapping(accelerator):
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names(accelerator)

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None: ec[name] = 'boma-bend.txt'
        elif _qf_re.match(name) is not None: ec[name] = 'boma-qf.txt'
        elif _qd_re.match(name) is not None: ec[name] = 'boma-qd.txt'
        elif _s_re.match(name) is not None: ec[name] = 'boma-s.txt'
        elif _ch_re.match(name) is not None: ec[name] = 'boma-ch.txt'
        elif _cv_re.match(name) is not None: ec[name] = 'boma-cv.txt'
        else: ec[name] = 'boma-s.txt'

    return ec
