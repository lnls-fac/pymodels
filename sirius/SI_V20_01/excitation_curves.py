
import re as _re
from . import device_names as _device_names

def get_excitation_curve_mapping(accelerator):
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _device_names.get_magnet_names(accelerator)

    ec = dict()
    for name in magnets:
        device = _device_names.split_name(name)['device']
        if _re.search('B1', device)     is not None: ec[name] = 'sima-b1.txt'
        elif _re.search('B2', device)   is not None: ec[name] = 'sima-b2.txt'
        elif _re.search('BC', device)   is not None: ec[name] = 'sima-bend.txt'
        elif _re.search('QDA', device)  is not None: ec[name] = 'sima-q14.txt'
        elif _re.search('QDB1', device) is not None: ec[name] = 'sima-q14.txt'
        elif _re.search('QDB2', device) is not None: ec[name] = 'sima-q14.txt'
        elif _re.search('QDP1', device) is not None: ec[name] = 'sima-q14.txt'
        elif _re.search('QDP2', device) is not None: ec[name] = 'sima-q14.txt'
        elif _re.search('QFA', device)  is not None: ec[name] = 'sima-q20.txt'
        elif _re.search('Q1', device)   is not None: ec[name] = 'sima-q20.txt'
        elif _re.search('Q2', device)   is not None: ec[name] = 'sima-q20.txt'
        elif _re.search('Q3', device)   is not None: ec[name] = 'sima-q20.txt'
        elif _re.search('Q4', device)   is not None: ec[name] = 'sima-q20.txt'
        elif _re.search('QFB', device)  is not None: ec[name] = 'sima-q30.txt'
        elif _re.search('QFP', device)  is not None: ec[name] = 'sima-q30.txt'
        elif _re.search('QS', device)   is not None: ec[name] = 'sima-qs.txt'
        elif _re.search('SF', device)   is not None: ec[name] = 'sima-sf.txt'
        elif _re.search('SD', device)   is not None: ec[name] = 'sima-sd.txt'
        elif _re.search('CH', device)   is not None: ec[name] = 'sima-ch.txt'
        elif _re.search('CV', device)   is not None: ec[name] = 'sima-cv.txt'
        elif _re.search('FCH', device)  is not None: ec[name] = 'sima-ch.txt'
        elif _re.search('FCV', device)  is not None: ec[name] = 'sima-cv.txt'
        elif _re.search('DIPK', device) is not None: ec[name] = 'sipm-kickinj.txt'
        elif _re.search('NLK', device)  is not None: ec[name] = 'sipm-nlk.txt'

    return ec
