"""Magnet to power supply mapping definitions"""

import re as _re
from . import record_names as _record_names


_name_split_char = '-'


def get_magnet_mapping():
    """Get mapping from power supply to magnet names and inverse mapping

    Returns mapping, inverse_mapping.
    """
    mapping = dict()
    inverse_mapping = dict()
    
    return mapping, inverse_mapping
