from . import families as _families


def get_record_names(subsystem = None):

    family_data = _families._family_data

    if subsystem == None:
        subsystems = ['bopa', 'bodi', 'borf', 'bops']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(subsystem))
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
        }
        return _dict

    if subsystem.lower() == 'bodi':
        prefix = 'BODI-'

        _dict = {
                'BODI-TUNEH':{},
                'BODI-TUNEV':{},
                'BODI-TUNES':{},
                'BODI-CURRENT':{},
                'BODI-BCURRENT':{},
        }
        bpm_dict = get_element_names(element = 'bpm', prefix = prefix)
        _dict.update(bpm_dict)
        bpm_fam_dict = get_family_names(family = 'bpm', prefix = prefix)
        _dict.update(bpm_fam_dict)
        return _dict

    if subsystem.lower() == 'bops':
        prefix = 'BOPS-'

        family_dict = {}
        family_dict.update(get_family_names(family = 'bend', prefix = prefix))
        family_dict.update(get_family_names(family = 'quad', prefix = prefix))
        family_dict.update(get_family_names(family = 'sext', prefix = prefix))

        element_dict ={}
        element_dict.update(get_element_names(element = 'ch', prefix = prefix))
        element_dict.update(get_element_names(element = 'cv', prefix = prefix))

        _dict = {}
        _dict.update(element_dict)
        _dict.update(family_dict)
        return _dict

    if subsystem.lower() == 'boma':
        prefix = 'BOMA-'

        element_dict = {}
        element_dict.update(get_element_names(element = 'bend', prefix = prefix))
        element_dict.update(get_element_names(element = 'quad', prefix = prefix))
        element_dict.update(get_element_names(element = 'sext', prefix = prefix))
        element_dict.update(get_element_names(element = 'ch', prefix = prefix))
        element_dict.update(get_element_names(element = 'cv', prefix = prefix))

        return element_dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(family = None, prefix = ''):

    family_data = _families._family_data

    if family == None:

        family_names = []
        family_names += _families.families_dipoles()
        family_names += _families.families_quadrupoles()
        family_names += _families.families_sextupoles()
        family_names += ['bpm']

        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family, prefix = prefix))
        return _dict

    if family.lower() == 'quad':
        family_names = _families.families_quadrupoles()
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family, prefix = prefix))
        return _dict

    if family.lower() == 'sext':
        family_names = _families.families_sextupoles()
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

    if family.lower() == 'qf':
        _dict = {prefix + 'QF-FAM' : {'qf' : family_data['qf']['index']}}
        return _dict

    if family.lower() == 'qd':
        _dict = {prefix + 'QD-FAM' : {'qd' : family_data['qd']['index']}}
        return _dict

    if family.lower() == 'sd':
        _dict = {prefix + 'SD-FAM' : {'sd' : family_data['sd']['index']}}
        return _dict

    if family.lower() == 'sf':
        _dict = {prefix + 'SF-FAM' : {'sf' : family_data['sf']['index']}}
        return _dict

    if family.lower() == 'b' or family.lower() == 'bend':
        _dict = {prefix + 'BEND-FAM-A' : {'bend' : family_data['b']['index']},
                 prefix + 'BEND-FAM-B' : {'bend' : family_data['b']['index']}}
        return _dict

    else:
        raise Exception('Family name %s not found'%family)


