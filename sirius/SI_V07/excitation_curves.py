"""Mapping from magnet name to excitation curve"""

import re as _re


_bend_re = _re.compile('SIMA-BEND-.*')
_quad_re = _re.compile('SIMA-Q.*')
_corr_re = _re.compile('SIMA-C.*')


def get_excitation_curve_mapping(record_names):
    """Get mapping from magnet name to excitation curve file name

    Returns dict.
    """
    magnets = [key for key in record_names.keys() if key.startswith('SIMA-')]

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None:
            ec[name] = 'sima-bend-i2e.txt'
        elif _quad_re.match(name) is not None:
            ec[name] = 'sima-q-i2gl.txt'
        elif _corr_re.match(name) is not None:
            ec[name] = 'sima-c-i2bl.txt'
        else:
            ec[name] = 'sima-q-i2gl.txt'

    return ec
