
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
        if _re.search('B', device)     is not None: ec[name] = 'tsma-bend.txt'
        elif _re.search('Q', device)   is not None: ec[name] = 'tsma-q.txt'
        elif _re.search('CH', device)   is not None: ec[name] = 'tsma-ch.txt'
        elif _re.search('CV', device)  is not None: ec[name] = 'tsma-cv.txt'
        elif _re.search('SEPTUME', device) is not None: ec[name] = 'tspm-septex.txt'
        elif _re.search('SEPTUMTHICK', device)  is not None: ec[name] = 'tspm-septing.txt'
        elif _re.search('SEPTUMTHIN', device) is not None: ec[name] = 'tspm-septinf.txt'

    return ec
