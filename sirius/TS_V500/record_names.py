
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
        subsystems = ['tsdi', 'tsps', 'tspu', 'tsti']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(family_data, subsystem))
        return record_names_dict

    if subsystem.lower() == 'tsdi':
        prefix = 'TSDI-'
        _dict = get_element_names(family_data, element = 'bpm', prefix = prefix)
        _dict.update(get_family_names(family_data, family = 'bpm', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tsps':
        prefix = 'TSPS-'

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'hcm', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'vcm', prefix = prefix))
        return _dict

    if subsystem.lower() == 'tspu':
        prefix = 'TSPU-'
        _dict = get_element_names(family_data, element = 'septa', prefix = prefix)
        return _dict

    if subsystem.lower() == 'tsma':
        prefix = 'TSMA-'

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'hcm',  prefix = prefix))
        _dict.update(get_element_names(family_data, element = 'vcm',  prefix = prefix))
        return _dict

    if subsystem.lower() == 'tspm':
        prefix = 'TSPM-'
        _dict = get_element_names(family_data, element = 'sep', prefix = prefix)
        return _dict

    if subsystem.lower() == 'tsti':
        _dict = {
                'TSTI-SEPTUMTHICK-ENABLED':{},
                'TSTI-SEPTUMTHICK-DELAY':{},
                'TSTI-SEPTUMTHIN-ENABLED':{},
                'TSTI-SEPTUMTHIN-DELAY':{},
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
            prefix + 'BEND-01' : {'bend' :  family_data['bend']['index'][0]},
            prefix + 'BEND-02' : {'bend' : [family_data['bend']['index'][1]]},
            prefix + 'BEND-03' : {'bend' : [family_data['bend']['index'][2]]},
        }
        return _dict

    if element.lower() == 'septa' or element.lower() == 'sep':
        _dict ={
            prefix + 'SEPTUMEXT-01'   : {'septex'  :  family_data['septex']['index']},
            prefix + 'SEPTUMTHICK-04' : {'septing' : [family_data['septing']['index'][0]]},
            prefix + 'SEPTUMTHIN-04'  : {'septinf' : [family_data['septinf']['index'][0]]},
        }
        return _dict

    if element.lower() == 'quad':
        #elements = _families.families_quadrupoles()
        _dict = {
            prefix + 'QF1A-01' : {'qf1a': family_data['qf1a']['index']},
            prefix + 'QF1B-01' : {'qf1b': family_data['qf1b']['index']},
            prefix + 'QD2-02'  : {'qd2' : family_data['qd2']['index']},
            prefix + 'QF2-02'  : {'qf2' : family_data['qf2']['index']},
            prefix + 'QD3-03'  : {'qd3' : family_data['qd3']['index']},
            prefix + 'QF3-03'  : {'qf3' : family_data['qf3']['index']},
            prefix + 'QD4A-04' : {'qd4a': family_data['qd4a']['index']},
            prefix + 'QF4-04'  : {'qf4' : family_data['qf4']['index']},
            prefix + 'QD4B-04' : {'qd4b': family_data['qd4b']['index']},
        }
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
            prefix + 'BPM-01'   : {'bpm' : [indices[0]]},
            prefix + 'BPM-02'   : {'bpm' : [indices[1]]},
            prefix + 'BPM-03'   : {'bpm' : [indices[2]]},
            prefix + 'BPM-04-A' : {'bpm' : [indices[3]]},
            prefix + 'BPM-04-B' : {'bpm' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'hcm':
        indices = family_data['hcm']['index']
        _dict = {
            prefix + 'CH-01'   : {'hcm' : [indices[0]]},
            prefix + 'CH-02'   : {'hcm' : [indices[1]]},
            prefix + 'CH-03'   : {'hcm' : [indices[2]]},
            prefix + 'CH-04'   : {'hcm' : [indices[3]]},
        }
        return _dict

    if element.lower() == 'vcm':
        indices = family_data['vcm']['index']
        _dict = {
            prefix + 'CV-01-A' : {'vcm' : [indices[0]]},
            prefix + 'CV-01-B' : {'vcm' : [indices[1]]},
            prefix + 'CV-02'   : {'vcm' : [indices[2]]},
            prefix + 'CV-03'   : {'vcm' : [indices[3]]},
            prefix + 'CV-04-A' : {'vcm' : [indices[4]]},
            prefix + 'CV-04-B' : {'vcm' : [indices[5]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_record_names(accelerator, 'tsma')
    _dict.update(get_record_names(accelerator, 'tspm'))
    return _dict
