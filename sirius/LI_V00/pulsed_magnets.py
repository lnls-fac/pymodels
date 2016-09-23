
from . import device_names as _device_names


def get_pulse_curve_mapping(accelerator):
    """Get mapping from pulsed magnet to pulse curve file names

    Returns dict.
    """
    pc = dict()
    return pc

def get_magnet_delay_mapping(accelerator):
    """Get mapping from pulsed magnet to timing delay

    Returns dict.
    """
    mapping = dict()
    inverse_mapping = dict()
    return mapping, inverse_mapping


def get_magnet_enabled_mapping(accelerator):
    """Get mapping from pulsed magnet to timing enabled

    Returns dict.
    """
    mapping = dict()
    inverse_mapping = dict()
    return mapping, inverse_mapping
