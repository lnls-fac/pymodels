
from . import families as _families
import sirius.naming_system as _naming_system

system = 'li'
subsystems = ['ti']

def get_device_names(accelerator, subsystem = None):
    """Return a dictionary of device names for given subsystem
    each entry is another dictionary of model families whose
    values are the indices in the pyaccel model of the magnets
    that belong to the family. The magnet models ca be segmented,
    in which case the value is a python list of lists."""

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    if subsystem == None:
        device_names_dict = {}
        for subsystem in subsystems:
            device_names_dict.update(get_device_names(family_data, subsystem))
        return device_names_dict

    if subsystem.lower() == 'ti':
        _dict = {
            _naming_system.join_name(system, subsystem, 'STDMOE', 'EGun') : {},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(accelerator, subsystem, family = None):
    _dict = {}
    return _dict


def get_element_names(accelerator, subsystem, element = None):
    _dict = {}
    return _dict


def get_magnet_names(accelerator):
    _dict = {}
    return _dict