def get_element_names(element = None, prefix = ''):

    family_data = _families._family_data

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
            _dict.update(get_element_names(element, prefix = prefix))
        return _dict

    if element.lower() == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(element, prefix = prefix))
        return _dict

    if element.lower() == 'sext':
        elements = _families.families_sextupoles()
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
        prefix = prefix + 'BPM-'
        _dict = {
            prefix + '01-U'   : {'bpm' : [family_data['bpm']['index'][3]]},
            prefix + '02-U'   : {'bpm' : [family_data['bpm']['index'][4]]},
            prefix + '03-U'   : {'bpm' : [family_data['bpm']['index'][5]]},
            prefix + '04-U'   : {'bpm' : [family_data['bpm']['index'][6]]},
            prefix + '05-U'   : {'bpm' : [family_data['bpm']['index'][7]]},
            prefix + '06-U'   : {'bpm' : [family_data['bpm']['index'][8]]},
            prefix + '07-U'   : {'bpm' : [family_data['bpm']['index'][9]]},
            prefix + '08-U'   : {'bpm' : [family_data['bpm']['index'][10]]},
            prefix + '09-U'   : {'bpm' : [family_data['bpm']['index'][11]]},
            prefix + '10-U'   : {'bpm' : [family_data['bpm']['index'][12]]},
            prefix + '11-U'   : {'bpm' : [family_data['bpm']['index'][13]]},
            prefix + '12-U'   : {'bpm' : [family_data['bpm']['index'][14]]},
            prefix + '13-U'   : {'bpm' : [family_data['bpm']['index'][15]]},
            prefix + '14-U'   : {'bpm' : [family_data['bpm']['index'][16]]},
            prefix + '15-U'   : {'bpm' : [family_data['bpm']['index'][17]]},
            prefix + '16-U'   : {'bpm' : [family_data['bpm']['index'][18]]},
            prefix + '17-U'   : {'bpm' : [family_data['bpm']['index'][19]]},
            prefix + '18-U'   : {'bpm' : [family_data['bpm']['index'][20]]},
            prefix + '19-U'   : {'bpm' : [family_data['bpm']['index'][21]]},
            prefix + '20-U'   : {'bpm' : [family_data['bpm']['index'][22]]},
            prefix + '21-U'   : {'bpm' : [family_data['bpm']['index'][23]]},
            prefix + '22-U'   : {'bpm' : [family_data['bpm']['index'][24]]},
            prefix + '23-U'   : {'bpm' : [family_data['bpm']['index'][25]]},
            prefix + '24-U'   : {'bpm' : [family_data['bpm']['index'][26]]},
            prefix + '25-U'   : {'bpm' : [family_data['bpm']['index'][27]]},
            prefix + '26-U'   : {'bpm' : [family_data['bpm']['index'][28]]},
            prefix + '27-U'   : {'bpm' : [family_data['bpm']['index'][29]]},
            prefix + '28-U'   : {'bpm' : [family_data['bpm']['index'][30]]},
            prefix + '29-U'   : {'bpm' : [family_data['bpm']['index'][31]]},
            prefix + '30-U'   : {'bpm' : [family_data['bpm']['index'][32]]},
            prefix + '31-U'   : {'bpm' : [family_data['bpm']['index'][33]]},
            prefix + '32-U'   : {'bpm' : [family_data['bpm']['index'][34]]},
            prefix + '33-U'   : {'bpm' : [family_data['bpm']['index'][35]]},
            prefix + '34-U'   : {'bpm' : [family_data['bpm']['index'][36]]},
            prefix + '35-U'   : {'bpm' : [family_data['bpm']['index'][37]]},
            prefix + '36-U'   : {'bpm' : [family_data['bpm']['index'][38]]},
            prefix + '37-U'   : {'bpm' : [family_data['bpm']['index'][39]]},
            prefix + '38-U'   : {'bpm' : [family_data['bpm']['index'][40]]},
            prefix + '39-U'   : {'bpm' : [family_data['bpm']['index'][41]]},
            prefix + '40-U'   : {'bpm' : [family_data['bpm']['index'][42]]},
            prefix + '41-U'   : {'bpm' : [family_data['bpm']['index'][43]]},
            prefix + '42-U'   : {'bpm' : [family_data['bpm']['index'][44]]},
            prefix + '43-U'   : {'bpm' : [family_data['bpm']['index'][45]]},
            prefix + '44-U'   : {'bpm' : [family_data['bpm']['index'][46]]},
            prefix + '45-U'   : {'bpm' : [family_data['bpm']['index'][47]]},
            prefix + '46-U'   : {'bpm' : [family_data['bpm']['index'][48]]},
            prefix + '47-U'   : {'bpm' : [family_data['bpm']['index'][49]]},
            prefix + '48-U'   : {'bpm' : [family_data['bpm']['index'][0]]},
            prefix + '49-U'   : {'bpm' : [family_data['bpm']['index'][1]]},
            prefix + '50-U'   : {'bpm' : [family_data['bpm']['index'][2]]},
        }
        return _dict

    if element.lower() == 'bend' or element.lower() == 'b':
        prefix = prefix + 'BEND-'
        _dict = {
            prefix + '01'   : {'bend' : [family_data['b']['index'][4]]},
            prefix + '02'   : {'bend' : [family_data['b']['index'][5]]},
            prefix + '03'   : {'bend' : [family_data['b']['index'][6]]},
            prefix + '04'   : {'bend' : [family_data['b']['index'][7]]},
            prefix + '05'   : {'bend' : [family_data['b']['index'][8]]},
            prefix + '06'   : {'bend' : [family_data['b']['index'][9]]},
            prefix + '07'   : {'bend' : [family_data['b']['index'][10]]},
            prefix + '08'   : {'bend' : [family_data['b']['index'][11]]},
            prefix + '09'   : {'bend' : [family_data['b']['index'][12]]},
            prefix + '10'   : {'bend' : [family_data['b']['index'][13]]},
            prefix + '11'   : {'bend' : [family_data['b']['index'][14]]},
            prefix + '12'   : {'bend' : [family_data['b']['index'][15]]},
            prefix + '13'   : {'bend' : [family_data['b']['index'][16]]},
            prefix + '14'   : {'bend' : [family_data['b']['index'][17]]},
            prefix + '15'   : {'bend' : [family_data['b']['index'][18]]},
            prefix + '16'   : {'bend' : [family_data['b']['index'][19]]},
            prefix + '17'   : {'bend' : [family_data['b']['index'][20]]},
            prefix + '18'   : {'bend' : [family_data['b']['index'][21]]},
            prefix + '19'   : {'bend' : [family_data['b']['index'][22]]},
            prefix + '20'   : {'bend' : [family_data['b']['index'][23]]},
            prefix + '21'   : {'bend' : [family_data['b']['index'][24]]},
            prefix + '22'   : {'bend' : [family_data['b']['index'][25]]},
            prefix + '23'   : {'bend' : [family_data['b']['index'][26]]},
            prefix + '24'   : {'bend' : [family_data['b']['index'][27]]},
            prefix + '25'   : {'bend' : [family_data['b']['index'][28]]},
            prefix + '26'   : {'bend' : [family_data['b']['index'][29]]},
            prefix + '27'   : {'bend' : [family_data['b']['index'][30]]},
            prefix + '28'   : {'bend' : [family_data['b']['index'][31]]},
            prefix + '29'   : {'bend' : [family_data['b']['index'][32]]},
            prefix + '30'   : {'bend' : [family_data['b']['index'][33]]},
            prefix + '31'   : {'bend' : [family_data['b']['index'][34]]},
            prefix + '32'   : {'bend' : [family_data['b']['index'][35]]},
            prefix + '33'   : {'bend' : [family_data['b']['index'][36]]},
            prefix + '34'   : {'bend' : [family_data['b']['index'][37]]},
            prefix + '35'   : {'bend' : [family_data['b']['index'][38]]},
            prefix + '36'   : {'bend' : [family_data['b']['index'][39]]},
            prefix + '37'   : {'bend' : [family_data['b']['index'][40]]},
            prefix + '38'   : {'bend' : [family_data['b']['index'][41]]},
            prefix + '39'   : {'bend' : [family_data['b']['index'][42]]},
            prefix + '40'   : {'bend' : [family_data['b']['index'][43]]},
            prefix + '41'   : {'bend' : [family_data['b']['index'][44]]},
            prefix + '42'   : {'bend' : [family_data['b']['index'][45]]},
            prefix + '43'   : {'bend' : [family_data['b']['index'][46]]},
            prefix + '44'   : {'bend' : [family_data['b']['index'][47]]},
            prefix + '45'   : {'bend' : [family_data['b']['index'][48]]},
            prefix + '46'   : {'bend' : [family_data['b']['index'][49]]},
            prefix + '47'   : {'bend' : [family_data['b']['index'][0]]},
            prefix + '48'   : {'bend' : [family_data['b']['index'][1]]},
            prefix + '49'   : {'bend' : [family_data['b']['index'][2]]},
            prefix + '50'   : {'bend' : [family_data['b']['index'][3]]},
        }
        return _dict

    if element.lower() == 'cv':
        prefix = prefix + 'CV-'
        _dict = {
            prefix + '01-U'   : {'cv' : [family_data['cv']['index'][1]]},
            prefix + '03-U'   : {'cv' : [family_data['cv']['index'][2]]},
            prefix + '05-U'   : {'cv' : [family_data['cv']['index'][3]]},
            prefix + '07-U'   : {'cv' : [family_data['cv']['index'][4]]},
            prefix + '09-U'   : {'cv' : [family_data['cv']['index'][5]]},
            prefix + '11-U'   : {'cv' : [family_data['cv']['index'][6]]},
            prefix + '13-U'   : {'cv' : [family_data['cv']['index'][7]]},
            prefix + '15-U'   : {'cv' : [family_data['cv']['index'][8]]},
            prefix + '17-U'   : {'cv' : [family_data['cv']['index'][9]]},
            prefix + '19-U'   : {'cv' : [family_data['cv']['index'][10]]},
            prefix + '21-U'   : {'cv' : [family_data['cv']['index'][11]]},
            prefix + '23-U'   : {'cv' : [family_data['cv']['index'][12]]},
            prefix + '25-U'   : {'cv' : [family_data['cv']['index'][13]]},
            prefix + '27-U'   : {'cv' : [family_data['cv']['index'][14]]},
            prefix + '29-U'   : {'cv' : [family_data['cv']['index'][15]]},
            prefix + '31-U'   : {'cv' : [family_data['cv']['index'][16]]},
            prefix + '33-U'   : {'cv' : [family_data['cv']['index'][17]]},
            prefix + '35-U'   : {'cv' : [family_data['cv']['index'][18]]},
            prefix + '37-U'   : {'cv' : [family_data['cv']['index'][19]]},
            prefix + '39-U'   : {'cv' : [family_data['cv']['index'][20]]},
            prefix + '41-U'   : {'cv' : [family_data['cv']['index'][21]]},
            prefix + '43-U'   : {'cv' : [family_data['cv']['index'][22]]},
            prefix + '45-U'   : {'cv' : [family_data['cv']['index'][23]]},
            prefix + '47-U'   : {'cv' : [family_data['cv']['index'][24]]},
            prefix + '49-U'   : {'cv' : [family_data['cv']['index'][0]]},
        }
        return _dict

    if element.lower() == 'ch':
        prefix = prefix + 'CH-'
        _dict = {
            prefix + '01-U'   : {'ch' : [family_data['ch']['index'][1]]},
            prefix + '03-U'   : {'ch' : [family_data['ch']['index'][2]]},
            prefix + '05-U'   : {'ch' : [family_data['ch']['index'][3]]},
            prefix + '07-U'   : {'ch' : [family_data['ch']['index'][4]]},
            prefix + '09-U'   : {'ch' : [family_data['ch']['index'][5]]},
            prefix + '11-U'   : {'ch' : [family_data['ch']['index'][6]]},
            prefix + '13-U'   : {'ch' : [family_data['ch']['index'][7]]},
            prefix + '15-U'   : {'ch' : [family_data['ch']['index'][8]]},
            prefix + '17-U'   : {'ch' : [family_data['ch']['index'][9]]},
            prefix + '19-U'   : {'ch' : [family_data['ch']['index'][10]]},
            prefix + '21-U'   : {'ch' : [family_data['ch']['index'][11]]},
            prefix + '23-U'   : {'ch' : [family_data['ch']['index'][12]]},
            prefix + '25-U'   : {'ch' : [family_data['ch']['index'][13]]},
            prefix + '27-U'   : {'ch' : [family_data['ch']['index'][14]]},
            prefix + '29-U'   : {'ch' : [family_data['ch']['index'][15]]},
            prefix + '31-U'   : {'ch' : [family_data['ch']['index'][16]]},
            prefix + '33-U'   : {'ch' : [family_data['ch']['index'][17]]},
            prefix + '35-U'   : {'ch' : [family_data['ch']['index'][18]]},
            prefix + '37-U'   : {'ch' : [family_data['ch']['index'][19]]},
            prefix + '39-U'   : {'ch' : [family_data['ch']['index'][20]]},
            prefix + '41-U'   : {'ch' : [family_data['ch']['index'][21]]},
            prefix + '43-U'   : {'ch' : [family_data['ch']['index'][22]]},
            prefix + '45-U'   : {'ch' : [family_data['ch']['index'][23]]},
            prefix + '47-U'   : {'ch' : [family_data['ch']['index'][24]]},
            prefix + '49-D'   : {'ch' : [family_data['ch']['index'][0]]},
        }
        return _dict

    if element.lower() == 'qd':
        prefix = prefix + 'QD-'
        _dict = {
            prefix + '02-D'   : {'qd' : [family_data['qd']['index'][2]]},
            prefix + '04-D'   : {'qd' : [family_data['qd']['index'][3]]},
            prefix + '06-D'   : {'qd' : [family_data['qd']['index'][4]]},
            prefix + '08-D'   : {'qd' : [family_data['qd']['index'][5]]},
            prefix + '10-D'   : {'qd' : [family_data['qd']['index'][6]]},
            prefix + '12-D'   : {'qd' : [family_data['qd']['index'][7]]},
            prefix + '14-D'   : {'qd' : [family_data['qd']['index'][8]]},
            prefix + '16-D'   : {'qd' : [family_data['qd']['index'][9]]},
            prefix + '18-D'   : {'qd' : [family_data['qd']['index'][10]]},
            prefix + '20-D'   : {'qd' : [family_data['qd']['index'][11]]},
            prefix + '22-D'   : {'qd' : [family_data['qd']['index'][12]]},
            prefix + '24-D'   : {'qd' : [family_data['qd']['index'][13]]},
            prefix + '26-D'   : {'qd' : [family_data['qd']['index'][14]]},
            prefix + '28-D'   : {'qd' : [family_data['qd']['index'][15]]},
            prefix + '30-D'   : {'qd' : [family_data['qd']['index'][16]]},
            prefix + '32-D'   : {'qd' : [family_data['qd']['index'][17]]},
            prefix + '34-D'   : {'qd' : [family_data['qd']['index'][18]]},
            prefix + '36-D'   : {'qd' : [family_data['qd']['index'][19]]},
            prefix + '38-D'   : {'qd' : [family_data['qd']['index'][20]]},
            prefix + '40-D'   : {'qd' : [family_data['qd']['index'][21]]},
            prefix + '42-D'   : {'qd' : [family_data['qd']['index'][22]]},
            prefix + '44-D'   : {'qd' : [family_data['qd']['index'][23]]},
            prefix + '46-D'   : {'qd' : [family_data['qd']['index'][24]]},
            prefix + '48-D'   : {'qd' : [family_data['qd']['index'][0]]},
            prefix + '50-D'   : {'qd' : [family_data['qd']['index'][1]]},
        }
        return _dict

    if element.lower() == 'qf':
        prefix = prefix + 'QF-'
        _dict = {
            prefix + '01'   : {'qf' : [family_data['qf']['index'][4]]},
            prefix + '02'   : {'qf' : [family_data['qf']['index'][5]]},
            prefix + '03'   : {'qf' : [family_data['qf']['index'][6]]},
            prefix + '04'   : {'qf' : [family_data['qf']['index'][7]]},
            prefix + '05'   : {'qf' : [family_data['qf']['index'][8]]},
            prefix + '06'   : {'qf' : [family_data['qf']['index'][9]]},
            prefix + '07'   : {'qf' : [family_data['qf']['index'][10]]},
            prefix + '08'   : {'qf' : [family_data['qf']['index'][11]]},
            prefix + '09'   : {'qf' : [family_data['qf']['index'][12]]},
            prefix + '10'   : {'qf' : [family_data['qf']['index'][13]]},
            prefix + '11'   : {'qf' : [family_data['qf']['index'][14]]},
            prefix + '12'   : {'qf' : [family_data['qf']['index'][15]]},
            prefix + '13'   : {'qf' : [family_data['qf']['index'][16]]},
            prefix + '14'   : {'qf' : [family_data['qf']['index'][17]]},
            prefix + '15'   : {'qf' : [family_data['qf']['index'][18]]},
            prefix + '16'   : {'qf' : [family_data['qf']['index'][19]]},
            prefix + '17'   : {'qf' : [family_data['qf']['index'][20]]},
            prefix + '18'   : {'qf' : [family_data['qf']['index'][21]]},
            prefix + '19'   : {'qf' : [family_data['qf']['index'][22]]},
            prefix + '20'   : {'qf' : [family_data['qf']['index'][23]]},
            prefix + '21'   : {'qf' : [family_data['qf']['index'][24]]},
            prefix + '22'   : {'qf' : [family_data['qf']['index'][25]]},
            prefix + '23'   : {'qf' : [family_data['qf']['index'][26]]},
            prefix + '24'   : {'qf' : [family_data['qf']['index'][27]]},
            prefix + '25'   : {'qf' : [family_data['qf']['index'][28]]},
            prefix + '26'   : {'qf' : [family_data['qf']['index'][29]]},
            prefix + '27'   : {'qf' : [family_data['qf']['index'][30]]},
            prefix + '28'   : {'qf' : [family_data['qf']['index'][31]]},
            prefix + '29'   : {'qf' : [family_data['qf']['index'][32]]},
            prefix + '30'   : {'qf' : [family_data['qf']['index'][33]]},
            prefix + '31'   : {'qf' : [family_data['qf']['index'][34]]},
            prefix + '32'   : {'qf' : [family_data['qf']['index'][35]]},
            prefix + '33'   : {'qf' : [family_data['qf']['index'][36]]},
            prefix + '34'   : {'qf' : [family_data['qf']['index'][37]]},
            prefix + '35'   : {'qf' : [family_data['qf']['index'][38]]},
            prefix + '36'   : {'qf' : [family_data['qf']['index'][39]]},
            prefix + '37'   : {'qf' : [family_data['qf']['index'][40]]},
            prefix + '38'   : {'qf' : [family_data['qf']['index'][41]]},
            prefix + '39'   : {'qf' : [family_data['qf']['index'][42]]},
            prefix + '40'   : {'qf' : [family_data['qf']['index'][43]]},
            prefix + '41'   : {'qf' : [family_data['qf']['index'][44]]},
            prefix + '42'   : {'qf' : [family_data['qf']['index'][45]]},
            prefix + '43'   : {'qf' : [family_data['qf']['index'][46]]},
            prefix + '44'   : {'qf' : [family_data['qf']['index'][47]]},
            prefix + '45'   : {'qf' : [family_data['qf']['index'][48]]},
            prefix + '46'   : {'qf' : [family_data['qf']['index'][49]]},
            prefix + '47'   : {'qf' : [family_data['qf']['index'][0]]},
            prefix + '48'   : {'qf' : [family_data['qf']['index'][1]]},
            prefix + '49'   : {'qf' : [family_data['qf']['index'][2]]},
            prefix + '50'   : {'qf' : [family_data['qf']['index'][3]]},
        }
        return _dict

    if element.lower() == 'sd':
        prefix = prefix + 'SD-'
        _dict = {
            prefix + '03-U'   : {'sd' : [family_data['sd']['index'][1]]},
            prefix + '08-U'   : {'sd' : [family_data['sd']['index'][2]]},
            prefix + '13-U'   : {'sd' : [family_data['sd']['index'][3]]},
            prefix + '18-U'   : {'sd' : [family_data['sd']['index'][4]]},
            prefix + '23-U'   : {'sd' : [family_data['sd']['index'][5]]},
            prefix + '28-U'   : {'sd' : [family_data['sd']['index'][6]]},
            prefix + '33-U'   : {'sd' : [family_data['sd']['index'][7]]},
            prefix + '38-U'   : {'sd' : [family_data['sd']['index'][8]]},
            prefix + '43-U'   : {'sd' : [family_data['sd']['index'][9]]},
            prefix + '48-U'   : {'sd' : [family_data['sd']['index'][0]]},
        }
        return _dict

    if element.lower() == 'sf':
        prefix = prefix + 'SF-'
        _dict = {
            prefix + '02-U'   : {'sf' : [family_data['sf']['index'][2]]},
            prefix + '04-U'   : {'sf' : [family_data['sf']['index'][3]]},
            prefix + '06-U'   : {'sf' : [family_data['sf']['index'][4]]},
            prefix + '08-U'   : {'sf' : [family_data['sf']['index'][5]]},
            prefix + '10-U'   : {'sf' : [family_data['sf']['index'][6]]},
            prefix + '12-U'   : {'sf' : [family_data['sf']['index'][7]]},
            prefix + '14-U'   : {'sf' : [family_data['sf']['index'][8]]},
            prefix + '16-U'   : {'sf' : [family_data['sf']['index'][9]]},
            prefix + '18-U'   : {'sf' : [family_data['sf']['index'][10]]},
            prefix + '20-U'   : {'sf' : [family_data['sf']['index'][11]]},
            prefix + '22-U'   : {'sf' : [family_data['sf']['index'][12]]},
            prefix + '24-U'   : {'sf' : [family_data['sf']['index'][13]]},
            prefix + '26-U'   : {'sf' : [family_data['sf']['index'][14]]},
            prefix + '28-U'   : {'sf' : [family_data['sf']['index'][15]]},
            prefix + '30-U'   : {'sf' : [family_data['sf']['index'][16]]},
            prefix + '32-U'   : {'sf' : [family_data['sf']['index'][17]]},
            prefix + '34-U'   : {'sf' : [family_data['sf']['index'][18]]},
            prefix + '36-U'   : {'sf' : [family_data['sf']['index'][19]]},
            prefix + '38-U'   : {'sf' : [family_data['sf']['index'][20]]},
            prefix + '40-U'   : {'sf' : [family_data['sf']['index'][21]]},
            prefix + '42-U'   : {'sf' : [family_data['sf']['index'][22]]},
            prefix + '44-U'   : {'sf' : [family_data['sf']['index'][23]]},
            prefix + '46-U'   : {'sf' : [family_data['sf']['index'][24]]},
            prefix + '48-U'   : {'sf' : [family_data['sf']['index'][0]]},
            prefix + '50-U'   : {'sf' : [family_data['sf']['index'][1]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)
