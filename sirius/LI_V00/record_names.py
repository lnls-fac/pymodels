
from . import families as _families


def get_record_names(subsystem=None):
    """Return a dictionary of record names for given subsystem
    each entry is another dictionary of model families whose
    values are the indices in the pyaccel model of the magnets
    that belong to the family. The magnet models ca be segmented,
    in which case the value is a python list of lists."""

    if subsystem == None:
        subsystems = ['liti']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(subsystem))
        return record_names_dict

    if subsystem.lower() == 'liti':
        _dict = {
                'LITI-CYCLE':{},
                'LITI-EGUN-ENABLED':{},
                'LITI-EGUN-DELAY':{},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)

def get_family_names(family=None, prefix=''):
    _dict = {}
    return _dict


def get_element_names(element=None, prefix=''):
    _dict = {}
    return _dict


def get_magnet_names():
    _dict = {}
    return _dict

def get_pulsed_magnet_names():
    _dict = {}
    return _dict
