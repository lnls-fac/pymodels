
import re as _re
from . import device_names as _device_names


_bend_re = _re.compile('BOMA-B.*')
_qf_re = _re.compile('BOMA-QF.*')
_qd_re = _re.compile('BOMA-QD.*')
_sf_re = _re.compile('BOMA-SF.*')
_sd_re = _re.compile('BOMA-SD.*')
_ch_re = _re.compile('BOMA-CH.*')
_cv_re = _re.compile('BOMA-CV.*')
_kick_in_re = _re.compile('BOPM-KICKERINJ.*')
_kick_ex_re = _re.compile('BOPM-KICKEREX.*')

def get_excitation_curve_mapping(accelerator):
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _device_names.get_magnet_names(accelerator)

    ec = dict()
    for name in magnets:
        if _bend_re.match(name) is not None: ec[name] = 'boma-bend.txt'
        elif _qf_re.match(name) is not None: ec[name] = 'boma-qf.txt'
        elif _qd_re.match(name) is not None: ec[name] = 'boma-qd.txt'
        elif _sf_re.match(name) is not None: ec[name] = 'boma-sf.txt'
        elif _sd_re.match(name) is not None: ec[name] = 'boma-sd.txt'
        elif _ch_re.match(name) is not None: ec[name] = 'boma-ch.txt'
        elif _cv_re.match(name) is not None: ec[name] = 'boma-cv.txt'
        elif _kick_in_re.match(name) is not None: ec[name] = 'bopm-kickinj.txt'
        elif _kick_ex_re.match(name) is not None: ec[name] = 'bopm-kickex.txt'
        elif _sd_re.match(name) is not None : ec[name] = 'boma-sd.txt'

    return ec
