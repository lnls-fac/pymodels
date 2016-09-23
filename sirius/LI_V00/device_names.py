
from . import families as _families

system = 'li'

_pvnaming_rule = 2 # 1 : PV Naming Proposal#1; 2 : PV Naming Proposal#2
_pvnaming_glob = 'Glob'
_pvnaming_fam  = 'Fam'

def join_name(system, subsystem, device, sector, idx = None):
    # Proposal 1
    if _pvnaming_rule == 1:
        if idx is not None:
            name = system.upper() + '-' + subsystem.upper() + ':' + device + '-' + sector + '-' + idx
        else:
            name = system.upper() + '-' + subsystem.upper() + ':' + device + '-' + sector
        return name

    # Proposal 2
    elif _pvnaming_rule == 2:
        if idx is not None:
            name = system.upper() + '-' + sector + ':' + subsystem.upper() + '-' + device + '-' + idx
        else:
            name = system.upper() + '-' + sector + ':' + subsystem.upper() + '-' + device
        return name

    else:
        raise Exception('Device name specification not found.')

def split_name(name):
    name_list = [s.split(':') for s in name.split('-')]
    name_list = [y for x in name_list for y in x]
    name_dict = {}

    # Proposal 1
    if _pvnaming_rule == 1:
        name_dict['system']    = name_list[0]
        name_dict['subsystem'] = name_list[1]
        name_dict['device']    = name_list[2]
        name_dict['sector']    = name_list[3]
        if len(name_list) >= 5:
            name_dict['idx']  = name_list[4]
        return name_dict

    # Proposal 2
    elif _pvnaming_rule == 2:
        name_dict['system']    = name_list[0]
        name_dict['sector']    = name_list[1]
        name_dict['subsystem'] = name_list[2]
        name_dict['device']    = name_list[3]
        if len(name_list) >= 5:
            name_dict['idx']  = name_list[4]
        return name_dict

    else:
        raise Exception('Device name specification not found.')


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
        subsystems = ['ti']
        device_names_dict = {}
        for subsystem in subsystems:
            device_names_dict.update(get_device_names(family_data, subsystem))
        return device_names_dict

    if subsystem.lower() == 'ti':
        _dict = {
            join_name(system, subsystem, 'STDMOE', 'EGUN') : {},
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
