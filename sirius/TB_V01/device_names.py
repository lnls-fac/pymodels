
from . import families as _families

system = 'tb'

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
        subsystems = ['di', 'ps', 'ti', 'pu']
        device_names_dict = {}
        for subsystem in subsystems:
            device_names_dict.update(get_device_names(family_data, subsystem))
        return device_names_dict

    if subsystem.lower() == 'di':
        _dict = {}
        _dict.update(get_element_names(family_data, subsystem, element = 'bpm'))
        _dict.update(get_family_names(family_data, subsystem, family = 'bpm'))
        return _dict

    if subsystem.lower() == 'ps':
        _dict = {}
        _dict.update(get_element_names(family_data, subsystem, element = 'bend'))
        _dict.update(get_element_names(family_data, subsystem, element = 'quad'))
        _dict.update(get_element_names(family_data, subsystem, element = 'corr'))
        return _dict

    if subsystem.lower() == 'pu':
        _dict = get_element_names(family_data, subsystem, element='pulsed_magnets')
        return _dict

    if subsystem.lower() == 'ma':
        _dict = {}
        _dict.update(get_element_names(family_data, subsystem, element = 'bend'))
        _dict.update(get_element_names(family_data, subsystem, element = 'quad'))
        _dict.update(get_element_names(family_data, subsystem, element = 'corr'))
        return _dict

    if subsystem.lower() == 'pm':
        _dict = get_element_names(family_data, subsystem, element = 'pulsed_magnets')
        return _dict

    if subsystem.lower() == 'ti':
        _dict = {
            join_name(system, subsystem, 'SOE', '05') : {},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(accelerator, subsystem, family = None):

    try:
        family = family.lower()
    except:
        pass

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    start = family_data['start']['index'][0]
    if start != 0:
        for key in family_data.keys():
            if isinstance(family_data[key], dict):
                index = family_data[key]['index']
                j = 0
                for i in index:
                    if isinstance(i, int) and i < start: j+=1
                    elif isinstance(i, list) and i[0] < start: j+=1
                index = index[j:]+index[:j]
                family_data[key]['index'] = index

    family_names = ['bpm']

    if family == None:
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, subsystem, family))
        return _dict

    if family in family_names:
        indices = family_data[family]['index']
        _dict = {join_name(system, subsystem, family.upper(), _pvnaming_fam): {family : indices}}
        return _dict

    else:
        raise Exception('Family %s not found'%family)


def get_element_names(accelerator, subsystem, element = None):

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    start = family_data['start']['index'][0]
    if start != 0:
        for key in family_data.keys():
            if isinstance(family_data[key], dict):
                index = family_data[key]['index']
                j = 0
                for i in index:
                    if isinstance(i, int) and i < start: j+=1
                    elif isinstance(i, list) and i[0] < start: j+=1
                index = index[j:]+index[:j]
                family_data[key]['index'] = index

    if element == None:
        elements = []
        elements += _families.families_dipoles()
        elements += _families.families_quadrupoles()
        elements += _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        elements += _families.families_pulsed_magnets()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'corr':
        elements = _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'hcorr':
        elements = _families.families_horizontal_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'vcorr':
        elements = _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'bend':
        _dict = {
            join_name(system, subsystem, element.upper(),'01') : {'bend' :  family_data['spec']['index']},
            join_name(system, subsystem, element.upper(),'02') : {'bend' :  family_data['bn']['index']},
            join_name(system, subsystem, element.upper(),'03') : {'bend' : [family_data['bp']['index'][0]]},
            join_name(system, subsystem, element.upper(),'04') : {'bend' : [family_data['bp']['index'][1]]},
        }
        return _dict

    if element.lower() == 'pulsed_magnets':
        _dict ={
            join_name(system, subsystem, 'SEPTUMINJ' ,'05') : {'sep' : family_data['sep']['index']},
        }
        return _dict


    if element.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            join_name(system, subsystem, element.upper(),'02', '1') : {'bpm' : [indices[0]]},
            join_name(system, subsystem, element.upper(),'02', '2') : {'bpm' : [indices[1]]},
            join_name(system, subsystem, element.upper(),'03', '1') : {'bpm' : [indices[2]]},
            join_name(system, subsystem, element.upper(),'03', '2') : {'bpm' : [indices[3]]},
            join_name(system, subsystem, element.upper(),'04')      : {'bpm' : [indices[4]]},
            join_name(system, subsystem, element.upper(),'05')      : {'bpm' : [indices[5]]},
        }
        return _dict

    if element.lower() == 'qf':
        indices = family_data['qf']['index']
        _dict = {
            join_name(system, subsystem, element.upper(),'02'  )    : {'qf' : [indices[0]]},
            join_name(system, subsystem, element.upper(),'03', '1') : {'qf' : [indices[1]]},
            join_name(system, subsystem, element.upper(),'03', '2') : {'qf' : [indices[2]]},
            join_name(system, subsystem, element.upper(),'04'  )    : {'qf' : [indices[3]]},
            join_name(system, subsystem, element.upper(),'05'  )    : {'qf' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'qd':
        indices = family_data['qd']['index']
        _dict = {
            join_name(system, subsystem, element.upper(),'02'  )    : {'qd' : [indices[0]]},
            join_name(system, subsystem, element.upper(),'03', '1') : {'qd' : [indices[1]]},
            join_name(system, subsystem, element.upper(),'03', '2') : {'qd' : [indices[2]]},
            join_name(system, subsystem, element.upper(),'04'  )    : {'qd' : [indices[3]]},
            join_name(system, subsystem, element.upper(),'05'  )    : {'qd' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'triplet':
        indices = family_data['triplet']['index']
        _dict = {
            join_name(system, subsystem, 'Q1A', '01', '1')  : {'triplet': [indices[0]]},
            join_name(system, subsystem, 'Q1B', '01')       : {'triplet': [indices[1]]},
            join_name(system, subsystem, 'Q1A', '01', '2')  : {'triplet': [indices[2]]},
            join_name(system, subsystem, 'Q1C', '01')       : {'triplet': [indices[3]]},
        }
        return _dict

    if element.lower() == 'ch':
        indices = family_data['ch']['index']
        _dict = {
            join_name(system, subsystem, element.upper(),'02', '1') : {'ch' : [indices[0]]},
            join_name(system, subsystem, element.upper(),'02', '1') : {'ch' : [indices[1]]},
            join_name(system, subsystem, element.upper(),'03', '1') : {'ch' : [indices[2]]},
            join_name(system, subsystem, element.upper(),'03', '2') : {'ch' : [indices[3]]},
            join_name(system, subsystem, element.upper(),'04'  )    : {'ch' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'cv':
        indices = family_data['cv']['index']
        _dict = {
            join_name(system, subsystem, element.upper(),'02', '1') : {'cv' : [indices[0]]},
            join_name(system, subsystem, element.upper(),'02', '2') : {'cv' : [indices[1]]},
            join_name(system, subsystem, element.upper(),'03', '1') : {'cv' : [indices[2]]},
            join_name(system, subsystem, element.upper(),'03', '2') : {'cv' : [indices[3]]},
            join_name(system, subsystem, element.upper(),'05', '1') : {'cv' : [indices[4]]},
            join_name(system, subsystem, element.upper(),'05', '2') : {'cv' : [indices[5]]},
        }
        return _dict
    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_device_names(accelerator, 'ma')
    _dict.update(get_device_names(accelerator, 'pm'))
    return _dict
