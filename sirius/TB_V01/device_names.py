
from . import families as _families


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
        subsystems = ['tbdi', 'tbps', 'tbpu', 'tbti', 'tbpa']
        device_names_dict = {}
        for subsystem in subsystems:
            device_names_dict.update(get_device_names(family_data, subsystem))
        return device_names_dict

    if subsystem.lower() == 'tbpa':
        _dict = {
            'TBPA-INJEFF':{},
            'TBPA-EXTEFF':{},
        }
        return _dict

    if subsystem.lower() == 'tbdi':
        prefix = 'TBDI-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'bpm', prefix=prefix, suffix=suffix)
        _dict.update(get_family_names(family_data, family = 'bpm', prefix=prefix, suffix=suffix))
        return _dict

    if subsystem.lower() == 'tbps':
        prefix = 'TBPS-'
        suffix = ''

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'quad',prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'corr', prefix=prefix, suffix=suffix))
        return _dict

    if subsystem.lower() == 'tbpu':
        prefix = 'TBPU-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'sep', prefix=prefix, suffix=suffix)
        return _dict

    if subsystem.lower() == 'tbma':
        prefix = 'TBMA-'
        suffix = ''

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'corr', prefix=prefix, suffix=suffix))
        return _dict

    if subsystem.lower() == 'tbpm':
        prefix = 'TBPM-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'sep', prefix=prefix, suffix=suffix)
        return _dict

    if subsystem.lower() == 'tbti':
        _dict = {
                'TBTI-SEPTUMINJ-ENABLED':{},
                'TBTI-SEPTUMINJ-DELAY':{},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(accelerator, family = None, prefix='', suffix=''):

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    if family == None:
        family_names = ['bpm']

        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix=prefix, suffix=suffix))
        return _dict

    if family.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {prefix + 'BPM-FAM' + suffix : {'bpm': indices}}
        return _dict

    else:
        raise Exception('Family name %s not found'%family)


def get_element_names(accelerator, element = None, prefix='', suffix=''):

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
        elements += _families.families_septa()
        elements += _families.families_quadrupoles()
        elements += _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'bend':
        _dict = {
            prefix + 'BEND-01' + suffix : {'bend' :  family_data['spec']['index']},
            prefix + 'BEND-02' + suffix : {'bend' :  family_data['bn']['index']},
            prefix + 'BEND-03' + suffix : {'bend' : [family_data['bp']['index'][0]]},
            prefix + 'BEND-04' + suffix : {'bend' : [family_data['bp']['index'][1]]},
        }
        return _dict

    if element.lower() == 'quad':
        _dict = {}
        _dict.update(get_element_names(family_data, 'qd', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, 'qf', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, 'triplet', prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'sep':
        _dict ={
            prefix + 'SEPIN-05' + suffix : {'sep' : family_data['sep']['index']},
        }
        return _dict

    if element.lower() == 'corr':
        elements = _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            prefix + 'BPM-02-A' + suffix : {'bpm' : [indices[0]]},
            prefix + 'BPM-02-B' + suffix : {'bpm' : [indices[1]]},
            prefix + 'BPM-03-A' + suffix : {'bpm' : [indices[2]]},
            prefix + 'BPM-03-B' + suffix : {'bpm' : [indices[3]]},
            prefix + 'BPM-04'   + suffix : {'bpm' : [indices[4]]},
            prefix + 'BPM-05'   + suffix : {'bpm' : [indices[5]]},
        }
        return _dict

    if element.lower() == 'qf':
        indices = family_data['qf']['index']
        _dict = {
            prefix + 'QF-02'   + suffix : {'qf' : [indices[0]]},
            prefix + 'QF-03-A' + suffix : {'qf' : [indices[1]]},
            prefix + 'QF-03-B' + suffix : {'qf' : [indices[2]]},
            prefix + 'QF-04'   + suffix : {'qf' : [indices[3]]},
            prefix + 'QF-05'   + suffix : {'qf' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'qd':
        indices = family_data['qd']['index']
        _dict = {
            prefix + 'QD-02'   + suffix : {'qd' : [indices[0]]},
            prefix + 'QD-03-A' + suffix : {'qd' : [indices[1]]},
            prefix + 'QD-03-B' + suffix : {'qd' : [indices[2]]},
            prefix + 'QD-04'   + suffix : {'qd' : [indices[3]]},
            prefix + 'QD-05'   + suffix : {'qd' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'triplet':
        indices = family_data['triplet']['index']
        _dict = {
            prefix + 'Q1A-01-A' + suffix : {'triplet': [indices[0]]},
            prefix + 'Q1B-01'   + suffix : {'triplet': [indices[1]]},
            prefix + 'Q1A-01-B' + suffix : {'triplet': [indices[2]]},
            prefix + 'Q1C-01'   + suffix : {'triplet': [indices[3]]},
        }
        return _dict

    if element.lower() == 'ch' or element.lower() == 'hcm':
        indices = family_data['ch']['index']
        _dict = {
            prefix + 'CH-02-A' + suffix : {'ch' : [indices[0]]},
            prefix + 'CH-02-B' + suffix : {'ch' : [indices[1]]},
            prefix + 'CH-03-A' + suffix : {'ch' : [indices[2]]},
            prefix + 'CH-03-B' + suffix : {'ch' : [indices[3]]},
            prefix + 'CH-04'   + suffix : {'ch' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'cv' or element.lower() == 'vcm':
        indices = family_data['cv']['index']
        _dict = {
            prefix + 'CV-02-A' + suffix : {'cv' : [indices[0]]},
            prefix + 'CV-02-B' + suffix : {'cv' : [indices[1]]},
            prefix + 'CV-03-A' + suffix : {'cv' : [indices[2]]},
            prefix + 'CV-03-B' + suffix : {'cv' : [indices[3]]},
            prefix + 'CV-05-A' + suffix : {'cv' : [indices[4]]},
            prefix + 'CV-05-B' + suffix : {'cv' : [indices[5]]},
        }
        return _dict
    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_device_names(accelerator, 'tbma')
    _dict.update(get_device_names(accelerator, 'tbpm'))
    return _dict
