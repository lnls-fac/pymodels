"""Magnet to power supply mapping definitions"""

import re as _re
from . import record_names as _record_names


_name_split_char = '-'


def get_magnet_mapping():
    """Get mapping from power supply to magnet names

    Returns dict.
    """
    prefix = 'SIMA-'
    mapping = dict()

    # Add family power supplies
    bend_family = _record_names.get_family_names('bend', prefix)
    bend_magnets = _record_names.get_element_names('bend', prefix)
    bend_family_name = list(bend_family.keys())[0]
    for magnet_name in bend_magnets.keys():
        s = set()
        s.add(bend_family_name)
        mapping[magnet_name] = s

    quad_families = _record_names.get_family_names('quad', prefix)
    quad_magnets = _record_names.get_element_names('quad', prefix)
    for family_name in quad_families.keys():
        family_prefix = family_name[:-4]
        for magnet_name in quad_magnets.keys():
            if _re.match(family_prefix+'.*', magnet_name) is not None:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    sext_families = _record_names.get_family_names('sext', prefix)
    sext_magnets = _record_names.get_element_names('sext', prefix)
    for family_name in sext_families.keys():
        family_prefix = family_name[:-4]
        for magnet_name in sext_magnets.keys():
            if _re.match(family_prefix+'.*', magnet_name) is not None:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    # Add individual power supplies
    magnets = _record_names.get_record_names('sima')
    magnet_names = magnets.keys()
    pss = _record_names.get_record_names('sips')
    for ps_name in pss.keys():
        ps_magnet_name = ps_name.replace('SIPS', 'SIMA')
        if ps_magnet_name in magnet_names:
            if ps_magnet_name in mapping:
                mapping[ps_magnet_name].add(ps_name)
            else:
                s = set()
                s.add(ps_name)
                mapping[ps_magnet_name] = s

    return mapping
