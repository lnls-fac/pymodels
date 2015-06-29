"""Magnet to power supply mapping definitions"""

import re as _re
from . import record_names as _record_names


_name_split_char = '-'


def get_magnet_mapping():
    """Get mapping from power supply to magnet names and inverse mapping

    Returns mapping, inverse_mapping.
    """
    magnet_prefix = 'BOMA-'
    ps_prefix = 'BOPS-'
    mapping = dict()

    # Add family power supplies
    bend_magnets = _record_names.get_element_names('bend', magnet_prefix)
    bend_family = _record_names.get_family_names('bend', ps_prefix)
    bend_family_name = list(bend_family.keys())[0]
    for magnet_name in bend_magnets.keys():
        if _re.match('SIMA-BC-.*', magnet_name) is None:
            s = set()
            s.add(bend_family_name)
            mapping[magnet_name] = s

    quad_magnets = _record_names.get_element_names('quad', magnet_prefix)
    quad_families = _record_names.get_family_names('quad', ps_prefix)
    for family_name in quad_families.keys():
        element_name = family_name[5:-4]
        for magnet_name in quad_magnets.keys():
            template = magnet_prefix + element_name + '.*'
            if _re.match(template, magnet_name) is not None:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    sext_magnets = _record_names.get_element_names('sext', magnet_prefix)
    sext_families = _record_names.get_family_names('sext', ps_prefix)
    for family_name in sext_families.keys():
        element_name = family_name[5:-4]
        for magnet_name in sext_magnets.keys():
            template = magnet_prefix + element_name + '.*'
            if _re.match(template, magnet_name) is not None:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    # Add individual power supplies
    magnets = _record_names.get_record_names('boma')
    magnet_names = magnets.keys()
    pss = _record_names.get_record_names('bops')
    for ps_name in pss.keys():
        ps_magnet_name = ps_name.replace('BOPS', 'BOMA')
        if ps_magnet_name in magnet_names:
            if ps_magnet_name in mapping:
                mapping[ps_magnet_name].add(ps_name)
            else:
                s = set()
                s.add(ps_name)
                mapping[ps_magnet_name] = s

    inverse_mapping = dict()
    for item in mapping.items():
        key, value = item
        for v in value:
            if v in inverse_mapping:
                inverse_mapping[v].add(key)
            else:
                s = set()
                s.add(key)
                inverse_mapping[v] = s

    return mapping, inverse_mapping
