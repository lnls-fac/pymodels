
from . import device_names as _device_names

_system  = 'si'

# DIPK
_pm1_sec   =  '01SA'
_pm1_name  = _device_names.join_name(_system, 'PM', 'DIPK', _pm1_sec)
_pm1_delay = _device_names.join_name(_system, 'TI', 'SOE',  _pm1_sec) + ':TrigDelayCh01'
_pm1_enbl  = _device_names.join_name(_system, 'TI', 'SOE',  _pm1_sec) + ':TrigEnblCh01'
_pm1_pc    = 'sipm-dipk-pulse.txt'

# NLK
_pm2_sec   =  '01SA'
_pm2_name  = _device_names.join_name(_system, 'PM', 'NLK', _pm2_sec)
_pm2_delay = _device_names.join_name(_system, 'TI', 'SOE', _pm2_sec) + ':TrigDelayCh01'
_pm2_enbl  = _device_names.join_name(_system, 'TI', 'SOE', _pm2_sec) + ':TrigEnblCh01'
_pm2_pc    = 'sipm-nlk-pulse.txt'


def get_magnet_delay_mapping():
    """Get mapping from pulsed magnet to timing delay

    Returns dict.
    """
    mapping = {}
    mapping[_pm1_name] = _pm1_delay
    mapping[_pm2_name] = _pm2_delay

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
    mapping[_pm2_name] = _pm2_enbl

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
    mapping[_pm2_name] = _pm2_pc

    return mapping
