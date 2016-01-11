
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
        subsystems = ['tsdi', 'tsps', 'tspu', 'tsti', 'tspa']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(family_data, subsystem))
        return record_names_dict

    if subsystem.lower() == 'tspa':
        _dict = {
            'TSPA-INJEFF':{},
            'TSPA-EXTEFF':{},
        }
        return _dict

    if subsystem.lower() == 'tsdi':
        prefix = 'TSDI-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'bpm', prefix=prefix, suffix=suffix)
        _dict.update(get_family_names(family_data, family = 'bpm', prefix=prefix, suffix='-X'))
        _dict.update(get_family_names(family_data, family = 'bpm', prefix=prefix, suffix='-Y'))
        return _dict

    if subsystem.lower() == 'tsps':
        prefix = 'TSPS-'
        suffix = ''

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'corr', prefix=prefix, suffix=suffix))
        return _dict

    if subsystem.lower() == 'tspu':
        prefix = 'TSPU-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'septa', prefix=prefix, suffix=suffix)
        return _dict

    if subsystem.lower() == 'tsma':
        prefix = 'TSMA-'
        suffix = ''

        _dict ={}
        _dict.update(get_element_names(family_data, element = 'bend', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'quad', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, element = 'corr',  prefix=prefix, suffix=suffix))
        return _dict

    if subsystem.lower() == 'tspm':
        prefix = 'TSPM-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'sep', prefix=prefix, suffix=suffix)
        return _dict

    if subsystem.lower() == 'tsti':
        _dict = {
                'TSTI-SEPTUMTHICK-ENABLED':{},
                'TSTI-SEPTUMTHICK-DELAY':{},
                'TSTI-SEPTUMTHIN-ENABLED':{},
                'TSTI-SEPTUMTHIN-DELAY':{},
                'TSTI-SEPTUMEX-ENABLED':{},
                'TSTI-SEPTUMEX-DELAY':{},
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
            prefix + 'BEND-01' + suffix : {'bend' : [family_data['bend']['index'][0]]},
            prefix + 'BEND-02' + suffix : {'bend' : [family_data['bend']['index'][1]]},
            prefix + 'BEND-03' + suffix : {'bend' : [family_data['bend']['index'][2]]},
        }
        return _dict

    if element.lower() == 'septa' or element.lower() == 'sep':
        _dict ={
            prefix + 'SEPTUMEXT-01'   + suffix : {'septex'  : family_data['septex']['index'] },
            prefix + 'SEPTUMTHICK-04' + suffix : {'septing' : family_data['septing']['index']},
            prefix + 'SEPTUMTHIN-04'  + suffix : {'septinf' : family_data['septinf']['index']},
        }
        return _dict

    if element.lower() == 'quad':
        _dict = {
            prefix + 'QF-01-A' + suffix : {'qf1a': family_data['qf1a']['index']},
            prefix + 'QF-01-B' + suffix : {'qf1b': family_data['qf1b']['index']},
            prefix + 'QD-02'   + suffix : {'qd2' : family_data['qd2']['index'] },
            prefix + 'QF-02'   + suffix : {'qf2' : family_data['qf2']['index'] },
            prefix + 'QF-03'   + suffix : {'qf3' : family_data['qf3']['index'] },
            prefix + 'QD-04-A' + suffix : {'qd4a': family_data['qd4a']['index']},
            prefix + 'QF-04'   + suffix : {'qf4' : family_data['qf4']['index'] },
            prefix + 'QD-04-B' + suffix : {'qd4b': family_data['qd4b']['index']},
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
            prefix + 'BPM-01'   + suffix : {'bpm' : [indices[0]]},
            prefix + 'BPM-02'   + suffix : {'bpm' : [indices[1]]},
            prefix + 'BPM-03'   + suffix : {'bpm' : [indices[2]]},
            prefix + 'BPM-04-A' + suffix : {'bpm' : [indices[3]]},
            prefix + 'BPM-04-B' + suffix : {'bpm' : [indices[4]]},
        }
        return _dict

    if element.lower() == 'ch' or element.lower() == 'hcm' :
        indices = family_data['ch']['index']
        _dict = {
            prefix + 'CH-01' + suffix : {'ch' : [indices[0]]},
            prefix + 'CH-02' + suffix : {'ch' : [indices[1]]},
            prefix + 'CH-03' + suffix : {'ch' : [indices[2]]},
            prefix + 'CH-04' + suffix : {'ch' : [indices[3]]},
        }
        return _dict

    if element.lower() == 'cv' or element.lower() == 'vcm':
        indices = family_data['cv']['index']
        _dict = {
            prefix + 'CV-01-A' + suffix : {'cv' : [indices[0]]},
            prefix + 'CV-01-B' + suffix : {'cv' : [indices[1]]},
            prefix + 'CV-02'   + suffix : {'cv' : [indices[2]]},
            prefix + 'CV-03'   + suffix : {'cv' : [indices[3]]},
            prefix + 'CV-04-A' + suffix : {'cv' : [indices[4]]},
            prefix + 'CV-04-B' + suffix : {'cv' : [indices[5]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_record_names(accelerator, 'tsma')
    _dict.update(get_record_names(accelerator, 'tspm'))
    return _dict
