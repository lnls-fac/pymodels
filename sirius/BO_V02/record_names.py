
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
        subsystems = ['bopa', 'bodi', 'borf', 'bops', 'boti']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(family_data, subsystem))
        return record_names_dict

    if subsystem.lower() == 'borf':
        indices = family_data['cav']['index']
        _dict = {
            'BORF-FREQUENCY':{'cav':indices},
            'BORF-VOLTAGE'  :{'cav':indices},
        }
        return _dict

    if subsystem.lower() == 'bopa':
        _dict = {
                'BOPA-CHROMX':{},
                'BOPA-CHROMY':{},
                'BOPA-LIFETIME':{},
                'BOPA-BLIFETIME':{},
                'BOPA-SIGX':{},
                'BOPA-SIGY':{},
                'BOPA-SIGS':{},
                'BOPA-EMITX':{},
                'BOPA-EMITY':{},
                'BOPA-SIGX':{},
                'BOPA-SIGY':{},
                'BOPA-SIGS':{},
                'BOPA-INJEFF':{},
                'BOPA-EXTEFF':{},
        }
        return _dict

    if subsystem.lower() == 'bodi':
        prefix = 'BODI-'
        suffix = ''

        _dict = {
                'BODI-TUNEH':{},
                'BODI-TUNEV':{},
                'BODI-TUNES':{},
                'BODI-CURRENT':{},
                'BODI-BCURRENT':{},
        }
        _dict.update(get_element_names(family_data, element = 'bpm', prefix=prefix, suffix=suffix))
        _dict.update(get_family_names(family_data, family = 'bpm', prefix=prefix, suffix='-X'))
        _dict.update(get_family_names(family_data, family = 'bpm', prefix=prefix, suffix='-Y'))
        return _dict

    if subsystem.lower() == 'bops':
        prefix = 'BOPS-'
        suffix = ''

        family_dict = {}
        family_dict.update(get_family_names(family_data, family = 'bend', prefix=prefix, suffix=suffix))
        family_dict.update(get_family_names(family_data, family = 'quad', prefix=prefix, suffix=suffix))
        family_dict.update(get_family_names(family_data, family = 'sext', prefix=prefix, suffix=suffix))

        element_dict ={}
        element_dict.update(get_element_names(family_data, element = 'corr', prefix=prefix, suffix=suffix))

        _dict = {}
        _dict.update(element_dict)
        _dict.update(family_dict)
        return _dict

    if subsystem.lower() == 'boma':
        prefix = 'BOMA-'
        suffix = ''

        element_dict = {}
        element_dict.update(get_element_names(family_data, element = 'bend', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'quad', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'sext', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'corr', prefix=prefix, suffix=suffix))

        return element_dict


    if subsystem.lower() == 'boti':
        _dict = {
                'BOTI-KICKINJ-ENABLED':{},
                'BOTI-KICKINJ-DELAY':{},
                'BOTI-KICKEX-ENABLED':{},
                'BOTI-KICKEX-DELAY':{},
                'BOTI-KICKEX-INC':{},
                'BOTI-RAMPPS-ENABLED':{},
                'BOTI-RAMPPS-DELAY':{},
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

        family_names = []
        family_names += _families.families_dipoles()
        family_names += _families.families_quadrupoles()
        family_names += _families.families_sextupoles()
        family_names += ['bpm']

        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix=prefix, suffix=suffix))
        return _dict

    if family.lower() == 'quad':
        family_names = _families.families_quadrupoles()
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix=prefix, suffix=suffix))
        return _dict

    if family.lower() == 'sext':
        family_names = _families.families_sextupoles()
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix=prefix, suffix=suffix))
        return _dict

    if family.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {prefix + 'BPM-FAM' + suffix : {'bpm': indices}}
        return _dict

    if family.lower() == 'qf':
        _dict = {prefix + 'QF-FAM' + suffix : {'qf' : family_data['qf']['index']}}
        return _dict

    if family.lower() == 'qd':
        _dict = {prefix + 'QD-FAM' + suffix : {'qd' : family_data['qd']['index']}}
        return _dict

    if family.lower() == 'sd':
        _dict = {prefix + 'SD-FAM' + suffix : {'sd' : family_data['sd']['index']}}
        return _dict

    if family.lower() == 'sf':
        _dict = {prefix + 'SF-FAM' + suffix : {'sf' : family_data['sf']['index']}}
        return _dict

    if family.lower() == 'b' or family.lower() == 'bend':
        _dict = {prefix + 'BEND-FAM-A' + suffix : {'bend' : family_data['b']['index']},
                 prefix + 'BEND-FAM-B' + suffix : {'bend' : family_data['b']['index']}}
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
        elements += _families.families_quadrupoles()
        elements += _families.families_sextupoles()
        elements += _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'sext':
        elements = _families.families_sextupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'corr':
        elements  = _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'bpm':
        prefix = prefix + 'BPM-'
        _dict = {
            prefix + '01-U' + suffix : {'bpm' : [family_data['bpm']['index'][49]]},
            prefix + '02-U' + suffix : {'bpm' : [family_data['bpm']['index'][0]]},
            prefix + '03-U' + suffix : {'bpm' : [family_data['bpm']['index'][1]]},
            prefix + '04-U' + suffix : {'bpm' : [family_data['bpm']['index'][2]]},
            prefix + '05-U' + suffix : {'bpm' : [family_data['bpm']['index'][3]]},
            prefix + '06-U' + suffix : {'bpm' : [family_data['bpm']['index'][4]]},
            prefix + '07-U' + suffix : {'bpm' : [family_data['bpm']['index'][5]]},
            prefix + '08-U' + suffix : {'bpm' : [family_data['bpm']['index'][6]]},
            prefix + '09-U' + suffix : {'bpm' : [family_data['bpm']['index'][7]]},
            prefix + '10-U' + suffix : {'bpm' : [family_data['bpm']['index'][8]]},
            prefix + '11-U' + suffix : {'bpm' : [family_data['bpm']['index'][9]]},
            prefix + '12-U' + suffix : {'bpm' : [family_data['bpm']['index'][10]]},
            prefix + '13-U' + suffix : {'bpm' : [family_data['bpm']['index'][11]]},
            prefix + '14-U' + suffix : {'bpm' : [family_data['bpm']['index'][12]]},
            prefix + '15-U' + suffix : {'bpm' : [family_data['bpm']['index'][13]]},
            prefix + '16-U' + suffix : {'bpm' : [family_data['bpm']['index'][14]]},
            prefix + '17-U' + suffix : {'bpm' : [family_data['bpm']['index'][15]]},
            prefix + '18-U' + suffix : {'bpm' : [family_data['bpm']['index'][16]]},
            prefix + '19-U' + suffix : {'bpm' : [family_data['bpm']['index'][17]]},
            prefix + '20-U' + suffix : {'bpm' : [family_data['bpm']['index'][18]]},
            prefix + '21-U' + suffix : {'bpm' : [family_data['bpm']['index'][19]]},
            prefix + '22-U' + suffix : {'bpm' : [family_data['bpm']['index'][20]]},
            prefix + '23-U' + suffix : {'bpm' : [family_data['bpm']['index'][21]]},
            prefix + '24-U' + suffix : {'bpm' : [family_data['bpm']['index'][22]]},
            prefix + '25-U' + suffix : {'bpm' : [family_data['bpm']['index'][23]]},
            prefix + '26-U' + suffix : {'bpm' : [family_data['bpm']['index'][24]]},
            prefix + '27-U' + suffix : {'bpm' : [family_data['bpm']['index'][25]]},
            prefix + '28-U' + suffix : {'bpm' : [family_data['bpm']['index'][26]]},
            prefix + '29-U' + suffix : {'bpm' : [family_data['bpm']['index'][27]]},
            prefix + '30-U' + suffix : {'bpm' : [family_data['bpm']['index'][28]]},
            prefix + '31-U' + suffix : {'bpm' : [family_data['bpm']['index'][29]]},
            prefix + '32-U' + suffix : {'bpm' : [family_data['bpm']['index'][30]]},
            prefix + '33-U' + suffix : {'bpm' : [family_data['bpm']['index'][31]]},
            prefix + '34-U' + suffix : {'bpm' : [family_data['bpm']['index'][32]]},
            prefix + '35-U' + suffix : {'bpm' : [family_data['bpm']['index'][33]]},
            prefix + '36-U' + suffix : {'bpm' : [family_data['bpm']['index'][34]]},
            prefix + '37-U' + suffix : {'bpm' : [family_data['bpm']['index'][35]]},
            prefix + '38-U' + suffix : {'bpm' : [family_data['bpm']['index'][36]]},
            prefix + '39-U' + suffix : {'bpm' : [family_data['bpm']['index'][37]]},
            prefix + '40-U' + suffix : {'bpm' : [family_data['bpm']['index'][38]]},
            prefix + '41-U' + suffix : {'bpm' : [family_data['bpm']['index'][39]]},
            prefix + '42-U' + suffix : {'bpm' : [family_data['bpm']['index'][40]]},
            prefix + '43-U' + suffix : {'bpm' : [family_data['bpm']['index'][41]]},
            prefix + '44-U' + suffix : {'bpm' : [family_data['bpm']['index'][42]]},
            prefix + '45-U' + suffix : {'bpm' : [family_data['bpm']['index'][43]]},
            prefix + '46-U' + suffix : {'bpm' : [family_data['bpm']['index'][44]]},
            prefix + '47-U' + suffix : {'bpm' : [family_data['bpm']['index'][45]]},
            prefix + '48-U' + suffix : {'bpm' : [family_data['bpm']['index'][46]]},
            prefix + '49-U' + suffix : {'bpm' : [family_data['bpm']['index'][47]]},
            prefix + '50-U' + suffix : {'bpm' : [family_data['bpm']['index'][48]]},
        }
        return _dict

    if element.lower() == 'bend' or element.lower() == 'b':
        prefix = prefix + 'BEND-'
        _dict = {
            prefix + '01' + suffix : {'bend' : [family_data['b']['index'][0]]},
            prefix + '02' + suffix : {'bend' : [family_data['b']['index'][1]]},
            prefix + '03' + suffix : {'bend' : [family_data['b']['index'][2]]},
            prefix + '04' + suffix : {'bend' : [family_data['b']['index'][3]]},
            prefix + '05' + suffix : {'bend' : [family_data['b']['index'][4]]},
            prefix + '06' + suffix : {'bend' : [family_data['b']['index'][5]]},
            prefix + '07' + suffix : {'bend' : [family_data['b']['index'][6]]},
            prefix + '08' + suffix : {'bend' : [family_data['b']['index'][7]]},
            prefix + '09' + suffix : {'bend' : [family_data['b']['index'][8]]},
            prefix + '10' + suffix : {'bend' : [family_data['b']['index'][9]]},
            prefix + '11' + suffix : {'bend' : [family_data['b']['index'][10]]},
            prefix + '12' + suffix : {'bend' : [family_data['b']['index'][11]]},
            prefix + '13' + suffix : {'bend' : [family_data['b']['index'][12]]},
            prefix + '14' + suffix : {'bend' : [family_data['b']['index'][13]]},
            prefix + '15' + suffix : {'bend' : [family_data['b']['index'][14]]},
            prefix + '16' + suffix : {'bend' : [family_data['b']['index'][15]]},
            prefix + '17' + suffix : {'bend' : [family_data['b']['index'][16]]},
            prefix + '18' + suffix : {'bend' : [family_data['b']['index'][17]]},
            prefix + '19' + suffix : {'bend' : [family_data['b']['index'][18]]},
            prefix + '20' + suffix : {'bend' : [family_data['b']['index'][19]]},
            prefix + '21' + suffix : {'bend' : [family_data['b']['index'][20]]},
            prefix + '22' + suffix : {'bend' : [family_data['b']['index'][21]]},
            prefix + '23' + suffix : {'bend' : [family_data['b']['index'][22]]},
            prefix + '24' + suffix : {'bend' : [family_data['b']['index'][23]]},
            prefix + '25' + suffix : {'bend' : [family_data['b']['index'][24]]},
            prefix + '26' + suffix : {'bend' : [family_data['b']['index'][25]]},
            prefix + '27' + suffix : {'bend' : [family_data['b']['index'][26]]},
            prefix + '28' + suffix : {'bend' : [family_data['b']['index'][27]]},
            prefix + '29' + suffix : {'bend' : [family_data['b']['index'][28]]},
            prefix + '30' + suffix : {'bend' : [family_data['b']['index'][29]]},
            prefix + '31' + suffix : {'bend' : [family_data['b']['index'][30]]},
            prefix + '32' + suffix : {'bend' : [family_data['b']['index'][31]]},
            prefix + '33' + suffix : {'bend' : [family_data['b']['index'][32]]},
            prefix + '34' + suffix : {'bend' : [family_data['b']['index'][33]]},
            prefix + '35' + suffix : {'bend' : [family_data['b']['index'][34]]},
            prefix + '36' + suffix : {'bend' : [family_data['b']['index'][35]]},
            prefix + '37' + suffix : {'bend' : [family_data['b']['index'][36]]},
            prefix + '38' + suffix : {'bend' : [family_data['b']['index'][37]]},
            prefix + '39' + suffix : {'bend' : [family_data['b']['index'][38]]},
            prefix + '40' + suffix : {'bend' : [family_data['b']['index'][39]]},
            prefix + '41' + suffix : {'bend' : [family_data['b']['index'][40]]},
            prefix + '42' + suffix : {'bend' : [family_data['b']['index'][41]]},
            prefix + '43' + suffix : {'bend' : [family_data['b']['index'][42]]},
            prefix + '44' + suffix : {'bend' : [family_data['b']['index'][43]]},
            prefix + '45' + suffix : {'bend' : [family_data['b']['index'][44]]},
            prefix + '46' + suffix : {'bend' : [family_data['b']['index'][45]]},
            prefix + '47' + suffix : {'bend' : [family_data['b']['index'][46]]},
            prefix + '48' + suffix : {'bend' : [family_data['b']['index'][47]]},
            prefix + '49' + suffix : {'bend' : [family_data['b']['index'][48]]},
            prefix + '50' + suffix : {'bend' : [family_data['b']['index'][49]]},
        }
        return _dict

    if element.lower() == 'cv':
        prefix = prefix + 'CV-'
        _dict = {
            prefix + '01-U' + suffix : {'cv' : [family_data['cv']['index'][24]]},
            prefix + '03-U' + suffix : {'cv' : [family_data['cv']['index'][0]]},
            prefix + '05-U' + suffix : {'cv' : [family_data['cv']['index'][1]]},
            prefix + '07-U' + suffix : {'cv' : [family_data['cv']['index'][2]]},
            prefix + '09-U' + suffix : {'cv' : [family_data['cv']['index'][3]]},
            prefix + '11-U' + suffix : {'cv' : [family_data['cv']['index'][4]]},
            prefix + '13-U' + suffix : {'cv' : [family_data['cv']['index'][5]]},
            prefix + '15-U' + suffix : {'cv' : [family_data['cv']['index'][6]]},
            prefix + '17-U' + suffix : {'cv' : [family_data['cv']['index'][7]]},
            prefix + '19-U' + suffix : {'cv' : [family_data['cv']['index'][8]]},
            prefix + '21-U' + suffix : {'cv' : [family_data['cv']['index'][9]]},
            prefix + '23-U' + suffix : {'cv' : [family_data['cv']['index'][10]]},
            prefix + '25-U' + suffix : {'cv' : [family_data['cv']['index'][11]]},
            prefix + '27-U' + suffix : {'cv' : [family_data['cv']['index'][12]]},
            prefix + '29-U' + suffix : {'cv' : [family_data['cv']['index'][13]]},
            prefix + '31-U' + suffix : {'cv' : [family_data['cv']['index'][14]]},
            prefix + '33-U' + suffix : {'cv' : [family_data['cv']['index'][15]]},
            prefix + '35-U' + suffix : {'cv' : [family_data['cv']['index'][16]]},
            prefix + '37-U' + suffix : {'cv' : [family_data['cv']['index'][17]]},
            prefix + '39-U' + suffix : {'cv' : [family_data['cv']['index'][18]]},
            prefix + '41-U' + suffix : {'cv' : [family_data['cv']['index'][19]]},
            prefix + '43-U' + suffix : {'cv' : [family_data['cv']['index'][20]]},
            prefix + '45-U' + suffix : {'cv' : [family_data['cv']['index'][21]]},
            prefix + '47-U' + suffix : {'cv' : [family_data['cv']['index'][22]]},
            prefix + '49-U' + suffix : {'cv' : [family_data['cv']['index'][23]]},
        }
        return _dict

    if element.lower() == 'ch':
        prefix = prefix + 'CH-'
        _dict = {
            prefix + '01-U' + suffix : {'ch' : [family_data['ch']['index'][24]]},
            prefix + '03-U' + suffix : {'ch' : [family_data['ch']['index'][0]]},
            prefix + '05-U' + suffix : {'ch' : [family_data['ch']['index'][1]]},
            prefix + '07-U' + suffix : {'ch' : [family_data['ch']['index'][2]]},
            prefix + '09-U' + suffix : {'ch' : [family_data['ch']['index'][3]]},
            prefix + '11-U' + suffix : {'ch' : [family_data['ch']['index'][4]]},
            prefix + '13-U' + suffix : {'ch' : [family_data['ch']['index'][5]]},
            prefix + '15-U' + suffix : {'ch' : [family_data['ch']['index'][6]]},
            prefix + '17-U' + suffix : {'ch' : [family_data['ch']['index'][7]]},
            prefix + '19-U' + suffix : {'ch' : [family_data['ch']['index'][8]]},
            prefix + '21-U' + suffix : {'ch' : [family_data['ch']['index'][9]]},
            prefix + '23-U' + suffix : {'ch' : [family_data['ch']['index'][10]]},
            prefix + '25-U' + suffix : {'ch' : [family_data['ch']['index'][11]]},
            prefix + '27-U' + suffix : {'ch' : [family_data['ch']['index'][12]]},
            prefix + '29-U' + suffix : {'ch' : [family_data['ch']['index'][13]]},
            prefix + '31-U' + suffix : {'ch' : [family_data['ch']['index'][14]]},
            prefix + '33-U' + suffix : {'ch' : [family_data['ch']['index'][15]]},
            prefix + '35-U' + suffix : {'ch' : [family_data['ch']['index'][16]]},
            prefix + '37-U' + suffix : {'ch' : [family_data['ch']['index'][17]]},
            prefix + '39-U' + suffix : {'ch' : [family_data['ch']['index'][18]]},
            prefix + '41-U' + suffix : {'ch' : [family_data['ch']['index'][19]]},
            prefix + '43-U' + suffix : {'ch' : [family_data['ch']['index'][20]]},
            prefix + '45-U' + suffix : {'ch' : [family_data['ch']['index'][21]]},
            prefix + '47-U' + suffix : {'ch' : [family_data['ch']['index'][22]]},
            prefix + '49-D' + suffix : {'ch' : [family_data['ch']['index'][23]]},
        }
        return _dict

    if element.lower() == 'qd':
        prefix = prefix + 'QD-'
        _dict = {
            prefix + '02-D' + suffix : {'qd' : [family_data['qd']['index'][0]]},
            prefix + '04-D' + suffix : {'qd' : [family_data['qd']['index'][1]]},
            prefix + '06-D' + suffix : {'qd' : [family_data['qd']['index'][2]]},
            prefix + '08-D' + suffix : {'qd' : [family_data['qd']['index'][3]]},
            prefix + '10-D' + suffix : {'qd' : [family_data['qd']['index'][4]]},
            prefix + '12-D' + suffix : {'qd' : [family_data['qd']['index'][5]]},
            prefix + '14-D' + suffix : {'qd' : [family_data['qd']['index'][6]]},
            prefix + '16-D' + suffix : {'qd' : [family_data['qd']['index'][7]]},
            prefix + '18-D' + suffix : {'qd' : [family_data['qd']['index'][8]]},
            prefix + '20-D' + suffix : {'qd' : [family_data['qd']['index'][9]]},
            prefix + '22-D' + suffix : {'qd' : [family_data['qd']['index'][10]]},
            prefix + '24-D' + suffix : {'qd' : [family_data['qd']['index'][11]]},
            prefix + '26-D' + suffix : {'qd' : [family_data['qd']['index'][12]]},
            prefix + '28-D' + suffix : {'qd' : [family_data['qd']['index'][13]]},
            prefix + '30-D' + suffix : {'qd' : [family_data['qd']['index'][14]]},
            prefix + '32-D' + suffix : {'qd' : [family_data['qd']['index'][15]]},
            prefix + '34-D' + suffix : {'qd' : [family_data['qd']['index'][16]]},
            prefix + '36-D' + suffix : {'qd' : [family_data['qd']['index'][17]]},
            prefix + '38-D' + suffix : {'qd' : [family_data['qd']['index'][18]]},
            prefix + '40-D' + suffix : {'qd' : [family_data['qd']['index'][19]]},
            prefix + '42-D' + suffix : {'qd' : [family_data['qd']['index'][20]]},
            prefix + '44-D' + suffix : {'qd' : [family_data['qd']['index'][21]]},
            prefix + '46-D' + suffix : {'qd' : [family_data['qd']['index'][22]]},
            prefix + '48-D' + suffix : {'qd' : [family_data['qd']['index'][23]]},
            prefix + '50-D' + suffix : {'qd' : [family_data['qd']['index'][24]]},
        }
        return _dict

    if element.lower() == 'qf':
        prefix = prefix + 'QF-'
        _dict = {
            prefix + '01' + suffix : {'qf' : [family_data['qf']['index'][0]]},
            prefix + '02' + suffix : {'qf' : [family_data['qf']['index'][1]]},
            prefix + '03' + suffix : {'qf' : [family_data['qf']['index'][2]]},
            prefix + '04' + suffix : {'qf' : [family_data['qf']['index'][3]]},
            prefix + '05' + suffix : {'qf' : [family_data['qf']['index'][4]]},
            prefix + '06' + suffix : {'qf' : [family_data['qf']['index'][5]]},
            prefix + '07' + suffix : {'qf' : [family_data['qf']['index'][6]]},
            prefix + '08' + suffix : {'qf' : [family_data['qf']['index'][7]]},
            prefix + '09' + suffix : {'qf' : [family_data['qf']['index'][8]]},
            prefix + '10' + suffix : {'qf' : [family_data['qf']['index'][9]]},
            prefix + '11' + suffix : {'qf' : [family_data['qf']['index'][10]]},
            prefix + '12' + suffix : {'qf' : [family_data['qf']['index'][11]]},
            prefix + '13' + suffix : {'qf' : [family_data['qf']['index'][12]]},
            prefix + '14' + suffix : {'qf' : [family_data['qf']['index'][13]]},
            prefix + '15' + suffix : {'qf' : [family_data['qf']['index'][14]]},
            prefix + '16' + suffix : {'qf' : [family_data['qf']['index'][15]]},
            prefix + '17' + suffix : {'qf' : [family_data['qf']['index'][16]]},
            prefix + '18' + suffix : {'qf' : [family_data['qf']['index'][17]]},
            prefix + '19' + suffix : {'qf' : [family_data['qf']['index'][18]]},
            prefix + '20' + suffix : {'qf' : [family_data['qf']['index'][19]]},
            prefix + '21' + suffix : {'qf' : [family_data['qf']['index'][20]]},
            prefix + '22' + suffix : {'qf' : [family_data['qf']['index'][21]]},
            prefix + '23' + suffix : {'qf' : [family_data['qf']['index'][22]]},
            prefix + '24' + suffix : {'qf' : [family_data['qf']['index'][23]]},
            prefix + '25' + suffix : {'qf' : [family_data['qf']['index'][24]]},
            prefix + '26' + suffix : {'qf' : [family_data['qf']['index'][25]]},
            prefix + '27' + suffix : {'qf' : [family_data['qf']['index'][26]]},
            prefix + '28' + suffix : {'qf' : [family_data['qf']['index'][27]]},
            prefix + '29' + suffix : {'qf' : [family_data['qf']['index'][28]]},
            prefix + '30' + suffix : {'qf' : [family_data['qf']['index'][29]]},
            prefix + '31' + suffix : {'qf' : [family_data['qf']['index'][30]]},
            prefix + '32' + suffix : {'qf' : [family_data['qf']['index'][31]]},
            prefix + '33' + suffix : {'qf' : [family_data['qf']['index'][32]]},
            prefix + '34' + suffix : {'qf' : [family_data['qf']['index'][33]]},
            prefix + '35' + suffix : {'qf' : [family_data['qf']['index'][34]]},
            prefix + '36' + suffix : {'qf' : [family_data['qf']['index'][35]]},
            prefix + '37' + suffix : {'qf' : [family_data['qf']['index'][36]]},
            prefix + '38' + suffix : {'qf' : [family_data['qf']['index'][37]]},
            prefix + '39' + suffix : {'qf' : [family_data['qf']['index'][38]]},
            prefix + '40' + suffix : {'qf' : [family_data['qf']['index'][39]]},
            prefix + '41' + suffix : {'qf' : [family_data['qf']['index'][40]]},
            prefix + '42' + suffix : {'qf' : [family_data['qf']['index'][41]]},
            prefix + '43' + suffix : {'qf' : [family_data['qf']['index'][42]]},
            prefix + '44' + suffix : {'qf' : [family_data['qf']['index'][43]]},
            prefix + '45' + suffix : {'qf' : [family_data['qf']['index'][44]]},
            prefix + '46' + suffix : {'qf' : [family_data['qf']['index'][45]]},
            prefix + '47' + suffix : {'qf' : [family_data['qf']['index'][46]]},
            prefix + '48' + suffix : {'qf' : [family_data['qf']['index'][47]]},
            prefix + '49' + suffix : {'qf' : [family_data['qf']['index'][48]]},
            prefix + '50' + suffix : {'qf' : [family_data['qf']['index'][49]]},
        }
        return _dict

    if element.lower() == 'sd':
        prefix = prefix + 'SD-'
        _dict = {
            prefix + '03-U' + suffix : {'sd' : [family_data['sd']['index'][0]]},
            prefix + '08-U' + suffix : {'sd' : [family_data['sd']['index'][1]]},
            prefix + '13-U' + suffix : {'sd' : [family_data['sd']['index'][2]]},
            prefix + '18-U' + suffix : {'sd' : [family_data['sd']['index'][3]]},
            prefix + '23-U' + suffix : {'sd' : [family_data['sd']['index'][4]]},
            prefix + '28-U' + suffix : {'sd' : [family_data['sd']['index'][5]]},
            prefix + '33-U' + suffix : {'sd' : [family_data['sd']['index'][6]]},
            prefix + '38-U' + suffix : {'sd' : [family_data['sd']['index'][7]]},
            prefix + '43-U' + suffix : {'sd' : [family_data['sd']['index'][8]]},
            prefix + '48-U' + suffix : {'sd' : [family_data['sd']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sf':
        prefix = prefix + 'SF-'
        _dict = {
            prefix + '02-U' + suffix : {'sf' : [family_data['sf']['index'][0]]},
            prefix + '04-U' + suffix : {'sf' : [family_data['sf']['index'][1]]},
            prefix + '06-U' + suffix : {'sf' : [family_data['sf']['index'][2]]},
            prefix + '08-U' + suffix : {'sf' : [family_data['sf']['index'][3]]},
            prefix + '10-U' + suffix : {'sf' : [family_data['sf']['index'][4]]},
            prefix + '12-U' + suffix : {'sf' : [family_data['sf']['index'][5]]},
            prefix + '14-U' + suffix : {'sf' : [family_data['sf']['index'][6]]},
            prefix + '16-U' + suffix : {'sf' : [family_data['sf']['index'][7]]},
            prefix + '18-U' + suffix : {'sf' : [family_data['sf']['index'][8]]},
            prefix + '20-U' + suffix : {'sf' : [family_data['sf']['index'][9]]},
            prefix + '22-U' + suffix : {'sf' : [family_data['sf']['index'][10]]},
            prefix + '24-U' + suffix : {'sf' : [family_data['sf']['index'][11]]},
            prefix + '26-U' + suffix : {'sf' : [family_data['sf']['index'][12]]},
            prefix + '28-U' + suffix : {'sf' : [family_data['sf']['index'][13]]},
            prefix + '30-U' + suffix : {'sf' : [family_data['sf']['index'][14]]},
            prefix + '32-U' + suffix : {'sf' : [family_data['sf']['index'][15]]},
            prefix + '34-U' + suffix : {'sf' : [family_data['sf']['index'][16]]},
            prefix + '36-U' + suffix : {'sf' : [family_data['sf']['index'][17]]},
            prefix + '38-U' + suffix : {'sf' : [family_data['sf']['index'][18]]},
            prefix + '40-U' + suffix : {'sf' : [family_data['sf']['index'][19]]},
            prefix + '42-U' + suffix : {'sf' : [family_data['sf']['index'][20]]},
            prefix + '44-U' + suffix : {'sf' : [family_data['sf']['index'][21]]},
            prefix + '46-U' + suffix : {'sf' : [family_data['sf']['index'][22]]},
            prefix + '48-U' + suffix : {'sf' : [family_data['sf']['index'][23]]},
            prefix + '50-U' + suffix : {'sf' : [family_data['sf']['index'][24]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    return get_record_names(accelerator, 'boma')
