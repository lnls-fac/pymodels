
import re as _re
from . import device_names as _device_names
import sirius.naming_system as _naming_system

def get_excitation_curve_mapping(accelerator):
    """Get mapping from magnet to excitation curve file names

    Returns dict.
    """
    magnets = _device_names.get_magnet_names(accelerator)

    ec = dict()
    for name in magnets:
        device = _naming_system.split_name(name)['device']
        if _re.search('B', device)     is not None: ec[name] = 'boma-bend.txt'
        elif _re.search('QF', device)   is not None: ec[name] = 'boma-qf.txt'
        elif _re.search('QD', device)   is not None: ec[name] = 'boma-qd.txt'
        elif _re.search('SF', device)  is not None: ec[name] = 'boma-sf.txt'
        elif _re.search('SD', device) is not None: ec[name] = 'boma-sd.txt'
        elif _re.search('CH', device) is not None: ec[name] = 'boma-ch.txt'
        elif _re.search('CV', device) is not None: ec[name] = 'boma-cv.txt'
        elif _re.search('KICKERINJ', device) is not None: ec[name] = 'bopm-kickinj.txt'
        elif _re.search('KICKEREX', device)  is not None: ec[name] = 'bopm-kickex.txt'

    return ec
