
from . import families as _families
import sirius.naming_system as _naming_system

system = 'ts'
subsystems = ['di', 'ps', 'ti', 'pu', 'ma', 'pm']

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
            _naming_system.join_name(system, subsystem, 'SOE',    '04') : {},
            _naming_system.join_name(system, subsystem, 'STDMOE', '01') : {},
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
        _dict = {_naming_system.join_name(system, subsystem, family.upper(), _naming_system.pvnaming_fam): {family : indices}}
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

    if element.lower() == 'bend':
        _dict = {
            _naming_system.join_name(system, subsystem, element.upper(), '01') : {'bend' : [family_data['bend']['index'][0]]},
            _naming_system.join_name(system, subsystem, element.upper(), '02') : {'bend' : [family_data['bend']['index'][1]]},
            _naming_system.join_name(system, subsystem, element.upper(), '03') : {'bend' : [family_data['bend']['index'][2]]},
        }
        return _dict

    if element.lower() == 'pulsed_magnets':
        _dict ={
            _naming_system.join_name(system, subsystem, 'SEPTUMEXT',   '01') : {'septex'  : family_data['septex']['index'] },
            _naming_system.join_name(system, subsystem, 'SEPTUMTHICK', '04') : {'septing' : family_data['septing']['index']},
            _naming_system.join_name(system, subsystem, 'SEPTUMTHIN',  '04') : {'septinf' : family_data['septinf']['index']},
        }
        return _dict

    if element.lower() == 'quad':
        _dict = {
            _naming_system.join_name(system, subsystem, 'QF', '01', '1') : {'qf1a': family_data['qf1a']['index']},
            _naming_system.join_name(system, subsystem, 'QF', '01', '2') : {'qf1b': family_data['qf1b']['index']},
            _naming_system.join_name(system, subsystem, 'QD', '02' )     : {'qd2' : family_data['qd2']['index'] },
            _naming_system.join_name(system, subsystem, 'QF', '02' )     : {'qf2' : family_data['qf2']['index'] },
            _naming_system.join_name(system, subsystem, 'QF', '03' )     : {'qf3' : family_data['qf3']['index'] },
            _naming_system.join_name(system, subsystem, 'QD', '04', '1') : {'qd4a': family_data['qd4a']['index']},
            _naming_system.join_name(system, subsystem, 'QF', '04' )     : {'qf4' : family_data['qf4']['index'] },
            _naming_system.join_name(system, subsystem, 'QD', '04', '2') : {'qd4b': family_data['qd4b']['index']},
        }
        return _dict


    if element.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            _naming_system.join_name(system, subsystem, element.upper(), '01'  )    : {'bpm' : [indices[0]]},
            _naming_system.join_name(system, subsystem, element.upper(), '02'  )    : {'bpm' : [indices[1]]},
            _naming_system.join_name(system, subsystem, element.upper(), '03'  )    : {'bpm' : [indices[2]]},
            _naming_system.join_name(system, subsystem, element.upper(), '04', '1') : {'bpm' : [indices[3]]},
            _naming_system.join_name(system, subsystem, element.upper(), '04', '2') : {'bpm' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'ch':
        indices = family_data['ch']['index']
        _dict = {
            _naming_system.join_name(system, subsystem, element.upper(), '01') : {'ch' : [indices[0]]},
            _naming_system.join_name(system, subsystem, element.upper(), '02') : {'ch' : [indices[1]]},
            _naming_system.join_name(system, subsystem, element.upper(), '03') : {'ch' : [indices[2]]},
            _naming_system.join_name(system, subsystem, element.upper(), '04') : {'ch' : [indices[3]]},
        }
        return _dict

    if element.lower() == 'cv':
        indices = family_data['cv']['index']
        _dict = {
            _naming_system.join_name(system, subsystem, element.upper(), '01', '1') : {'cv' : [indices[0]]},
            _naming_system.join_name(system, subsystem, element.upper(), '01', '2') : {'cv' : [indices[1]]},
            _naming_system.join_name(system, subsystem, element.upper(), '02'  )    : {'cv' : [indices[2]]},
            _naming_system.join_name(system, subsystem, element.upper(), '03'  )    : {'cv' : [indices[3]]},
            _naming_system.join_name(system, subsystem, element.upper(), '04', '1') : {'cv' : [indices[4]]},
            _naming_system.join_name(system, subsystem, element.upper(), '04', '2') : {'cv' : [indices[5]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_device_names(accelerator, 'ma')
    _dict.update(get_device_names(accelerator, 'pm'))
    return _dict
