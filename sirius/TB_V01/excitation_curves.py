
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
        if _re.search('B', device)     is not None: ec[name] = 'tbma-bend.txt'
        elif _re.search('Q', device)   is not None: ec[name] = 'tbma-q.txt'
        elif _re.search('CH', device)   is not None: ec[name] = 'tbpm-ch.txt'
        elif _re.search('CV', device)  is not None: ec[name] = 'tbpm-cv.txt'
        elif _re.search('S', device) is not None: ec[name] = 'tbpm-sep.txt'

    return ec
