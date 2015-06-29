
from . import families as _families

def get_record_names(subsystem = None):
    """Return a dictionary of record names for given subsystem
    each entry is another dictionary of model families whose
    values are the indices in the pyaccel model of the magnets
    that belong to the family. The magnet models ca be segmented,
    in which case the value is a python list of lists."""

    family_data = _families._family_data

    if subsystem == None:
        subsystems = ['tsdi', 'tsps', 'tspu']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(subsystem))
        return record_names_dict

    if subsystem.lower() == 'tsdi':
        prefix = 'TSDI-'
        _dict = get_element_names(element = 'bpm', prefix = prefix)
        _dict.update(get_family_names(family = 'bpm', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tsps':
        prefix = 'TSPS-'

        _dict ={}
        _dict.update(get_element_names(element = 'bend', prefix = prefix))
        _dict.update(get_element_names(element = 'quad', prefix = prefix))
        _dict.update(get_element_names(element = 'ch', prefix = prefix))
        _dict.update(get_element_names(element = 'cv', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tspu':
        prefix = 'TSPU-'
        _dict = get_element_names(element = 'sep', prefix = prefix)
        return _dict

    if subsystem.lower() == 'tsma':
        prefix = 'TSMA-'

        _dict ={}
        _dict.update(get_element_names(element = 'bend', prefix = prefix))
        _dict.update(get_element_names(element = 'quad', prefix = prefix))
        _dict.update(get_element_names(element = 'ch', prefix = prefix))
        _dict.update(get_element_names(element = 'cv', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tspm':
        prefix = 'TSPM-'
        _dict = get_element_names(element = 'sep', prefix = prefix)
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(family = None, prefix = ''):

    family_data = _families._family_data

    if family == None:
        family_names = ['bpm']

        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family, prefix = prefix))
        return _dict

    if family.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {prefix + 'BPM-FAM-X': {'bpm': indices},
                 prefix + 'BPM-FAM-Y': {'bpm': indices}
                }
        return _dict

    else:
        raise Exception('Family name %s not found'%family)


def get_element_names(element = None, prefix = ''):

    family_data = _families._family_data

    if element == None:
        elements = []
        elements += _families.families_dipoles()
        elements += _families.families_septa()
        elements += _families.families_quadrupoles()
        elements += _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(element, prefix = prefix))
        return _dict

    if element.lower() == 'bend':
        _dict = {
            prefix + 'BEND-01' : {'bf ' :  family_data['bf']['index']},
            prefix + 'BEND-02' : {'bd ' : [family_data['bd']['index'][0]]},
            prefix + 'BEND-03' : {'bd ' : [family_data['bd']['index'][1]]},
        }
        return _dict

    if element.lower() == 'sep':
        _dict ={
            prefix + 'SEPEX-01'   : {'seb' :  family_data['seb']['index']},
            prefix + 'SEPINTK-04' : {'seg' : [family_data['seg']['index'][0]]},
            prefix + 'SEPINTN-04' : {'sef' : [family_data['sef']['index'][0]]},
        }
        return _dict

    if element.lower() == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(element, prefix = prefix))
        return _dict

    if element.lower() == 'corr':
        elements = _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(element, prefix = prefix))
        return _dict

    if element.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            prefix + 'BPM-01'   : {'bpm' : [indices[0]]},
            prefix + 'BPM-02'   : {'bpm' : [indices[1]]},
            prefix + 'BPM-03'   : {'bpm' : [indices[2]]},
            prefix + 'BPM-04-A' : {'bpm' : [indices[3]]},
            prefix + 'BPM-04-B' : {'bpm' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'qf':
        indices = family_data['qf']['index']
        _dict = {
            prefix + 'QF-01'   : {'qf' : [indices[0]]},
            prefix + 'QF-03-A' : {'qf' : [indices[1]]},
            prefix + 'QF-03-B' : {'qf' : [indices[2]]},
            prefix + 'QF-04-A' : {'qf' : [indices[3]]},
            prefix + 'QF-04-B' : {'qf' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'qd':
        indices = family_data['qd']['index']
        _dict = {
            prefix + 'QD-01'   : {'qd' : [indices[0]]},
            prefix + 'QD-02'   : {'qd' : [indices[1]]},
            prefix + 'QD-04-A' : {'qd' : [indices[2]]},
            prefix + 'QD-04-B' : {'qd' : [indices[3]]},
        }
        return _dict

    if element.lower() == 'ch':
        indices = family_data['ch']['index']
        _dict = {
            prefix + 'CH-01'   : {'ch' : [indices[0]]},
            prefix + 'CH-02'   : {'ch' : [indices[1]]},
            prefix + 'CH-03'   : {'ch' : [indices[2]]},
            prefix + 'CH-04'   : {'ch' : [indices[3]]},
        }
        return _dict

    if element.lower() == 'cv':
        indices = family_data['cv']['index']
        _dict = {
            prefix + 'CV-01-A' : {'cv' : [indices[0]]},
            prefix + 'CV-01-B' : {'cv' : [indices[1]]},
            prefix + 'CV-02'   : {'cv' : [indices[2]]},
            prefix + 'CV-03'   : {'cv' : [indices[3]]},
            prefix + 'CV-04-A' : {'cv' : [indices[4]]},
            prefix + 'CV-04-B' : {'cv' : [indices[5]]},
        }
        return _dict

    if element.lower() == 'bf':
        _dict = {
            prefix + 'BEND-01' : {'bf ' :  family_data['bf']['index']},
        }
        return _dict

    if element.lower() == 'bd':
        _dict = {
            prefix + 'BEND-02' : {'bd ' : [family_data['bd']['index'][0]]},
            prefix + 'BEND-03' : {'bd ' : [family_data['bd']['index'][1]]},
        }
        return _dict

    if element.lower() == 'seb':
        _dict ={
            prefix + 'SEPEX-01'   : {'seb' :  family_data['seb']['index']},
        }
        return _dict

    if element.lower() == 'seg':
        _dict ={
            prefix + 'SEPINTK-04' : {'seg' : [family_data['seg']['index'][0]]},
        }
        return _dict

    if element.lower() == 'sef':
        _dict ={
            prefix + 'SEPINTN-04' : {'sef' : [family_data['sef']['index'][0]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)
