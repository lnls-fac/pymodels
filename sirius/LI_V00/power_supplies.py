"""Magnet to power supply mapping definitions"""

from . import families as _families
from . import device_names as _device_names


def get_magnet_mapping(accelerator):
    """Get mapping from power supply to magnet names and inverse mapping

    Returns mapping, inverse_mapping.
    """
    family_data = _families.get_family_data(accelerator)

    mapping = dict()
    inverse_mapping = dict()

    return mapping, inverse_mapping
