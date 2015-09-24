"""Magnet to power supply mapping definitions"""

import re as _re
from . import families as _families
from . import record_names as _record_names


_name_split_char = '-'


def get_magnet_mapping(accelerator):
    """Get mapping from power supply to magnet names and inverse mapping

    Returns mapping, inverse_mapping.
    """
    family_data = _families.get_family_data(accelerator)

    mapping = dict()
    inverse_mapping = dict()

    return mapping, inverse_mapping
