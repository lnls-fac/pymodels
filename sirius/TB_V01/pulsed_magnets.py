
from . import device_names as _device_names

_system  = 'tb'

# INJECTION SEPTUM
_pm1_sec   =  '05'
_pm1_name  = _device_names.join_name(_system, 'PM', 'SEPTUMINJ', _pm1_sec)
_pm1_delay = _device_names.join_name(_system, 'TI', 'SOE',  _pm1_sec) + ':TrigDelayCh01'
_pm1_enbl  = _device_names.join_name(_system, 'TI', 'SOE',  _pm1_sec) + ':TrigEnblCh01'
_pm1_pc    = 'tbpm-sep-pulse.txt'


def get_magnet_delay_mapping():
    """Get mapping from pulsed magnet to timing delay

    Returns dict.
    """
    mapping = {}
    mapping[_pm1_name] = _pm1_delay

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_magnet_enabled_mapping():
    """Get mapping from pulsed magnet to timing enabled

    Returns dict.
    """
    mapping = {}
    mapping[_pm1_name] = _pm1_enbl

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_pulse_curve_mapping():
    """Get mapping from pulsed magnet to pulse curve file names

    Returns dict.
    """
    mapping = {}
    mapping[_pm1_name] = _pm1_pc

    return mapping
