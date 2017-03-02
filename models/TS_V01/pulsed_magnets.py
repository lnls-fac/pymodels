
from . import device_names as _device_names
import sirius.naming_system as _naming_system

_system  = 'ts'
_trigger_delay = 'TrigDelay'
_trigger_enabled = 'TrigEnbl'
_pulsed_magnet_mapping = {}

def _add_to_pulsed_magnet_mapping(pulsed_magnet_name, timing_device_name, pulse_curve_name, channel):
    _pulsed_magnet_mapping[pulsed_magnet_name] = {
        'delay'   : timing_device_name + ":" + _trigger_delay + channel,
        'enabled' : timing_device_name + ":" + _trigger_enabled + channel,
        'pulse_curve' : pulse_curve_name,
    }

# SEPTUMEXT
_pulsed_magnet_name = _naming_system.join_name(_system, 'PM', 'SEPTUMEXT', '01')
_timing_device_name = _naming_system.join_name(_system, 'TI', 'STDMOE',  '01')
_pulse_curve_name  = 'tspm-septex-pulse.txt'
_channel = 'Ch03'
_add_to_pulsed_magnet_mapping(_pulsed_magnet_name, _timing_device_name, _pulse_curve_name, _channel)

# SEPTUMTHICK
_pulsed_magnet_name = _naming_system.join_name(_system, 'PM', 'SEPTUMTHICK', '04')
_timing_device_name = _naming_system.join_name(_system, 'TI', 'SOE', '04')
_pulse_curve_name  = 'tspm-septin-pulse.txt'
_channel = 'Ch03'
_add_to_pulsed_magnet_mapping(_pulsed_magnet_name, _timing_device_name, _pulse_curve_name, _channel)

# SEPTUMTHIN
_pulsed_magnet_name = _naming_system.join_name(_system, 'PM', 'SEPTUMTHIN', '04')
_timing_device_name = _naming_system.join_name(_system, 'TI', 'SOE', '04')
_pulse_curve_name  = 'tspm-septin-pulse.txt'
_channel = 'Ch04'
_add_to_pulsed_magnet_mapping(_pulsed_magnet_name, _timing_device_name, _pulse_curve_name, _channel)

def get_magnet_delay_mapping():
    """Get mapping from pulsed magnet to timing delay

    Returns dict.
    """
    mapping = {}
    for key in _pulsed_magnet_mapping:
        mapping[key] = _pulsed_magnet_mapping[key]['delay']

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_magnet_enabled_mapping():
    """Get mapping from pulsed magnet to timing enabled

    Returns dict.
    """
    mapping = {}
    for key in _pulsed_magnet_mapping:
        mapping[key] = _pulsed_magnet_mapping[key]['enabled']

    inverse_mapping = dict()
    for key, value in mapping.items():
        inverse_mapping[value] = key

    return mapping, inverse_mapping


def get_pulse_curve_mapping():
    """Get mapping from pulsed magnet to pulse curve file names

    Returns dict.
    """
    mapping = {}
    for key in _pulsed_magnet_mapping:
        mapping[key] = _pulsed_magnet_mapping[key]['pulse_curve']

    return mapping
