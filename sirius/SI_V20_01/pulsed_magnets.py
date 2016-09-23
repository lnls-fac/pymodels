
from . import device_names as _device_names

_system  = 'si'

_dipk_sec   =  '01SA'
_dipk_pm    = _device_names.join_name(_system, 'PM', 'DIPK', _dipk_sec)
_dipk_delay = _device_names.join_name(_system, 'TI', 'SOE',  _dipk_sec) + ':TrigDelayCh01'
_dipk_enbl  = _device_names.join_name(_system, 'TI', 'SOE',  _dipk_sec) + ':TrigEnblCh01'
_dipk_pc    = 'sipm-dipk-pulse.txt'

_nlk_sec    =  '01SA'
_nlk_pm     = _device_names.join_name(_system, 'PM', 'NLK', _nlk_sec)
_nlk_delay  = _device_names.join_name(_system, 'TI', 'SOE', _nlk_sec) + ':TrigDelayCh02'
_nlk_enbl   = _device_names.join_name(_system, 'TI', 'SOE', _nlk_sec) + ':TrigEnblCh02'
_nlk_pc     = 'sipm-nlk-pulse.txt'


def get_magnet_delay_mapping():
    """Get mapping from pulsed magnet to timing delay

    Returns dict.
    """
    mapping = {}
    mapping[_dipk_pm] = _dipk_delay
    mapping[_nlk_pm ] = _nlk_delay

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_magnet_enabled_mapping():
    """Get mapping from pulsed magnet to timing enabled

    Returns dict.
    """
    mapping = {}
    mapping[_dipk_pm] = _dipk_enbl
    mapping[_nlk_pm ] = _nlk_enbl

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_pulse_curve_mapping():
    """Get mapping from pulsed magnet to pulse curve file names

    Returns dict.
    """
    mapping = {}
    mapping[_dipk_pm] = _dipk_pc
    mapping[_nlk_pm ] = _nlk_pc

    return mapping
