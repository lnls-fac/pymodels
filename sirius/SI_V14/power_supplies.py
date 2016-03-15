"""Magnet to power supply mapping definitions"""

import re as _re
from . import families as _families
from . import device_names as _device_names


_name_split_char = '-'


def get_magnet_mapping(accelerator):
    """Get mapping from power supply to magnet names and inverse mapping

    Returns mapping, inverse_mapping.
    """
    family_data = _families.get_family_data(accelerator)

    magnet_prefix = 'SIMA-'
    ps_prefix = 'SIPS-'
    mapping = dict()

    # Add family power supplies
    bend_magnets = _device_names.get_element_names(family_data, 'bend', magnet_prefix)
    bend_family = _device_names.get_family_names(family_data, 'bend', ps_prefix)
    bend_family_name = list(bend_family.keys())[0]
    for magnet_name in bend_magnets.keys():
        if _re.match('SIMA-BC-.*', magnet_name) is None:
            s = set()
            s.add(bend_family_name)
            mapping[magnet_name] = s

    quad_magnets = _device_names.get_element_names(family_data, 'quad', magnet_prefix)
    quad_families = _device_names.get_family_names(family_data, 'quad', ps_prefix)
    for family_name in quad_families.keys():
        element_name = family_name[5:-4]
        for magnet_name in quad_magnets.keys():
            template = magnet_prefix + element_name + '.*'
            if _re.match(template, magnet_name) is not None:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    sext_magnets = _device_names.get_element_names(family_data, 'sext', magnet_prefix)
    sext_families = _device_names.get_family_names(family_data, 'sext', ps_prefix)
    for family_name in sext_families.keys():
        element_name = family_name[5:-4]
        for magnet_name in sext_magnets.keys():
            template = magnet_prefix + element_name + '.*'
            if _re.match(template, magnet_name) is not None:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    # Add individual power supplies
    magnets = _device_names.get_device_names(family_data, 'sima')
    magnet_names = magnets.keys()
    pss = _device_names.get_device_names(family_data, 'sips')
    for ps_name in pss.keys():
        ps_magnet_name = ps_name.replace('SIPS', 'SIMA')
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
