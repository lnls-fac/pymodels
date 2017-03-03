
import re as _re
from . import device_names as _device_names

_septex_re  = _re.compile('TSPM-SEPTUME.*')
_septin_re  = _re.compile('TSPM-SEPTUMT.*')

def get_pulse_curve_mapping(accelerator):
    """Get mapping from pulsed magnet to pulse curve file names

    Returns dict.
    """
    pulsed_magnets = _device_names.get_device_names(accelerator, 'tspm')

    pc = dict()
    for name in pulsed_magnets:
        if _septex_re.match(name) is not None: pc[name] = 'tspm-septex-pulse.txt'
        elif _septin_re.match(name) is not None: pc[name] = 'tspm-septin-pulse.txt'

    return pc

def get_magnet_delay_mapping(accelerator):
    """Get mapping from pulsed magnet to timing delay

    Returns dict.
    """
    pulsed_magnets = _device_names.get_device_names(accelerator, 'tspm')
    timing_variables = _device_names.get_device_names(accelerator, 'tsti')

    mapping = dict()
    for magnet in pulsed_magnets.keys():
        magnet_name = magnet.split('-')[1]
        for timing_variable in timing_variables.keys():
            name = timing_variable[5:]
            if _re.match(magnet_name, name) is not None and 'DELAY' in name:
                mapping[magnet] = timing_variable

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_magnet_enabled_mapping(accelerator):
    """Get mapping from pulsed magnet to timing enabled

    Returns dict.
    """
    pulsed_magnets = _device_names.get_device_names(accelerator, 'tspm')
    timing_variables = _device_names.get_device_names(accelerator, 'tsti')

    mapping = dict()
    for magnet in pulsed_magnets.keys():
        magnet_name = magnet.split('-')[1]
        for timing_variable in timing_variables.keys():
            name = timing_variable[5:]
            if _re.match(magnet_name, name) is not None and 'ENABLED' in name:
                mapping[magnet] = timing_variable


    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key


    return mapping, inverse_mapping
