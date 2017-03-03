
import re as _re
from . import device_names as _device_names

_bc_re = _re.compile('SIMA-BC.*')
_b1_re = _re.compile('SIMA-B1.*')
_b2_re = _re.compile('SIMA-B2.*')
_qfa_re = _re.compile('SIMA-QFA.*')
_qfb_re = _re.compile('SIMA-QFB.*')
_qfp_re = _re.compile('SIMA-QFP.*')
_q1_re = _re.compile('SIMA-Q1.*')
_q2_re = _re.compile('SIMA-Q2.*')
_q3_re = _re.compile('SIMA-Q3.*')
_q4_re = _re.compile('SIMA-Q4.*')
_qda_re = _re.compile('SIMA-QDA.*')
_qdb1_re = _re.compile('SIMA-QDB1.*')
_qdb2_re = _re.compile('SIMA-QDB2.*')
_qdp1_re = _re.compile('SIMA-QDP1.*')
_qdp2_re = _re.compile('SIMA-QDP2.*')
_qs_re = _re.compile('SIMA-QS.*')
_sf_re = _re.compile('SIMA-SF.*')
_sd_re = _re.compile('SIMA-SD.*')
_ch_re = _re.compile('SIMA-CH.*')
_cv_re = _re.compile('SIMA-CV.*')
_fch_re = _re.compile('SIMA-FCH.*')
_fcv_re = _re.compile('SIMA-FCV.*')
_kick_re = _re.compile('SIPM-KICK.*')
_pmm_re = _re.compile('SIPM-PMM.*')

def get_excitation_curve_mapping(accelerator):
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _device_names.get_magnet_names(accelerator)

    ec = dict()
    for name in magnets:
        if _b1_re.match(name) is not None: ec[name] = 'sima-b1.txt'
        elif _b2_re.match(name) is not None: ec[name] = 'sima-b2.txt'
        elif _bc_re.match(name) is not None: ec[name] = 'sima-bend.txt'
        elif _qda_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdb1_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdb2_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdp1_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qdp2_re.match(name) is not None: ec[name] = 'sima-q14.txt'
        elif _qfa_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _q1_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _q2_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _q3_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _q4_re.match(name) is not None: ec[name] = 'sima-q20.txt'
        elif _qfb_re.match(name) is not None: ec[name] = 'sima-q30.txt'
        elif _qfp_re.match(name) is not None: ec[name] = 'sima-q30.txt'
        elif _qs_re.match(name) is not None: ec[name] = 'sima-qs.txt'
        elif _sf_re.match(name) is not None: ec[name] = 'sima-sf.txt'
        elif _sd_re.match(name) is not None: ec[name] = 'sima-sd.txt'
        elif _ch_re.match(name) is not None: ec[name] = 'sima-ch.txt'
        elif _cv_re.match(name) is not None: ec[name] = 'sima-cv.txt'
        elif _fch_re.match(name) is not None: ec[name] = 'sima-ch.txt'
        elif _fcv_re.match(name) is not None: ec[name] = 'sima-cv.txt'
        elif _kick_re.match(name) is not None: ec[name] = 'sipm-kickinj.txt'
        elif _pmm_re.match(name) is not None: ec[name] = 'sipm-pmm.txt'

    return ec
