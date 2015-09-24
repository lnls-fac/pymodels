
from . import families as _families


def get_record_names(accelerator, subsystem = None):
    """Return a dictionary of record names for given subsystem
    each entry is another dictionary of model families whose
    values are the indices in the pyaccel model of the magnets
    that belong to the family. The magnet models ca be segmented,
    in which case the value is a python list of lists."""

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    if subsystem == None:
        subsystems = ['tbdi', 'tbps', 'tbpu', 'tbti']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(family_data, subsystem))
        return record_names_dict

    if subsystem.lower() == 'tbdi':
        prefix = 'TBDI-'
        _dict = get_element_names(family_data, element = 'bpm', prefix = prefix)
        _dict.update(get_family_names(family_data, family = 'bpm', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tbps':
        prefix = 'TBPS-'

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'ch', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'cv', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tbpu':
        prefix = 'TBPU-'
        _dict = get_element_names(family_data, element = 'sep', prefix = prefix)
        return _dict

    if subsystem.lower() == 'tbma':
        prefix = 'TBMA-'

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'ch', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'cv', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tbpm':
        prefix = 'TBPM-'
        _dict = get_element_names(family_data, element = 'sep', prefix = prefix)
        return _dict

    if subsystem.lower() == 'tbti':
        _dict = {
                'TBTI-SEPTUMINJ-ENABLED':{},
                'TBTI-SEPTUMINJ-DELAY':{},
                'TBTI-SEPTUMEX-ENABLED':{},
                'TBTI-SEPTUMEX-DELAY':{},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(accelerator, family = None, prefix = ''):

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    if family == None:
        family_names = ['bpm']

        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix = prefix))
        return _dict

    if family.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {prefix + 'BPM-FAM-X': {'bpm': indices},
                 prefix + 'BPM-FAM-Y': {'bpm': indices}
                }
        return _dict

    else:
        raise Exception('Family name %s not found'%family)


def get_element_names(accelerator, element = None, prefix = ''):

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

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
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'bend':
        _dict = {
            prefix + 'BEND-01' : {'bend' :  family_data['bspec']['index']},
            prefix + 'BEND-02' : {'bend' :  family_data['bn']['index']},
            prefix + 'BEND-03' : {'bend' : [family_data['bp']['index'][0]]},
            prefix + 'BEND-04' : {'bend' : [family_data['bp']['index'][1]]},
        }
        return _dict

    if element.lower() == 'sep':
        _dict ={
            prefix + 'SEPIN-05' : {'sep' : family_data['sep']['index']},
        }
        return _dict

    if element.lower() == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'corr':
        elements = _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            prefix + 'BPM-02'   : {'bpm' : [indices[0]]},
            prefix + 'BPM-03-A' : {'bpm' : [indices[1]]},
            prefix + 'BPM-03-B' : {'bpm' : [indices[2]]},
            prefix + 'BPM-04'   : {'bpm' : [indices[3]]},
            prefix + 'BPM-05'   : {'bpm' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'qf':
        indices = family_data['qf']['index']
        _dict = {
            prefix + 'QF-01-A' : {'qf' : [indices[0]]},
            prefix + 'QF-01-B' : {'qf' : [indices[1]]},
            prefix + 'QF-02'   : {'qf' : [indices[2]]},
            prefix + 'QF-03-A' : {'qf' : [indices[3]]},
            prefix + 'QF-03-B' : {'qf' : [indices[4]]},
            prefix + 'QF-04'   : {'qf' : [indices[5]]},
            prefix + 'QF-05'   : {'qf' : [indices[6]]},
        }
        return _dict

    if element.lower() == 'qd':
        indices = family_data['qd']['index']
        _dict = {
            prefix + 'QD-01'   : {'qd' : [indices[0],indices[1]]},
            prefix + 'QD-02'   : {'qd' : [indices[2]]},
            prefix + 'QD-03'   : {'qd' : [indices[3]]},
            prefix + 'QD-04'   : {'qd' : [indices[4]]},
            prefix + 'QD-05'   : {'qd' : [indices[5]]},
        }
        return _dict

    if element.lower() == 'ch':
        _dict = {
            prefix + 'CH-03': {'ch' : [family_data['ch']['index'][0]]},
        }
        return _dict

    if element.lower() == 'cv':
        indices = family_data['cv']['index']
        _dict = {
            prefix + 'CV-02-A' : {'cv' : [indices[0]]},
            prefix + 'CV-02-B' : {'cv' : [indices[1]]},
            prefix + 'CV-03-A' : {'cv' : [indices[2]]},
            prefix + 'CV-03-B' : {'cv' : [indices[3]]},
            prefix + 'CV-05-A' : {'cv' : [indices[4]]},
            prefix + 'CV-05-B' : {'cv' : [indices[5]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_record_names(accelerator, 'tbma')
    _dict.update(get_record_names(accelerator, 'tbpm'))
    return _dict
