
from . import families as _families


def get_record_names(subsystem=None):
    """Return a dictionary of record names for given subsystem
    each entry is another dictionary of model families whose
    values are the indices in the pyaccel model of the magnets
    that belong to the family. The magnet models ca be segmented,
    in which case the value is a python list of lists."""
    _dict = {'LI-CO-MODE':{}}
    return _dict


def get_family_names(family=None, prefix=''):
    _dict = {}
    return _dict


def get_element_names(element=None, prefix=''):
    _dict = {}
    return _dict


def get_magnet_names():
    # return get_record_names('boma')
    _dict = {}
    return _dict

def get_pulsed_magnet_names():
    # return get_record_names('boma')
    _dict = {}
    return _dict
