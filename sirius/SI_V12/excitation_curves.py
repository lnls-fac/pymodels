
import re as _re
from . import record_names as _record_names

_bc_re = _re.compile('SIMA-BC.*')
_b1_re = _re.compile('SIMA-B1.*')
_b2_re = _re.compile('SIMA-B2.*')
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
_sf_re = _re.compile('SIMA-SF.*')
_sd_re = _re.compile('SIMA-SD.*')
_ch_re = _re.compile('SIMA-CH.*')
_cv_re = _re.compile('SIMA-CV.*')
_fch_re = _re.compile('SIMA-FCH.*')
_fcv_re = _re.compile('SIMA-FCV.*')

def get_excitation_curve_mapping(accelerator):
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _record_names.get_magnet_names(accelerator)

    ec = dict()
    for name in magnets:
        if _b1_re.match(name) is not None: ec[name] = 'sima-b1.txt'
        elif _b2_re.match(name) is not None: ec[name] = 'sima-b2.txt'
        elif _bc_re.match(name) is not None: ec[name] = 'sima-bend.txt'
        elif _qda_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdb1_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdb2_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qfa_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf1_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf2_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf3_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qf4_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qfb_re.match(name) is not None: ec[name] = 'sima-q30.txt'
        elif _qs_re.match(name) is not None: ec[name] = 'sima-qs.txt'
        elif _sf_re.match(name) is not None: ec[name] = 'sima-sf.txt'
        elif _sd_re.match(name) is not None: ec[name] = 'sima-sd.txt'
        elif _ch_re.match(name) is not None: ec[name] = 'sima-ch.txt'
        elif _cv_re.match(name) is not None: ec[name] = 'sima-cv.txt'
        elif _fch_re.match(name) is not None: ec[name] = 'sima-ch.txt'
        elif _fcv_re.match(name) is not None: ec[name] = 'sima-cv.txt'

    return ec
