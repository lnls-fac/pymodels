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

    system = 'BO'
    ma_subsystem = 'MA'
    ps_subsystem = 'PS'
    mapping = dict()

    # Add family power supplies
    bend_magnets = _device_names.get_element_names(family_data, ma_subsystem, 'bend')
    bend_family  = _device_names.get_family_names(family_data, ps_subsystem, 'bend')
    family_list = []
    for family_name in bend_families.keys():
        family_list.append(family_name)
    for magnet_name in bend_magnets.keys():
        mapping[magnet_name] = set(family_list)

    quad_magnets = _device_names.get_element_names(family_data, ma_subsystem, 'quad')
    quad_families = _device_names.get_family_names(family_data, ps_subsystem, 'quad')
    for family_name in quad_families.keys():
        element_name = _device_names.split_name(family_name)['device']
        for magnet_name in quad_magnets.keys():
            if  _device_names.split_name(magnet_name)['device'] ==  element_name:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    sext_magnets = _device_names.get_element_names(family_data, ma_subsystem, 'sext')
    sext_families = _device_names.get_family_names(family_data, ps_subsystem, 'sext')
    for family_name in sext_families.keys():
        element_name = _device_names.split_name(family_name)['device']
        for magnet_name in sext_magnets.keys():
            if  _device_names.split_name(magnet_name)['device'] ==  element_name:
                s = set()
                s.add(family_name)
                mapping[magnet_name] = s

    # Add individual power supplies
    magnets = _device_names.get_device_names(family_data, 'ma')
    magnet_names = magnets.keys()
    pss = _device_names.get_device_names(family_data, 'ps')
    for ps_name in pss.keys():
        ps_magnet_name = ps_name.replace('PS', 'MA')
        if ps_magnet_name in magnet_names:
            if ps_magnet_name in mapping:
                mapping[ps_magnet_name].add(ps_name)
            else:
                s = set()
                s.add(ps_name)
                mapping[ps_magnet_name] = s

    # Add pulsed power supplies
    pulsed_magnets = _device_names.get_device_names(family_data, 'pm')
    pulsed_magnet_names = pulsed_magnets.keys()
    pulsed_pss = _device_names.get_device_names(family_data, 'pu')
    for pu_name in pulsed_pss.keys():
        pu_magnet_name = pu_name.replace('PU', 'PM')
        if pu_magnet_name in pulsed_magnet_names:
            if pu_magnet_name in mapping:
                mapping[pu_magnet_name].add(pu_name)
            else:
                s = set()
                s.add(pu_name)
                mapping[pu_magnet_name] = s


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
