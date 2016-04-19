
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
        subsystems = ['sipa', 'sidi', 'sirf', 'sips', 'siti', 'sipu']
        device_names_dict = {}
        for subsystem in subsystems:
            device_names_dict.update(get_device_names(family_data, subsystem))
        return device_names_dict

    if subsystem.lower() == 'sirf':
        indices = family_data['cav']['index']
        _dict = {
            'SIRF-FREQUENCY':{'cav':indices},
            'SIRF-VOLTAGE':{'cav':indices},
        }
        return _dict

    if subsystem.lower() == 'sipa':
        _dict = {
                'SIPA-CHROMX':{},
                'SIPA-CHROMY':{},
                'SIPA-LIFETIME':{},
                'SIPA-BLIFETIME':{},
                'SIPA-SIGX':{},
                'SIPA-SIGY':{},
                'SIPA-SIGS':{},
                'SIPA-EMITX':{},
                'SIPA-EMITY':{},
                'SIPA-SIGX':{},
                'SIPA-SIGY':{},
                'SIPA-SIGS':{},
                'SIPA-INJEFF':{},
                'SIPA-INJEFF-TOTAL':{},
        }
        return _dict

    if subsystem.lower() == 'sidi':
        prefix = 'SIDI-'
        suffix = ''

        _dict = {
                'SIDI-TUNEH':{},
                'SIDI-TUNEV':{},
                'SIDI-TUNES':{},
                'SIDI-CURRENT':{},
                'SIDI-BCURRENT':{},
        }
        _dict.update(get_element_names(family_data, element = 'bpm', prefix=prefix, suffix=suffix))
        _dict.update(get_family_names(family_data, family = 'bpm', prefix=prefix, suffix=suffix))
        return _dict

    if subsystem.lower() == 'sips':
        prefix = 'SIPS-'
        suffix = ''

        element_dict = {}
        element_dict.update(get_element_names(family_data, element = 'quad',  prefix=prefix, suffix=suffix))
        #element_dict.update(get_element_names(family_data, element = 'sext',  prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'hcorr', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'vcorr', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'qs',    prefix=prefix, suffix=suffix))

        family_dict = {}
        family_dict.update(get_family_names(family_data, family = 'bend', prefix=prefix, suffix=suffix))
        family_dict.update(get_family_names(family_data, family = 'quad', prefix=prefix, suffix=suffix))
        family_dict.update(get_family_names(family_data, family = 'sext', prefix=prefix, suffix=suffix))

        _dict = {}
        _dict.update(element_dict)
        _dict.update(family_dict)
        return _dict

    if subsystem.lower() == 'sipu':
        prefix = 'SIPU-'
        suffix = ''
        _dict = get_element_names(family_data, element='pulsed_magnets', prefix=prefix, suffix=suffix)
        return _dict

    if subsystem.lower() == 'sima':
        prefix = 'SIMA-'
        suffix = ''

        element_dict = {}
        element_dict.update(get_element_names(family_data, element = 'bend',  prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'quad',  prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'sext',  prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'hcorr', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'vcorr', prefix=prefix, suffix=suffix))
        element_dict.update(get_element_names(family_data, element = 'qs',    prefix=prefix, suffix=suffix))

        return element_dict

    if subsystem.lower() == 'sipm':
        prefix = 'SIPM-'
        suffix = ''
        _dict = get_element_names(family_data, element = 'pulsed_magnets',  prefix=prefix, suffix=suffix)
        return _dict

    if subsystem.lower() == 'siti':
        _dict = {
                'SITI-KICKERINJ-ENABLED':{},
                'SITI-KICKERINJ-DELAY':{},
                'SITI-PMM-ENABLED':{},
                'SITI-PMM-DELAY':{},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_family_names(accelerator, family = None, prefix = '', suffix =''):

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

    if family.lower() == 'bend':
        _dict = { prefix + 'BEND-FAM' + suffix :
            {'b1' : family_data['b1']['index'],
             'b2' : family_data['b2']['index'],
            }
        }
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
        _dict = {prefix + 'BPM-FAM'+ suffix: {'bpm': indices}}
        return _dict

    if family.lower() == 'qfa':
        indices = family_data['qfa']['index']
        _dict = {prefix + 'QFA-FAM' + suffix: {'qfa' : indices}}
        return _dict

    if family.lower() == 'qda':
        indices = family_data['qda']['index']
        _dict = {prefix + 'QDA-FAM' + suffix: {'qda' : indices}}
        return _dict

    if family.lower() == 'qdb2':
        indices = family_data['qdb2']['index']
        _dict = {prefix + 'QDB2-FAM' + suffix: {'qdb2' : indices}}
        return _dict

    if family.lower() == 'qfb':
        indices = family_data['qfb']['index']
        _dict = {prefix + 'QFB-FAM' + suffix: {'qfb' : indices}}
        return _dict

    if family.lower() == 'qdb1':
        indices = family_data['qdb1']['index']
        _dict = {prefix + 'QDB1-FAM' + suffix: {'qdb1' : indices}}
        return _dict

    if family.lower() == 'qdp2':
        indices = family_data['qdp2']['index']
        _dict = {prefix + 'QDP2-FAM' + suffix: {'qdp2' : indices}}
        return _dict

    if family.lower() == 'qfp':
        indices = family_data['qfp']['index']
        _dict = {prefix + 'QFP-FAM' + suffix: {'qfp' : indices}}
        return _dict

    if family.lower() == 'qdp1':
        indices = family_data['qdp1']['index']
        _dict = {prefix + 'QDP1-FAM' + suffix: {'qdp1' : indices}}
        return _dict

    if family.lower() == 'q1':
        indices = family_data['q1']['index']
        _dict = {prefix + 'Q1-FAM' + suffix: {'q1' : indices}}
        return _dict

    if family.lower() == 'q2':
        indices = family_data['q2']['index']
        _dict = {prefix + 'Q2-FAM' + suffix: {'q2' : indices}}
        return _dict

    if family.lower() == 'q3':
        indices = family_data['q3']['index']
        _dict = {prefix + 'Q3-FAM' + suffix: {'q3' : indices}}
        return _dict

    if family.lower() == 'q4':
        indices = family_data['q4']['index']
        _dict = {prefix + 'Q4-FAM' + suffix: {'q4' : indices}}
        return _dict

    if family.lower() == 'sda0':
        indices = family_data['sda0']['index']
        _dict = {prefix + 'SDA0-FAM' + suffix: {'sda0' : indices}}
        return _dict

    if family.lower() == 'sdb0':
        indices = family_data['sdb0']['index']
        _dict = {prefix + 'SDB0-FAM' + suffix: {'sdb0' : indices}}
        return _dict

    if family.lower() == 'sdp0':
        indices = family_data['sdp0']['index']
        _dict = {prefix + 'SDP0-FAM' + suffix: {'sdp0' : indices}}
        return _dict

    if family.lower() == 'sda1':
        indices = family_data['sda1']['index']
        _dict = {prefix + 'SDA1-FAM' + suffix: {'sda1' : indices}}
        return _dict

    if family.lower() == 'sdb1':
        indices = family_data['sdb1']['index']
        _dict = {prefix + 'SDB1-FAM' + suffix: {'sdb1' : indices}}
        return _dict

    if family.lower() == 'sdp1':
        indices = family_data['sdp1']['index']
        _dict = {prefix + 'SDP1-FAM' + suffix: {'sdp1' : indices}}
        return _dict

    if family.lower() == 'sda2':
        indices = family_data['sda2']['index']
        _dict = {prefix + 'SDA2-FAM' + suffix: {'sda2' : indices}}
        return _dict

    if family.lower() == 'sdb2':
        indices = family_data['sdb2']['index']
        _dict = {prefix + 'SDB2-FAM' + suffix: {'sdb2' : indices}}
        return _dict

    if family.lower() == 'sdp2':
        indices = family_data['sdp2']['index']
        _dict = {prefix + 'SDP2-FAM' + suffix: {'sdp2' : indices}}
        return _dict

    if family.lower() == 'sda3':
        indices = family_data['sda3']['index']
        _dict = {prefix + 'SDA3-FAM' + suffix: {'sda3' : indices}}
        return _dict

    if family.lower() == 'sdb3':
        indices = family_data['sdb3']['index']
        _dict = {prefix + 'SDB3-FAM' + suffix: {'sdb3' : indices}}
        return _dict

    if family.lower() == 'sdp3':
        indices = family_data['sdp3']['index']
        _dict = {prefix + 'SDP3-FAM' + suffix: {'sdp3' : indices}}
        return _dict

    if family.lower() == 'sfa0':
        indices = family_data['sfa0']['index']
        _dict = {prefix + 'SFA0-FAM' + suffix: {'sfa0' : indices}}
        return _dict

    if family.lower() == 'sfb0':
        indices = family_data['sfb0']['index']
        _dict = {prefix + 'SFB0-FAM' + suffix: {'sfb0' : indices}}
        return _dict

    if family.lower() == 'sfp0':
        indices = family_data['sfp0']['index']
        _dict = {prefix + 'SFP0-FAM' + suffix: {'sfp0' : indices}}
        return _dict

    if family.lower() == 'sfa1':
        indices = family_data['sfa1']['index']
        _dict = {prefix + 'SFA1-FAM' + suffix: {'sfa1' : indices}}
        return _dict

    if family.lower() == 'sfb1':
        indices = family_data['sfb1']['index']
        _dict = {prefix + 'SFB1-FAM' + suffix: {'sfb1' : indices}}
        return _dict

    if family.lower() == 'sfp1':
        indices = family_data['sfp1']['index']
        _dict = {prefix + 'SFP1-FAM' + suffix: {'sfp1' : indices}}
        return _dict

    if family.lower() == 'sfa2':
        indices = family_data['sfa2']['index']
        _dict = {prefix + 'SFA2-FAM' + suffix: {'sfa2' : indices}}
        return _dict

    if family.lower() == 'sfb2':
        indices = family_data['sfb2']['index']
        _dict = {prefix + 'SFB2-FAM' + suffix: {'sfb2' : indices}}
        return _dict

    if family.lower() == 'sfp2':
        indices = family_data['sfp2']['index']
        _dict = {prefix + 'SFP2-FAM' + suffix: {'sfp2' : indices}}
        return _dict

    else:
        raise Exception('Family %s not found'%family)


def get_element_names(accelerator, element = None, prefix = '', suffix = ''):

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
        elements += _families.families_skew_correctors()
        elements += _families.families_pulsed_magnets()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'bend':
        _dict = {}
        _dict.update(get_element_names(family_data, 'b1', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, 'b2', prefix=prefix, suffix=suffix))
        _dict.update(get_element_names(family_data, 'bc', prefix=prefix, suffix=suffix))
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
        elements = _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'hcorr':
        elements = _families.families_horizontal_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'vcorr':
        elements = _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'pulsed_magnets':
        elements = _families.families_pulsed_magnets()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix=prefix, suffix=suffix))
        return _dict

    if element.lower() == 'b1':
        prefix = prefix + 'B1-'
        _dict = {
            prefix + '01-A' + suffix : { 'b1' : [family_data['b1']['index'][0]]},
            prefix + '01-B' + suffix : { 'b1' : [family_data['b1']['index'][1]]},
            prefix + '02-A' + suffix : { 'b1' : [family_data['b1']['index'][2]]},
            prefix + '02-B' + suffix : { 'b1' : [family_data['b1']['index'][3]]},
            prefix + '03-A' + suffix : { 'b1' : [family_data['b1']['index'][4]]},
            prefix + '03-B' + suffix : { 'b1' : [family_data['b1']['index'][5]]},
            prefix + '04-A' + suffix : { 'b1' : [family_data['b1']['index'][6]]},
            prefix + '04-B' + suffix : { 'b1' : [family_data['b1']['index'][7]]},
            prefix + '05-A' + suffix : { 'b1' : [family_data['b1']['index'][8]]},
            prefix + '05-B' + suffix : { 'b1' : [family_data['b1']['index'][9]]},
            prefix + '06-A' + suffix : { 'b1' : [family_data['b1']['index'][10]]},
            prefix + '06-B' + suffix : { 'b1' : [family_data['b1']['index'][11]]},
            prefix + '07-A' + suffix : { 'b1' : [family_data['b1']['index'][12]]},
            prefix + '07-B' + suffix : { 'b1' : [family_data['b1']['index'][13]]},
            prefix + '08-A' + suffix : { 'b1' : [family_data['b1']['index'][14]]},
            prefix + '08-B' + suffix : { 'b1' : [family_data['b1']['index'][15]]},
            prefix + '09-A' + suffix : { 'b1' : [family_data['b1']['index'][16]]},
            prefix + '09-B' + suffix : { 'b1' : [family_data['b1']['index'][17]]},
            prefix + '10-A' + suffix : { 'b1' : [family_data['b1']['index'][18]]},
            prefix + '10-B' + suffix : { 'b1' : [family_data['b1']['index'][19]]},
            prefix + '11-A' + suffix : { 'b1' : [family_data['b1']['index'][20]]},
            prefix + '11-B' + suffix : { 'b1' : [family_data['b1']['index'][21]]},
            prefix + '12-A' + suffix : { 'b1' : [family_data['b1']['index'][22]]},
            prefix + '12-B' + suffix : { 'b1' : [family_data['b1']['index'][23]]},
            prefix + '13-A' + suffix : { 'b1' : [family_data['b1']['index'][24]]},
            prefix + '13-B' + suffix : { 'b1' : [family_data['b1']['index'][25]]},
            prefix + '14-A' + suffix : { 'b1' : [family_data['b1']['index'][26]]},
            prefix + '14-B' + suffix : { 'b1' : [family_data['b1']['index'][27]]},
            prefix + '15-A' + suffix : { 'b1' : [family_data['b1']['index'][28]]},
            prefix + '15-B' + suffix : { 'b1' : [family_data['b1']['index'][29]]},
            prefix + '16-A' + suffix : { 'b1' : [family_data['b1']['index'][30]]},
            prefix + '16-B' + suffix : { 'b1' : [family_data['b1']['index'][31]]},
            prefix + '17-A' + suffix : { 'b1' : [family_data['b1']['index'][32]]},
            prefix + '17-B' + suffix : { 'b1' : [family_data['b1']['index'][33]]},
            prefix + '18-A' + suffix : { 'b1' : [family_data['b1']['index'][34]]},
            prefix + '18-B' + suffix : { 'b1' : [family_data['b1']['index'][35]]},
            prefix + '19-A' + suffix : { 'b1' : [family_data['b1']['index'][36]]},
            prefix + '19-B' + suffix : { 'b1' : [family_data['b1']['index'][37]]},
            prefix + '20-A' + suffix : { 'b1' : [family_data['b1']['index'][38]]},
            prefix + '20-B' + suffix : { 'b1' : [family_data['b1']['index'][39]]},
        }
        return _dict

    if element.lower() == 'b2':
        prefix = prefix + 'B2-'
        _dict = {
            prefix + '01-A' + suffix : { 'b2' : [family_data['b2']['index'][0]]},
            prefix + '01-B' + suffix : { 'b2' : [family_data['b2']['index'][1]]},
            prefix + '02-A' + suffix : { 'b2' : [family_data['b2']['index'][2]]},
            prefix + '02-B' + suffix : { 'b2' : [family_data['b2']['index'][3]]},
            prefix + '03-A' + suffix : { 'b2' : [family_data['b2']['index'][4]]},
            prefix + '03-B' + suffix : { 'b2' : [family_data['b2']['index'][5]]},
            prefix + '04-A' + suffix : { 'b2' : [family_data['b2']['index'][6]]},
            prefix + '04-B' + suffix : { 'b2' : [family_data['b2']['index'][7]]},
            prefix + '05-A' + suffix : { 'b2' : [family_data['b2']['index'][8]]},
            prefix + '05-B' + suffix : { 'b2' : [family_data['b2']['index'][9]]},
            prefix + '06-A' + suffix : { 'b2' : [family_data['b2']['index'][10]]},
            prefix + '06-B' + suffix : { 'b2' : [family_data['b2']['index'][11]]},
            prefix + '07-A' + suffix : { 'b2' : [family_data['b2']['index'][12]]},
            prefix + '07-B' + suffix : { 'b2' : [family_data['b2']['index'][13]]},
            prefix + '08-A' + suffix : { 'b2' : [family_data['b2']['index'][14]]},
            prefix + '08-B' + suffix : { 'b2' : [family_data['b2']['index'][15]]},
            prefix + '09-A' + suffix : { 'b2' : [family_data['b2']['index'][16]]},
            prefix + '09-B' + suffix : { 'b2' : [family_data['b2']['index'][17]]},
            prefix + '10-A' + suffix : { 'b2' : [family_data['b2']['index'][18]]},
            prefix + '10-B' + suffix : { 'b2' : [family_data['b2']['index'][19]]},
            prefix + '11-A' + suffix : { 'b2' : [family_data['b2']['index'][20]]},
            prefix + '11-B' + suffix : { 'b2' : [family_data['b2']['index'][21]]},
            prefix + '12-A' + suffix : { 'b2' : [family_data['b2']['index'][22]]},
            prefix + '12-B' + suffix : { 'b2' : [family_data['b2']['index'][23]]},
            prefix + '13-A' + suffix : { 'b2' : [family_data['b2']['index'][24]]},
            prefix + '13-B' + suffix : { 'b2' : [family_data['b2']['index'][25]]},
            prefix + '14-A' + suffix : { 'b2' : [family_data['b2']['index'][26]]},
            prefix + '14-B' + suffix : { 'b2' : [family_data['b2']['index'][27]]},
            prefix + '15-A' + suffix : { 'b2' : [family_data['b2']['index'][28]]},
            prefix + '15-B' + suffix : { 'b2' : [family_data['b2']['index'][29]]},
            prefix + '16-A' + suffix : { 'b2' : [family_data['b2']['index'][30]]},
            prefix + '16-B' + suffix : { 'b2' : [family_data['b2']['index'][31]]},
            prefix + '17-A' + suffix : { 'b2' : [family_data['b2']['index'][32]]},
            prefix + '17-B' + suffix : { 'b2' : [family_data['b2']['index'][33]]},
            prefix + '18-A' + suffix : { 'b2' : [family_data['b2']['index'][34]]},
            prefix + '18-B' + suffix : { 'b2' : [family_data['b2']['index'][35]]},
            prefix + '19-A' + suffix : { 'b2' : [family_data['b2']['index'][36]]},
            prefix + '19-B' + suffix : { 'b2' : [family_data['b2']['index'][37]]},
            prefix + '20-A' + suffix : { 'b2' : [family_data['b2']['index'][38]]},
            prefix + '20-B' + suffix : { 'b2' : [family_data['b2']['index'][39]]},
        }
        return _dict

    if element.lower() == 'bpm':
        prefix = prefix + 'BPM-'
        _dict = {
            prefix + '01M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][0]]},
            prefix + '01C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][1]]},
            prefix + '01C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][2]]},
            prefix + '01C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][3]]},
            prefix + '01C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][4]]},
            prefix + '01C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][5]]},
            prefix + '01C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][6]]},
            prefix + '02M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][7]]},
            prefix + '02M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][8]]},
            prefix + '02C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][9]]},
            prefix + '02C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][10]]},
            prefix + '02C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][11]]},
            prefix + '02C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][12]]},
            prefix + '02C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][13]]},
            prefix + '02C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][14]]},
            prefix + '03M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][15]]},
            prefix + '03M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][16]]},
            prefix + '03C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][17]]},
            prefix + '03C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][18]]},
            prefix + '03C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][19]]},
            prefix + '03C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][20]]},
            prefix + '03C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][21]]},
            prefix + '03C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][22]]},
            prefix + '04M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][23]]},
            prefix + '04M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][24]]},
            prefix + '04C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][25]]},
            prefix + '04C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][26]]},
            prefix + '04C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][27]]},
            prefix + '04C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][28]]},
            prefix + '04C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][29]]},
            prefix + '04C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][30]]},
            prefix + '05M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][31]]},
            prefix + '05M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][32]]},
            prefix + '05C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][33]]},
            prefix + '05C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][34]]},
            prefix + '05C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][35]]},
            prefix + '05C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][36]]},
            prefix + '05C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][37]]},
            prefix + '05C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][38]]},
            prefix + '06M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][39]]},
            prefix + '06M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][40]]},
            prefix + '06C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][41]]},
            prefix + '06C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][42]]},
            prefix + '06C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][43]]},
            prefix + '06C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][44]]},
            prefix + '06C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][45]]},
            prefix + '06C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][46]]},
            prefix + '07M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][47]]},
            prefix + '07M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][48]]},
            prefix + '07C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][49]]},
            prefix + '07C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][50]]},
            prefix + '07C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][51]]},
            prefix + '07C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][52]]},
            prefix + '07C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][53]]},
            prefix + '07C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][54]]},
            prefix + '08M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][55]]},
            prefix + '08M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][56]]},
            prefix + '08C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][57]]},
            prefix + '08C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][58]]},
            prefix + '08C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][59]]},
            prefix + '08C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][60]]},
            prefix + '08C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][61]]},
            prefix + '08C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][62]]},
            prefix + '09M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][63]]},
            prefix + '09M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][64]]},
            prefix + '09C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][65]]},
            prefix + '09C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][66]]},
            prefix + '09C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][67]]},
            prefix + '09C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][68]]},
            prefix + '09C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][69]]},
            prefix + '09C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][70]]},
            prefix + '10M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][71]]},
            prefix + '10M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][72]]},
            prefix + '10C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][73]]},
            prefix + '10C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][74]]},
            prefix + '10C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][75]]},
            prefix + '10C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][76]]},
            prefix + '10C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][77]]},
            prefix + '10C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][78]]},
            prefix + '11M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][79]]},
            prefix + '11M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][80]]},
            prefix + '11C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][81]]},
            prefix + '11C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][82]]},
            prefix + '11C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][83]]},
            prefix + '11C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][84]]},
            prefix + '11C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][85]]},
            prefix + '11C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][86]]},
            prefix + '12M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][87]]},
            prefix + '12M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][88]]},
            prefix + '12C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][89]]},
            prefix + '12C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][90]]},
            prefix + '12C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][91]]},
            prefix + '12C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][92]]},
            prefix + '12C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][93]]},
            prefix + '12C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][94]]},
            prefix + '13M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][95]]},
            prefix + '13M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][96]]},
            prefix + '13C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][97]]},
            prefix + '13C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][98]]},
            prefix + '13C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][99]]},
            prefix + '13C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][100]]},
            prefix + '13C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][101]]},
            prefix + '13C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][102]]},
            prefix + '14M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][103]]},
            prefix + '14M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][104]]},
            prefix + '14C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][105]]},
            prefix + '14C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][106]]},
            prefix + '14C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][107]]},
            prefix + '14C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][108]]},
            prefix + '14C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][109]]},
            prefix + '14C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][110]]},
            prefix + '15M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][111]]},
            prefix + '15M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][112]]},
            prefix + '15C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][113]]},
            prefix + '15C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][114]]},
            prefix + '15C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][115]]},
            prefix + '15C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][116]]},
            prefix + '15C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][117]]},
            prefix + '15C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][118]]},
            prefix + '16M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][119]]},
            prefix + '16M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][120]]},
            prefix + '16C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][121]]},
            prefix + '16C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][122]]},
            prefix + '16C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][123]]},
            prefix + '16C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][124]]},
            prefix + '16C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][125]]},
            prefix + '16C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][126]]},
            prefix + '17M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][127]]},
            prefix + '17M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][128]]},
            prefix + '17C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][129]]},
            prefix + '17C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][130]]},
            prefix + '17C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][131]]},
            prefix + '17C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][132]]},
            prefix + '17C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][133]]},
            prefix + '17C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][134]]},
            prefix + '18M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][135]]},
            prefix + '18M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][136]]},
            prefix + '18C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][137]]},
            prefix + '18C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][138]]},
            prefix + '18C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][139]]},
            prefix + '18C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][140]]},
            prefix + '18C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][141]]},
            prefix + '18C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][142]]},
            prefix + '19M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][143]]},
            prefix + '19M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][144]]},
            prefix + '19C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][145]]},
            prefix + '19C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][146]]},
            prefix + '19C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][147]]},
            prefix + '19C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][148]]},
            prefix + '19C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][149]]},
            prefix + '19C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][150]]},
            prefix + '20M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][151]]},
            prefix + '20M2'   + suffix : { 'bpm' : [family_data['bpm']['index'][152]]},
            prefix + '20C1-A' + suffix : { 'bpm' : [family_data['bpm']['index'][153]]},
            prefix + '20C1-B' + suffix : { 'bpm' : [family_data['bpm']['index'][154]]},
            prefix + '20C2'   + suffix : { 'bpm' : [family_data['bpm']['index'][155]]},
            prefix + '20C3-A' + suffix : { 'bpm' : [family_data['bpm']['index'][156]]},
            prefix + '20C3-B' + suffix : { 'bpm' : [family_data['bpm']['index'][157]]},
            prefix + '20C4'   + suffix : { 'bpm' : [family_data['bpm']['index'][158]]},
            prefix + '01M1'   + suffix : { 'bpm' : [family_data['bpm']['index'][159]]},
        }
        return _dict


    if element.lower() == 'bc':
        prefix = prefix + 'BC-'
        _dict = {
            prefix + '01' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][0]] + [family_data['bc_hf']['index'][0]])},
            prefix + '02' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][1]] + [family_data['bc_hf']['index'][1]])},
            prefix + '03' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][2]] + [family_data['bc_hf']['index'][2]])},
            prefix + '04' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][3]] + [family_data['bc_hf']['index'][3]])},
            prefix + '05' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][4]] + [family_data['bc_hf']['index'][4]])},
            prefix + '06' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][5]] + [family_data['bc_hf']['index'][5]])},
            prefix + '07' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][6]] + [family_data['bc_hf']['index'][6]])},
            prefix + '08' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][7]] + [family_data['bc_hf']['index'][7]])},
            prefix + '09' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][8]] + [family_data['bc_hf']['index'][8]])},
            prefix + '10' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][9]] + [family_data['bc_hf']['index'][9]])},
            prefix + '11' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][10]] + [family_data['bc_hf']['index'][10]])},
            prefix + '12' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][11]] + [family_data['bc_hf']['index'][11]])},
            prefix + '13' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][12]] + [family_data['bc_hf']['index'][12]])},
            prefix + '14' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][13]] + [family_data['bc_hf']['index'][13]])},
            prefix + '15' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][14]] + [family_data['bc_hf']['index'][14]])},
            prefix + '16' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][15]] + [family_data['bc_hf']['index'][15]])},
            prefix + '17' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][16]] + [family_data['bc_hf']['index'][16]])},
            prefix + '18' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][17]] + [family_data['bc_hf']['index'][17]])},
            prefix + '19' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][18]] + [family_data['bc_hf']['index'][18]])},
            prefix + '20' + suffix : {'bc' : sorted([family_data['bc_lf']['index'][19]] + [family_data['bc_hf']['index'][19]])},
        }
        return _dict


    if element.lower() == 'fch':
        prefix = prefix + 'FCH-'
        _dict = {
            prefix + '01M2' + suffix : { 'fch' : [family_data['fch']['index'][0]]},
            prefix + '01C2' + suffix : { 'fch' : [family_data['fch']['index'][1]]},
            prefix + '01C3' + suffix : { 'fch' : [family_data['fch']['index'][2]]},
            prefix + '02M1' + suffix : { 'fch' : [family_data['fch']['index'][3]]},
            prefix + '02M2' + suffix : { 'fch' : [family_data['fch']['index'][4]]},
            prefix + '02C2' + suffix : { 'fch' : [family_data['fch']['index'][5]]},
            prefix + '02C3' + suffix : { 'fch' : [family_data['fch']['index'][6]]},
            prefix + '03M1' + suffix : { 'fch' : [family_data['fch']['index'][7]]},
            prefix + '03M2' + suffix : { 'fch' : [family_data['fch']['index'][8]]},
            prefix + '03C2' + suffix : { 'fch' : [family_data['fch']['index'][9]]},
            prefix + '03C3' + suffix : { 'fch' : [family_data['fch']['index'][10]]},
            prefix + '04M1' + suffix : { 'fch' : [family_data['fch']['index'][11]]},
            prefix + '04M2' + suffix : { 'fch' : [family_data['fch']['index'][12]]},
            prefix + '04C2' + suffix : { 'fch' : [family_data['fch']['index'][13]]},
            prefix + '04C3' + suffix : { 'fch' : [family_data['fch']['index'][14]]},
            prefix + '05M1' + suffix : { 'fch' : [family_data['fch']['index'][15]]},
            prefix + '05M2' + suffix : { 'fch' : [family_data['fch']['index'][16]]},
            prefix + '05C2' + suffix : { 'fch' : [family_data['fch']['index'][17]]},
            prefix + '05C3' + suffix : { 'fch' : [family_data['fch']['index'][18]]},
            prefix + '06M1' + suffix : { 'fch' : [family_data['fch']['index'][19]]},
            prefix + '06M2' + suffix : { 'fch' : [family_data['fch']['index'][20]]},
            prefix + '06C2' + suffix : { 'fch' : [family_data['fch']['index'][21]]},
            prefix + '06C3' + suffix : { 'fch' : [family_data['fch']['index'][22]]},
            prefix + '07M1' + suffix : { 'fch' : [family_data['fch']['index'][23]]},
            prefix + '07M2' + suffix : { 'fch' : [family_data['fch']['index'][24]]},
            prefix + '07C2' + suffix : { 'fch' : [family_data['fch']['index'][25]]},
            prefix + '07C3' + suffix : { 'fch' : [family_data['fch']['index'][26]]},
            prefix + '08M1' + suffix : { 'fch' : [family_data['fch']['index'][27]]},
            prefix + '08M2' + suffix : { 'fch' : [family_data['fch']['index'][28]]},
            prefix + '08C2' + suffix : { 'fch' : [family_data['fch']['index'][29]]},
            prefix + '08C3' + suffix : { 'fch' : [family_data['fch']['index'][30]]},
            prefix + '09M1' + suffix : { 'fch' : [family_data['fch']['index'][31]]},
            prefix + '09M2' + suffix : { 'fch' : [family_data['fch']['index'][32]]},
            prefix + '09C2' + suffix : { 'fch' : [family_data['fch']['index'][33]]},
            prefix + '09C3' + suffix : { 'fch' : [family_data['fch']['index'][34]]},
            prefix + '10M1' + suffix : { 'fch' : [family_data['fch']['index'][35]]},
            prefix + '10M2' + suffix : { 'fch' : [family_data['fch']['index'][36]]},
            prefix + '10C2' + suffix : { 'fch' : [family_data['fch']['index'][37]]},
            prefix + '10C3' + suffix : { 'fch' : [family_data['fch']['index'][38]]},
            prefix + '11M1' + suffix : { 'fch' : [family_data['fch']['index'][39]]},
            prefix + '11M2' + suffix : { 'fch' : [family_data['fch']['index'][40]]},
            prefix + '11C2' + suffix : { 'fch' : [family_data['fch']['index'][41]]},
            prefix + '11C3' + suffix : { 'fch' : [family_data['fch']['index'][42]]},
            prefix + '12M1' + suffix : { 'fch' : [family_data['fch']['index'][43]]},
            prefix + '12M2' + suffix : { 'fch' : [family_data['fch']['index'][44]]},
            prefix + '12C2' + suffix : { 'fch' : [family_data['fch']['index'][45]]},
            prefix + '12C3' + suffix : { 'fch' : [family_data['fch']['index'][46]]},
            prefix + '13M1' + suffix : { 'fch' : [family_data['fch']['index'][47]]},
            prefix + '13M2' + suffix : { 'fch' : [family_data['fch']['index'][48]]},
            prefix + '13C2' + suffix : { 'fch' : [family_data['fch']['index'][49]]},
            prefix + '13C3' + suffix : { 'fch' : [family_data['fch']['index'][50]]},
            prefix + '14M1' + suffix : { 'fch' : [family_data['fch']['index'][51]]},
            prefix + '14M2' + suffix : { 'fch' : [family_data['fch']['index'][52]]},
            prefix + '14C2' + suffix : { 'fch' : [family_data['fch']['index'][53]]},
            prefix + '14C3' + suffix : { 'fch' : [family_data['fch']['index'][54]]},
            prefix + '15M1' + suffix : { 'fch' : [family_data['fch']['index'][55]]},
            prefix + '15M2' + suffix : { 'fch' : [family_data['fch']['index'][56]]},
            prefix + '15C2' + suffix : { 'fch' : [family_data['fch']['index'][57]]},
            prefix + '15C3' + suffix : { 'fch' : [family_data['fch']['index'][58]]},
            prefix + '16M1' + suffix : { 'fch' : [family_data['fch']['index'][59]]},
            prefix + '16M2' + suffix : { 'fch' : [family_data['fch']['index'][60]]},
            prefix + '16C2' + suffix : { 'fch' : [family_data['fch']['index'][61]]},
            prefix + '16C3' + suffix : { 'fch' : [family_data['fch']['index'][62]]},
            prefix + '17M1' + suffix : { 'fch' : [family_data['fch']['index'][63]]},
            prefix + '17M2' + suffix : { 'fch' : [family_data['fch']['index'][64]]},
            prefix + '17C2' + suffix : { 'fch' : [family_data['fch']['index'][65]]},
            prefix + '17C3' + suffix : { 'fch' : [family_data['fch']['index'][66]]},
            prefix + '18M1' + suffix : { 'fch' : [family_data['fch']['index'][67]]},
            prefix + '18M2' + suffix : { 'fch' : [family_data['fch']['index'][68]]},
            prefix + '18C2' + suffix : { 'fch' : [family_data['fch']['index'][69]]},
            prefix + '18C3' + suffix : { 'fch' : [family_data['fch']['index'][70]]},
            prefix + '19M1' + suffix : { 'fch' : [family_data['fch']['index'][71]]},
            prefix + '19M2' + suffix : { 'fch' : [family_data['fch']['index'][72]]},
            prefix + '19C2' + suffix : { 'fch' : [family_data['fch']['index'][73]]},
            prefix + '19C3' + suffix : { 'fch' : [family_data['fch']['index'][74]]},
            prefix + '20M1' + suffix : { 'fch' : [family_data['fch']['index'][75]]},
            prefix + '20M2' + suffix : { 'fch' : [family_data['fch']['index'][76]]},
            prefix + '20C2' + suffix : { 'fch' : [family_data['fch']['index'][77]]},
            prefix + '20C3' + suffix : { 'fch' : [family_data['fch']['index'][78]]},
            prefix + '01M1' + suffix : { 'fch' : [family_data['fch']['index'][79]]},
        }
        return _dict

    if element.lower() == 'cv':
        prefix = prefix + 'CV-'
        _dict = {
            prefix + '01M2'   + suffix : { 'cv' : [family_data['cv']['index'][0]]},
            prefix + '01C1'   + suffix : { 'cv' : [family_data['cv']['index'][1]]},
            prefix + '01C2-A' + suffix : { 'cv' : [family_data['cv']['index'][2]]},
            prefix + '01C2-B' + suffix : { 'cv' : [family_data['cv']['index'][3]]},
            prefix + '01C3-A' + suffix : { 'cv' : [family_data['cv']['index'][4]]},
            prefix + '01C3-B' + suffix : { 'cv' : [family_data['cv']['index'][5]]},
            prefix + '01C4'   + suffix : { 'cv' : [family_data['cv']['index'][6]]},
            prefix + '02M1'   + suffix : { 'cv' : [family_data['cv']['index'][7]]},
            prefix + '02M2'   + suffix : { 'cv' : [family_data['cv']['index'][8]]},
            prefix + '02C1'   + suffix : { 'cv' : [family_data['cv']['index'][9]]},
            prefix + '02C2-A' + suffix : { 'cv' : [family_data['cv']['index'][10]]},
            prefix + '02C2-B' + suffix : { 'cv' : [family_data['cv']['index'][11]]},
            prefix + '02C3-A' + suffix : { 'cv' : [family_data['cv']['index'][12]]},
            prefix + '02C3-B' + suffix : { 'cv' : [family_data['cv']['index'][13]]},
            prefix + '02C4'   + suffix : { 'cv' : [family_data['cv']['index'][14]]},
            prefix + '03M1'   + suffix : { 'cv' : [family_data['cv']['index'][15]]},
            prefix + '03M2'   + suffix : { 'cv' : [family_data['cv']['index'][16]]},
            prefix + '03C1'   + suffix : { 'cv' : [family_data['cv']['index'][17]]},
            prefix + '03C2-A' + suffix : { 'cv' : [family_data['cv']['index'][18]]},
            prefix + '03C2-B' + suffix : { 'cv' : [family_data['cv']['index'][19]]},
            prefix + '03C3-A' + suffix : { 'cv' : [family_data['cv']['index'][20]]},
            prefix + '03C3-B' + suffix : { 'cv' : [family_data['cv']['index'][21]]},
            prefix + '03C4'   + suffix : { 'cv' : [family_data['cv']['index'][22]]},
            prefix + '04M1'   + suffix : { 'cv' : [family_data['cv']['index'][23]]},
            prefix + '04M2'   + suffix : { 'cv' : [family_data['cv']['index'][24]]},
            prefix + '04C1'   + suffix : { 'cv' : [family_data['cv']['index'][25]]},
            prefix + '04C2-A' + suffix : { 'cv' : [family_data['cv']['index'][26]]},
            prefix + '04C2-B' + suffix : { 'cv' : [family_data['cv']['index'][27]]},
            prefix + '04C3-A' + suffix : { 'cv' : [family_data['cv']['index'][28]]},
            prefix + '04C3-B' + suffix : { 'cv' : [family_data['cv']['index'][29]]},
            prefix + '04C4'   + suffix : { 'cv' : [family_data['cv']['index'][30]]},
            prefix + '05M1'   + suffix : { 'cv' : [family_data['cv']['index'][31]]},
            prefix + '05M2'   + suffix : { 'cv' : [family_data['cv']['index'][32]]},
            prefix + '05C1'   + suffix : { 'cv' : [family_data['cv']['index'][33]]},
            prefix + '05C2-A' + suffix : { 'cv' : [family_data['cv']['index'][34]]},
            prefix + '05C2-B' + suffix : { 'cv' : [family_data['cv']['index'][35]]},
            prefix + '05C3-A' + suffix : { 'cv' : [family_data['cv']['index'][36]]},
            prefix + '05C3-B' + suffix : { 'cv' : [family_data['cv']['index'][37]]},
            prefix + '05C4'   + suffix : { 'cv' : [family_data['cv']['index'][38]]},
            prefix + '06M1'   + suffix : { 'cv' : [family_data['cv']['index'][39]]},
            prefix + '06M2'   + suffix : { 'cv' : [family_data['cv']['index'][40]]},
            prefix + '06C1'   + suffix : { 'cv' : [family_data['cv']['index'][41]]},
            prefix + '06C2-A' + suffix : { 'cv' : [family_data['cv']['index'][42]]},
            prefix + '06C2-B' + suffix : { 'cv' : [family_data['cv']['index'][43]]},
            prefix + '06C3-A' + suffix : { 'cv' : [family_data['cv']['index'][44]]},
            prefix + '06C3-B' + suffix : { 'cv' : [family_data['cv']['index'][45]]},
            prefix + '06C4'   + suffix : { 'cv' : [family_data['cv']['index'][46]]},
            prefix + '07M1'   + suffix : { 'cv' : [family_data['cv']['index'][47]]},
            prefix + '07M2'   + suffix : { 'cv' : [family_data['cv']['index'][48]]},
            prefix + '07C1'   + suffix : { 'cv' : [family_data['cv']['index'][49]]},
            prefix + '07C2-A' + suffix : { 'cv' : [family_data['cv']['index'][50]]},
            prefix + '07C2-B' + suffix : { 'cv' : [family_data['cv']['index'][51]]},
            prefix + '07C3-A' + suffix : { 'cv' : [family_data['cv']['index'][52]]},
            prefix + '07C3-B' + suffix : { 'cv' : [family_data['cv']['index'][53]]},
            prefix + '07C4'   + suffix : { 'cv' : [family_data['cv']['index'][54]]},
            prefix + '08M1'   + suffix : { 'cv' : [family_data['cv']['index'][55]]},
            prefix + '08M2'   + suffix : { 'cv' : [family_data['cv']['index'][56]]},
            prefix + '08C1'   + suffix : { 'cv' : [family_data['cv']['index'][57]]},
            prefix + '08C2-A' + suffix : { 'cv' : [family_data['cv']['index'][58]]},
            prefix + '08C2-B' + suffix : { 'cv' : [family_data['cv']['index'][59]]},
            prefix + '08C3-A' + suffix : { 'cv' : [family_data['cv']['index'][60]]},
            prefix + '08C3-B' + suffix : { 'cv' : [family_data['cv']['index'][61]]},
            prefix + '08C4'   + suffix : { 'cv' : [family_data['cv']['index'][62]]},
            prefix + '09M1'   + suffix : { 'cv' : [family_data['cv']['index'][63]]},
            prefix + '09M2'   + suffix : { 'cv' : [family_data['cv']['index'][64]]},
            prefix + '09C1'   + suffix : { 'cv' : [family_data['cv']['index'][65]]},
            prefix + '09C2-A' + suffix : { 'cv' : [family_data['cv']['index'][66]]},
            prefix + '09C2-B' + suffix : { 'cv' : [family_data['cv']['index'][67]]},
            prefix + '09C3-A' + suffix : { 'cv' : [family_data['cv']['index'][68]]},
            prefix + '09C3-B' + suffix : { 'cv' : [family_data['cv']['index'][69]]},
            prefix + '09C4'   + suffix : { 'cv' : [family_data['cv']['index'][70]]},
            prefix + '10M1'   + suffix : { 'cv' : [family_data['cv']['index'][71]]},
            prefix + '10M2'   + suffix : { 'cv' : [family_data['cv']['index'][72]]},
            prefix + '10C1'   + suffix : { 'cv' : [family_data['cv']['index'][73]]},
            prefix + '10C2-A' + suffix : { 'cv' : [family_data['cv']['index'][74]]},
            prefix + '10C2-B' + suffix : { 'cv' : [family_data['cv']['index'][75]]},
            prefix + '10C3-A' + suffix : { 'cv' : [family_data['cv']['index'][76]]},
            prefix + '10C3-B' + suffix : { 'cv' : [family_data['cv']['index'][77]]},
            prefix + '10C4'   + suffix : { 'cv' : [family_data['cv']['index'][78]]},
            prefix + '11M1'   + suffix : { 'cv' : [family_data['cv']['index'][79]]},
            prefix + '11M2'   + suffix : { 'cv' : [family_data['cv']['index'][80]]},
            prefix + '11C1'   + suffix : { 'cv' : [family_data['cv']['index'][81]]},
            prefix + '11C2-A' + suffix : { 'cv' : [family_data['cv']['index'][82]]},
            prefix + '11C2-B' + suffix : { 'cv' : [family_data['cv']['index'][83]]},
            prefix + '11C3-A' + suffix : { 'cv' : [family_data['cv']['index'][84]]},
            prefix + '11C3-B' + suffix : { 'cv' : [family_data['cv']['index'][85]]},
            prefix + '11C4'   + suffix : { 'cv' : [family_data['cv']['index'][86]]},
            prefix + '12M1'   + suffix : { 'cv' : [family_data['cv']['index'][87]]},
            prefix + '12M2'   + suffix : { 'cv' : [family_data['cv']['index'][88]]},
            prefix + '12C1'   + suffix : { 'cv' : [family_data['cv']['index'][89]]},
            prefix + '12C2-A' + suffix : { 'cv' : [family_data['cv']['index'][90]]},
            prefix + '12C2-B' + suffix : { 'cv' : [family_data['cv']['index'][91]]},
            prefix + '12C3-A' + suffix : { 'cv' : [family_data['cv']['index'][92]]},
            prefix + '12C3-B' + suffix : { 'cv' : [family_data['cv']['index'][93]]},
            prefix + '12C4'   + suffix : { 'cv' : [family_data['cv']['index'][94]]},
            prefix + '13M1'   + suffix : { 'cv' : [family_data['cv']['index'][95]]},
            prefix + '13M2'   + suffix : { 'cv' : [family_data['cv']['index'][96]]},
            prefix + '13C1'   + suffix : { 'cv' : [family_data['cv']['index'][97]]},
            prefix + '13C2-A' + suffix : { 'cv' : [family_data['cv']['index'][98]]},
            prefix + '13C2-B' + suffix : { 'cv' : [family_data['cv']['index'][99]]},
            prefix + '13C3-A' + suffix : { 'cv' : [family_data['cv']['index'][100]]},
            prefix + '13C3-B' + suffix : { 'cv' : [family_data['cv']['index'][101]]},
            prefix + '13C4'   + suffix : { 'cv' : [family_data['cv']['index'][102]]},
            prefix + '14M1'   + suffix : { 'cv' : [family_data['cv']['index'][103]]},
            prefix + '14M2'   + suffix : { 'cv' : [family_data['cv']['index'][104]]},
            prefix + '14C1'   + suffix : { 'cv' : [family_data['cv']['index'][105]]},
            prefix + '14C2-A' + suffix : { 'cv' : [family_data['cv']['index'][106]]},
            prefix + '14C2-B' + suffix : { 'cv' : [family_data['cv']['index'][107]]},
            prefix + '14C3-A' + suffix : { 'cv' : [family_data['cv']['index'][108]]},
            prefix + '14C3-B' + suffix : { 'cv' : [family_data['cv']['index'][109]]},
            prefix + '14C4'   + suffix : { 'cv' : [family_data['cv']['index'][110]]},
            prefix + '15M1'   + suffix : { 'cv' : [family_data['cv']['index'][111]]},
            prefix + '15M2'   + suffix : { 'cv' : [family_data['cv']['index'][112]]},
            prefix + '15C1'   + suffix : { 'cv' : [family_data['cv']['index'][113]]},
            prefix + '15C2-A' + suffix : { 'cv' : [family_data['cv']['index'][114]]},
            prefix + '15C2-B' + suffix : { 'cv' : [family_data['cv']['index'][115]]},
            prefix + '15C3-A' + suffix : { 'cv' : [family_data['cv']['index'][116]]},
            prefix + '15C3-B' + suffix : { 'cv' : [family_data['cv']['index'][117]]},
            prefix + '15C4'   + suffix : { 'cv' : [family_data['cv']['index'][118]]},
            prefix + '16M1'   + suffix : { 'cv' : [family_data['cv']['index'][119]]},
            prefix + '16M2'   + suffix : { 'cv' : [family_data['cv']['index'][120]]},
            prefix + '16C1'   + suffix : { 'cv' : [family_data['cv']['index'][121]]},
            prefix + '16C2-A' + suffix : { 'cv' : [family_data['cv']['index'][122]]},
            prefix + '16C2-B' + suffix : { 'cv' : [family_data['cv']['index'][123]]},
            prefix + '16C3-A' + suffix : { 'cv' : [family_data['cv']['index'][124]]},
            prefix + '16C3-B' + suffix : { 'cv' : [family_data['cv']['index'][125]]},
            prefix + '16C4'   + suffix : { 'cv' : [family_data['cv']['index'][126]]},
            prefix + '17M1'   + suffix : { 'cv' : [family_data['cv']['index'][127]]},
            prefix + '17M2'   + suffix : { 'cv' : [family_data['cv']['index'][128]]},
            prefix + '17C1'   + suffix : { 'cv' : [family_data['cv']['index'][129]]},
            prefix + '17C2-A' + suffix : { 'cv' : [family_data['cv']['index'][130]]},
            prefix + '17C2-B' + suffix : { 'cv' : [family_data['cv']['index'][131]]},
            prefix + '17C3-A' + suffix : { 'cv' : [family_data['cv']['index'][132]]},
            prefix + '17C3-B' + suffix : { 'cv' : [family_data['cv']['index'][133]]},
            prefix + '17C4'   + suffix : { 'cv' : [family_data['cv']['index'][134]]},
            prefix + '18M1'   + suffix : { 'cv' : [family_data['cv']['index'][135]]},
            prefix + '18M2'   + suffix : { 'cv' : [family_data['cv']['index'][136]]},
            prefix + '18C1'   + suffix : { 'cv' : [family_data['cv']['index'][137]]},
            prefix + '18C2-A' + suffix : { 'cv' : [family_data['cv']['index'][138]]},
            prefix + '18C2-B' + suffix : { 'cv' : [family_data['cv']['index'][139]]},
            prefix + '18C3-A' + suffix : { 'cv' : [family_data['cv']['index'][140]]},
            prefix + '18C3-B' + suffix : { 'cv' : [family_data['cv']['index'][141]]},
            prefix + '18C4'   + suffix : { 'cv' : [family_data['cv']['index'][142]]},
            prefix + '19M1'   + suffix : { 'cv' : [family_data['cv']['index'][143]]},
            prefix + '19M2'   + suffix : { 'cv' : [family_data['cv']['index'][144]]},
            prefix + '19C1'   + suffix : { 'cv' : [family_data['cv']['index'][145]]},
            prefix + '19C2-A' + suffix : { 'cv' : [family_data['cv']['index'][146]]},
            prefix + '19C2-B' + suffix : { 'cv' : [family_data['cv']['index'][147]]},
            prefix + '19C3-A' + suffix : { 'cv' : [family_data['cv']['index'][148]]},
            prefix + '19C3-B' + suffix : { 'cv' : [family_data['cv']['index'][149]]},
            prefix + '19C4'   + suffix : { 'cv' : [family_data['cv']['index'][150]]},
            prefix + '20M1'   + suffix : { 'cv' : [family_data['cv']['index'][151]]},
            prefix + '20M2'   + suffix : { 'cv' : [family_data['cv']['index'][152]]},
            prefix + '20C1'   + suffix : { 'cv' : [family_data['cv']['index'][153]]},
            prefix + '20C2-A' + suffix : { 'cv' : [family_data['cv']['index'][154]]},
            prefix + '20C2-B' + suffix : { 'cv' : [family_data['cv']['index'][155]]},
            prefix + '20C3-A' + suffix : { 'cv' : [family_data['cv']['index'][156]]},
            prefix + '20C3-B' + suffix : { 'cv' : [family_data['cv']['index'][157]]},
            prefix + '20C4'   + suffix : { 'cv' : [family_data['cv']['index'][158]]},
            prefix + '01M1'   + suffix : { 'cv' : [family_data['cv']['index'][159]]},
        }
        return _dict

    if element.lower() == 'qs':
        prefix = prefix + 'QS-'
        _dict = {
            prefix + '01M2' + suffix : { 'qs' : [family_data['qs']['index'][0]]},
            prefix + '01C1' + suffix : { 'qs' : [family_data['qs']['index'][1]]},
            prefix + '01C4' + suffix : { 'qs' : [family_data['qs']['index'][2]]},
            prefix + '02M1' + suffix : { 'qs' : [family_data['qs']['index'][3]]},
            prefix + '02M2' + suffix : { 'qs' : [family_data['qs']['index'][4]]},
            prefix + '02C1' + suffix : { 'qs' : [family_data['qs']['index'][5]]},
            prefix + '02C4' + suffix : { 'qs' : [family_data['qs']['index'][6]]},
            prefix + '03M1' + suffix : { 'qs' : [family_data['qs']['index'][7]]},
            prefix + '03M2' + suffix : { 'qs' : [family_data['qs']['index'][8]]},
            prefix + '03C1' + suffix : { 'qs' : [family_data['qs']['index'][9]]},
            prefix + '03C4' + suffix : { 'qs' : [family_data['qs']['index'][10]]},
            prefix + '04M1' + suffix : { 'qs' : [family_data['qs']['index'][11]]},
            prefix + '04M2' + suffix : { 'qs' : [family_data['qs']['index'][12]]},
            prefix + '04C1' + suffix : { 'qs' : [family_data['qs']['index'][13]]},
            prefix + '04C4' + suffix : { 'qs' : [family_data['qs']['index'][14]]},
            prefix + '05M1' + suffix : { 'qs' : [family_data['qs']['index'][15]]},
            prefix + '05M2' + suffix : { 'qs' : [family_data['qs']['index'][16]]},
            prefix + '05C1' + suffix : { 'qs' : [family_data['qs']['index'][17]]},
            prefix + '05C4' + suffix : { 'qs' : [family_data['qs']['index'][18]]},
            prefix + '06M1' + suffix : { 'qs' : [family_data['qs']['index'][19]]},
            prefix + '06M2' + suffix : { 'qs' : [family_data['qs']['index'][20]]},
            prefix + '06C1' + suffix : { 'qs' : [family_data['qs']['index'][21]]},
            prefix + '06C4' + suffix : { 'qs' : [family_data['qs']['index'][22]]},
            prefix + '07M1' + suffix : { 'qs' : [family_data['qs']['index'][23]]},
            prefix + '07M2' + suffix : { 'qs' : [family_data['qs']['index'][24]]},
            prefix + '07C1' + suffix : { 'qs' : [family_data['qs']['index'][25]]},
            prefix + '07C4' + suffix : { 'qs' : [family_data['qs']['index'][26]]},
            prefix + '08M1' + suffix : { 'qs' : [family_data['qs']['index'][27]]},
            prefix + '08M2' + suffix : { 'qs' : [family_data['qs']['index'][28]]},
            prefix + '08C1' + suffix : { 'qs' : [family_data['qs']['index'][29]]},
            prefix + '08C4' + suffix : { 'qs' : [family_data['qs']['index'][30]]},
            prefix + '09M1' + suffix : { 'qs' : [family_data['qs']['index'][31]]},
            prefix + '09M2' + suffix : { 'qs' : [family_data['qs']['index'][32]]},
            prefix + '09C1' + suffix : { 'qs' : [family_data['qs']['index'][33]]},
            prefix + '09C4' + suffix : { 'qs' : [family_data['qs']['index'][34]]},
            prefix + '10M1' + suffix : { 'qs' : [family_data['qs']['index'][35]]},
            prefix + '10M2' + suffix : { 'qs' : [family_data['qs']['index'][36]]},
            prefix + '10C1' + suffix : { 'qs' : [family_data['qs']['index'][37]]},
            prefix + '10C4' + suffix : { 'qs' : [family_data['qs']['index'][38]]},
            prefix + '11M1' + suffix : { 'qs' : [family_data['qs']['index'][39]]},
            prefix + '11M2' + suffix : { 'qs' : [family_data['qs']['index'][40]]},
            prefix + '11C1' + suffix : { 'qs' : [family_data['qs']['index'][41]]},
            prefix + '11C4' + suffix : { 'qs' : [family_data['qs']['index'][42]]},
            prefix + '12M1' + suffix : { 'qs' : [family_data['qs']['index'][43]]},
            prefix + '12M2' + suffix : { 'qs' : [family_data['qs']['index'][44]]},
            prefix + '12C1' + suffix : { 'qs' : [family_data['qs']['index'][45]]},
            prefix + '12C4' + suffix : { 'qs' : [family_data['qs']['index'][46]]},
            prefix + '13M1' + suffix : { 'qs' : [family_data['qs']['index'][47]]},
            prefix + '13M2' + suffix : { 'qs' : [family_data['qs']['index'][48]]},
            prefix + '13C1' + suffix : { 'qs' : [family_data['qs']['index'][49]]},
            prefix + '13C4' + suffix : { 'qs' : [family_data['qs']['index'][50]]},
            prefix + '14M1' + suffix : { 'qs' : [family_data['qs']['index'][51]]},
            prefix + '14M2' + suffix : { 'qs' : [family_data['qs']['index'][52]]},
            prefix + '14C1' + suffix : { 'qs' : [family_data['qs']['index'][53]]},
            prefix + '14C4' + suffix : { 'qs' : [family_data['qs']['index'][54]]},
            prefix + '15M1' + suffix : { 'qs' : [family_data['qs']['index'][55]]},
            prefix + '15M2' + suffix : { 'qs' : [family_data['qs']['index'][56]]},
            prefix + '15C1' + suffix : { 'qs' : [family_data['qs']['index'][57]]},
            prefix + '15C4' + suffix : { 'qs' : [family_data['qs']['index'][58]]},
            prefix + '16M1' + suffix : { 'qs' : [family_data['qs']['index'][59]]},
            prefix + '16M2' + suffix : { 'qs' : [family_data['qs']['index'][60]]},
            prefix + '16C1' + suffix : { 'qs' : [family_data['qs']['index'][61]]},
            prefix + '16C4' + suffix : { 'qs' : [family_data['qs']['index'][62]]},
            prefix + '17M1' + suffix : { 'qs' : [family_data['qs']['index'][63]]},
            prefix + '17M2' + suffix : { 'qs' : [family_data['qs']['index'][64]]},
            prefix + '17C1' + suffix : { 'qs' : [family_data['qs']['index'][65]]},
            prefix + '17C4' + suffix : { 'qs' : [family_data['qs']['index'][66]]},
            prefix + '18M1' + suffix : { 'qs' : [family_data['qs']['index'][67]]},
            prefix + '18M2' + suffix : { 'qs' : [family_data['qs']['index'][68]]},
            prefix + '18C1' + suffix : { 'qs' : [family_data['qs']['index'][69]]},
            prefix + '18C4' + suffix : { 'qs' : [family_data['qs']['index'][70]]},
            prefix + '19M1' + suffix : { 'qs' : [family_data['qs']['index'][71]]},
            prefix + '19M2' + suffix : { 'qs' : [family_data['qs']['index'][72]]},
            prefix + '19C1' + suffix : { 'qs' : [family_data['qs']['index'][73]]},
            prefix + '19C4' + suffix : { 'qs' : [family_data['qs']['index'][74]]},
            prefix + '20M1' + suffix : { 'qs' : [family_data['qs']['index'][75]]},
            prefix + '20M2' + suffix : { 'qs' : [family_data['qs']['index'][76]]},
            prefix + '20C1' + suffix : { 'qs' : [family_data['qs']['index'][77]]},
            prefix + '20C4' + suffix : { 'qs' : [family_data['qs']['index'][78]]},
            prefix + '01M1' + suffix : { 'qs' : [family_data['qs']['index'][79]]},
        }
        return _dict

    if element.lower() == 'ch':
        prefix = prefix + 'CH-'
        _dict = {
            prefix + '01M2' + suffix : { 'ch' : [family_data['ch']['index'][0]]},
            prefix + '01C1' + suffix : { 'ch' : [family_data['ch']['index'][1]]},
            prefix + '01C2' + suffix : { 'ch' : [family_data['ch']['index'][2]]},
            prefix + '01C3' + suffix : { 'ch' : [family_data['ch']['index'][3]]},
            prefix + '01C4' + suffix : { 'ch' : [family_data['ch']['index'][4]]},
            prefix + '02M1' + suffix : { 'ch' : [family_data['ch']['index'][5]]},
            prefix + '02M2' + suffix : { 'ch' : [family_data['ch']['index'][6]]},
            prefix + '02C1' + suffix : { 'ch' : [family_data['ch']['index'][7]]},
            prefix + '02C2' + suffix : { 'ch' : [family_data['ch']['index'][8]]},
            prefix + '02C3' + suffix : { 'ch' : [family_data['ch']['index'][9]]},
            prefix + '02C4' + suffix : { 'ch' : [family_data['ch']['index'][10]]},
            prefix + '03M1' + suffix : { 'ch' : [family_data['ch']['index'][11]]},
            prefix + '03M2' + suffix : { 'ch' : [family_data['ch']['index'][12]]},
            prefix + '03C1' + suffix : { 'ch' : [family_data['ch']['index'][13]]},
            prefix + '03C2' + suffix : { 'ch' : [family_data['ch']['index'][14]]},
            prefix + '03C3' + suffix : { 'ch' : [family_data['ch']['index'][15]]},
            prefix + '03C4' + suffix : { 'ch' : [family_data['ch']['index'][16]]},
            prefix + '04M1' + suffix : { 'ch' : [family_data['ch']['index'][17]]},
            prefix + '04M2' + suffix : { 'ch' : [family_data['ch']['index'][18]]},
            prefix + '04C1' + suffix : { 'ch' : [family_data['ch']['index'][19]]},
            prefix + '04C2' + suffix : { 'ch' : [family_data['ch']['index'][20]]},
            prefix + '04C3' + suffix : { 'ch' : [family_data['ch']['index'][21]]},
            prefix + '04C4' + suffix : { 'ch' : [family_data['ch']['index'][22]]},
            prefix + '05M1' + suffix : { 'ch' : [family_data['ch']['index'][23]]},
            prefix + '05M2' + suffix : { 'ch' : [family_data['ch']['index'][24]]},
            prefix + '05C1' + suffix : { 'ch' : [family_data['ch']['index'][25]]},
            prefix + '05C2' + suffix : { 'ch' : [family_data['ch']['index'][26]]},
            prefix + '05C3' + suffix : { 'ch' : [family_data['ch']['index'][27]]},
            prefix + '05C4' + suffix : { 'ch' : [family_data['ch']['index'][28]]},
            prefix + '06M1' + suffix : { 'ch' : [family_data['ch']['index'][29]]},
            prefix + '06M2' + suffix : { 'ch' : [family_data['ch']['index'][30]]},
            prefix + '06C1' + suffix : { 'ch' : [family_data['ch']['index'][31]]},
            prefix + '06C2' + suffix : { 'ch' : [family_data['ch']['index'][32]]},
            prefix + '06C3' + suffix : { 'ch' : [family_data['ch']['index'][33]]},
            prefix + '06C4' + suffix : { 'ch' : [family_data['ch']['index'][34]]},
            prefix + '07M1' + suffix : { 'ch' : [family_data['ch']['index'][35]]},
            prefix + '07M2' + suffix : { 'ch' : [family_data['ch']['index'][36]]},
            prefix + '07C1' + suffix : { 'ch' : [family_data['ch']['index'][37]]},
            prefix + '07C2' + suffix : { 'ch' : [family_data['ch']['index'][38]]},
            prefix + '07C3' + suffix : { 'ch' : [family_data['ch']['index'][39]]},
            prefix + '07C4' + suffix : { 'ch' : [family_data['ch']['index'][40]]},
            prefix + '08M1' + suffix : { 'ch' : [family_data['ch']['index'][41]]},
            prefix + '08M2' + suffix : { 'ch' : [family_data['ch']['index'][42]]},
            prefix + '08C1' + suffix : { 'ch' : [family_data['ch']['index'][43]]},
            prefix + '08C2' + suffix : { 'ch' : [family_data['ch']['index'][44]]},
            prefix + '08C3' + suffix : { 'ch' : [family_data['ch']['index'][45]]},
            prefix + '08C4' + suffix : { 'ch' : [family_data['ch']['index'][46]]},
            prefix + '09M1' + suffix : { 'ch' : [family_data['ch']['index'][47]]},
            prefix + '09M2' + suffix : { 'ch' : [family_data['ch']['index'][48]]},
            prefix + '09C1' + suffix : { 'ch' : [family_data['ch']['index'][49]]},
            prefix + '09C2' + suffix : { 'ch' : [family_data['ch']['index'][50]]},
            prefix + '09C3' + suffix : { 'ch' : [family_data['ch']['index'][51]]},
            prefix + '09C4' + suffix : { 'ch' : [family_data['ch']['index'][52]]},
            prefix + '10M1' + suffix : { 'ch' : [family_data['ch']['index'][53]]},
            prefix + '10M2' + suffix : { 'ch' : [family_data['ch']['index'][54]]},
            prefix + '10C1' + suffix : { 'ch' : [family_data['ch']['index'][55]]},
            prefix + '10C2' + suffix : { 'ch' : [family_data['ch']['index'][56]]},
            prefix + '10C3' + suffix : { 'ch' : [family_data['ch']['index'][57]]},
            prefix + '10C4' + suffix : { 'ch' : [family_data['ch']['index'][58]]},
            prefix + '11M1' + suffix : { 'ch' : [family_data['ch']['index'][59]]},
            prefix + '11M2' + suffix : { 'ch' : [family_data['ch']['index'][60]]},
            prefix + '11C1' + suffix : { 'ch' : [family_data['ch']['index'][61]]},
            prefix + '11C2' + suffix : { 'ch' : [family_data['ch']['index'][62]]},
            prefix + '11C3' + suffix : { 'ch' : [family_data['ch']['index'][63]]},
            prefix + '11C4' + suffix : { 'ch' : [family_data['ch']['index'][64]]},
            prefix + '12M1' + suffix : { 'ch' : [family_data['ch']['index'][65]]},
            prefix + '12M2' + suffix : { 'ch' : [family_data['ch']['index'][66]]},
            prefix + '12C1' + suffix : { 'ch' : [family_data['ch']['index'][67]]},
            prefix + '12C2' + suffix : { 'ch' : [family_data['ch']['index'][68]]},
            prefix + '12C3' + suffix : { 'ch' : [family_data['ch']['index'][69]]},
            prefix + '12C4' + suffix : { 'ch' : [family_data['ch']['index'][70]]},
            prefix + '13M1' + suffix : { 'ch' : [family_data['ch']['index'][71]]},
            prefix + '13M2' + suffix : { 'ch' : [family_data['ch']['index'][72]]},
            prefix + '13C1' + suffix : { 'ch' : [family_data['ch']['index'][73]]},
            prefix + '13C2' + suffix : { 'ch' : [family_data['ch']['index'][74]]},
            prefix + '13C3' + suffix : { 'ch' : [family_data['ch']['index'][75]]},
            prefix + '13C4' + suffix : { 'ch' : [family_data['ch']['index'][76]]},
            prefix + '14M1' + suffix : { 'ch' : [family_data['ch']['index'][77]]},
            prefix + '14M2' + suffix : { 'ch' : [family_data['ch']['index'][78]]},
            prefix + '14C1' + suffix : { 'ch' : [family_data['ch']['index'][79]]},
            prefix + '14C2' + suffix : { 'ch' : [family_data['ch']['index'][80]]},
            prefix + '14C3' + suffix : { 'ch' : [family_data['ch']['index'][81]]},
            prefix + '14C4' + suffix : { 'ch' : [family_data['ch']['index'][82]]},
            prefix + '15M1' + suffix : { 'ch' : [family_data['ch']['index'][83]]},
            prefix + '15M2' + suffix : { 'ch' : [family_data['ch']['index'][84]]},
            prefix + '15C1' + suffix : { 'ch' : [family_data['ch']['index'][85]]},
            prefix + '15C2' + suffix : { 'ch' : [family_data['ch']['index'][86]]},
            prefix + '15C3' + suffix : { 'ch' : [family_data['ch']['index'][87]]},
            prefix + '15C4' + suffix : { 'ch' : [family_data['ch']['index'][88]]},
            prefix + '16M1' + suffix : { 'ch' : [family_data['ch']['index'][89]]},
            prefix + '16M2' + suffix : { 'ch' : [family_data['ch']['index'][90]]},
            prefix + '16C1' + suffix : { 'ch' : [family_data['ch']['index'][91]]},
            prefix + '16C2' + suffix : { 'ch' : [family_data['ch']['index'][92]]},
            prefix + '16C3' + suffix : { 'ch' : [family_data['ch']['index'][93]]},
            prefix + '16C4' + suffix : { 'ch' : [family_data['ch']['index'][94]]},
            prefix + '17M1' + suffix : { 'ch' : [family_data['ch']['index'][95]]},
            prefix + '17M2' + suffix : { 'ch' : [family_data['ch']['index'][96]]},
            prefix + '17C1' + suffix : { 'ch' : [family_data['ch']['index'][97]]},
            prefix + '17C2' + suffix : { 'ch' : [family_data['ch']['index'][98]]},
            prefix + '17C3' + suffix : { 'ch' : [family_data['ch']['index'][99]]},
            prefix + '17C4' + suffix : { 'ch' : [family_data['ch']['index'][100]]},
            prefix + '18M1' + suffix : { 'ch' : [family_data['ch']['index'][101]]},
            prefix + '18M2' + suffix : { 'ch' : [family_data['ch']['index'][102]]},
            prefix + '18C1' + suffix : { 'ch' : [family_data['ch']['index'][103]]},
            prefix + '18C2' + suffix : { 'ch' : [family_data['ch']['index'][104]]},
            prefix + '18C3' + suffix : { 'ch' : [family_data['ch']['index'][105]]},
            prefix + '18C4' + suffix : { 'ch' : [family_data['ch']['index'][106]]},
            prefix + '19M1' + suffix : { 'ch' : [family_data['ch']['index'][107]]},
            prefix + '19M2' + suffix : { 'ch' : [family_data['ch']['index'][108]]},
            prefix + '19C1' + suffix : { 'ch' : [family_data['ch']['index'][109]]},
            prefix + '19C2' + suffix : { 'ch' : [family_data['ch']['index'][110]]},
            prefix + '19C3' + suffix : { 'ch' : [family_data['ch']['index'][111]]},
            prefix + '19C4' + suffix : { 'ch' : [family_data['ch']['index'][112]]},
            prefix + '20M1' + suffix : { 'ch' : [family_data['ch']['index'][113]]},
            prefix + '20M2' + suffix : { 'ch' : [family_data['ch']['index'][114]]},
            prefix + '20C1' + suffix : { 'ch' : [family_data['ch']['index'][115]]},
            prefix + '20C2' + suffix : { 'ch' : [family_data['ch']['index'][116]]},
            prefix + '20C3' + suffix : { 'ch' : [family_data['ch']['index'][117]]},
            prefix + '20C4' + suffix : { 'ch' : [family_data['ch']['index'][118]]},
            prefix + '01M1' + suffix : { 'ch' : [family_data['ch']['index'][119]]},
        }
        return _dict

    if element.lower() == 'fcv':
        prefix = prefix + 'FCV-'
        _dict = {
            prefix + '01M2' + suffix : { 'fcv' : [family_data['fcv']['index'][0]]},
            prefix + '01C2' + suffix : { 'fcv' : [family_data['fcv']['index'][1]]},
            prefix + '01C3' + suffix : { 'fcv' : [family_data['fcv']['index'][2]]},
            prefix + '02M1' + suffix : { 'fcv' : [family_data['fcv']['index'][3]]},
            prefix + '02M2' + suffix : { 'fcv' : [family_data['fcv']['index'][4]]},
            prefix + '02C2' + suffix : { 'fcv' : [family_data['fcv']['index'][5]]},
            prefix + '02C3' + suffix : { 'fcv' : [family_data['fcv']['index'][6]]},
            prefix + '03M1' + suffix : { 'fcv' : [family_data['fcv']['index'][7]]},
            prefix + '03M2' + suffix : { 'fcv' : [family_data['fcv']['index'][8]]},
            prefix + '03C2' + suffix : { 'fcv' : [family_data['fcv']['index'][9]]},
            prefix + '03C3' + suffix : { 'fcv' : [family_data['fcv']['index'][10]]},
            prefix + '04M1' + suffix : { 'fcv' : [family_data['fcv']['index'][11]]},
            prefix + '04M2' + suffix : { 'fcv' : [family_data['fcv']['index'][12]]},
            prefix + '04C2' + suffix : { 'fcv' : [family_data['fcv']['index'][13]]},
            prefix + '04C3' + suffix : { 'fcv' : [family_data['fcv']['index'][14]]},
            prefix + '05M1' + suffix : { 'fcv' : [family_data['fcv']['index'][15]]},
            prefix + '05M2' + suffix : { 'fcv' : [family_data['fcv']['index'][16]]},
            prefix + '05C2' + suffix : { 'fcv' : [family_data['fcv']['index'][17]]},
            prefix + '05C3' + suffix : { 'fcv' : [family_data['fcv']['index'][18]]},
            prefix + '06M1' + suffix : { 'fcv' : [family_data['fcv']['index'][19]]},
            prefix + '06M2' + suffix : { 'fcv' : [family_data['fcv']['index'][20]]},
            prefix + '06C2' + suffix : { 'fcv' : [family_data['fcv']['index'][21]]},
            prefix + '06C3' + suffix : { 'fcv' : [family_data['fcv']['index'][22]]},
            prefix + '07M1' + suffix : { 'fcv' : [family_data['fcv']['index'][23]]},
            prefix + '07M2' + suffix : { 'fcv' : [family_data['fcv']['index'][24]]},
            prefix + '07C2' + suffix : { 'fcv' : [family_data['fcv']['index'][25]]},
            prefix + '07C3' + suffix : { 'fcv' : [family_data['fcv']['index'][26]]},
            prefix + '08M1' + suffix : { 'fcv' : [family_data['fcv']['index'][27]]},
            prefix + '08M2' + suffix : { 'fcv' : [family_data['fcv']['index'][28]]},
            prefix + '08C2' + suffix : { 'fcv' : [family_data['fcv']['index'][29]]},
            prefix + '08C3' + suffix : { 'fcv' : [family_data['fcv']['index'][30]]},
            prefix + '09M1' + suffix : { 'fcv' : [family_data['fcv']['index'][31]]},
            prefix + '09M2' + suffix : { 'fcv' : [family_data['fcv']['index'][32]]},
            prefix + '09C2' + suffix : { 'fcv' : [family_data['fcv']['index'][33]]},
            prefix + '09C3' + suffix : { 'fcv' : [family_data['fcv']['index'][34]]},
            prefix + '10M1' + suffix : { 'fcv' : [family_data['fcv']['index'][35]]},
            prefix + '10M2' + suffix : { 'fcv' : [family_data['fcv']['index'][36]]},
            prefix + '10C2' + suffix : { 'fcv' : [family_data['fcv']['index'][37]]},
            prefix + '10C3' + suffix : { 'fcv' : [family_data['fcv']['index'][38]]},
            prefix + '11M1' + suffix : { 'fcv' : [family_data['fcv']['index'][39]]},
            prefix + '11M2' + suffix : { 'fcv' : [family_data['fcv']['index'][40]]},
            prefix + '11C2' + suffix : { 'fcv' : [family_data['fcv']['index'][41]]},
            prefix + '11C3' + suffix : { 'fcv' : [family_data['fcv']['index'][42]]},
            prefix + '12M1' + suffix : { 'fcv' : [family_data['fcv']['index'][43]]},
            prefix + '12M2' + suffix : { 'fcv' : [family_data['fcv']['index'][44]]},
            prefix + '12C2' + suffix : { 'fcv' : [family_data['fcv']['index'][45]]},
            prefix + '12C3' + suffix : { 'fcv' : [family_data['fcv']['index'][46]]},
            prefix + '13M1' + suffix : { 'fcv' : [family_data['fcv']['index'][47]]},
            prefix + '13M2' + suffix : { 'fcv' : [family_data['fcv']['index'][48]]},
            prefix + '13C2' + suffix : { 'fcv' : [family_data['fcv']['index'][49]]},
            prefix + '13C3' + suffix : { 'fcv' : [family_data['fcv']['index'][50]]},
            prefix + '14M1' + suffix : { 'fcv' : [family_data['fcv']['index'][51]]},
            prefix + '14M2' + suffix : { 'fcv' : [family_data['fcv']['index'][52]]},
            prefix + '14C2' + suffix : { 'fcv' : [family_data['fcv']['index'][53]]},
            prefix + '14C3' + suffix : { 'fcv' : [family_data['fcv']['index'][54]]},
            prefix + '15M1' + suffix : { 'fcv' : [family_data['fcv']['index'][55]]},
            prefix + '15M2' + suffix : { 'fcv' : [family_data['fcv']['index'][56]]},
            prefix + '15C2' + suffix : { 'fcv' : [family_data['fcv']['index'][57]]},
            prefix + '15C3' + suffix : { 'fcv' : [family_data['fcv']['index'][58]]},
            prefix + '16M1' + suffix : { 'fcv' : [family_data['fcv']['index'][59]]},
            prefix + '16M2' + suffix : { 'fcv' : [family_data['fcv']['index'][60]]},
            prefix + '16C2' + suffix : { 'fcv' : [family_data['fcv']['index'][61]]},
            prefix + '16C3' + suffix : { 'fcv' : [family_data['fcv']['index'][62]]},
            prefix + '17M1' + suffix : { 'fcv' : [family_data['fcv']['index'][63]]},
            prefix + '17M2' + suffix : { 'fcv' : [family_data['fcv']['index'][64]]},
            prefix + '17C2' + suffix : { 'fcv' : [family_data['fcv']['index'][65]]},
            prefix + '17C3' + suffix : { 'fcv' : [family_data['fcv']['index'][66]]},
            prefix + '18M1' + suffix : { 'fcv' : [family_data['fcv']['index'][67]]},
            prefix + '18M2' + suffix : { 'fcv' : [family_data['fcv']['index'][68]]},
            prefix + '18C2' + suffix : { 'fcv' : [family_data['fcv']['index'][69]]},
            prefix + '18C3' + suffix : { 'fcv' : [family_data['fcv']['index'][70]]},
            prefix + '19M1' + suffix : { 'fcv' : [family_data['fcv']['index'][71]]},
            prefix + '19M2' + suffix : { 'fcv' : [family_data['fcv']['index'][72]]},
            prefix + '19C2' + suffix : { 'fcv' : [family_data['fcv']['index'][73]]},
            prefix + '19C3' + suffix : { 'fcv' : [family_data['fcv']['index'][74]]},
            prefix + '20M1' + suffix : { 'fcv' : [family_data['fcv']['index'][75]]},
            prefix + '20M2' + suffix : { 'fcv' : [family_data['fcv']['index'][76]]},
            prefix + '20C2' + suffix : { 'fcv' : [family_data['fcv']['index'][77]]},
            prefix + '20C3' + suffix : { 'fcv' : [family_data['fcv']['index'][78]]},
            prefix + '01M1' + suffix : { 'fcv' : [family_data['fcv']['index'][79]]},
        }
        return _dict


    if element.lower() == 'fc':
        prefix = prefix + 'FC-'
        _dict = {
            prefix + '01M2' + suffix : { 'fc' : [family_data['fc']['index'][0]]},
            prefix + '01C2' + suffix : { 'fc' : [family_data['fc']['index'][1]]},
            prefix + '01C3' + suffix : { 'fc' : [family_data['fc']['index'][2]]},
            prefix + '02M1' + suffix : { 'fc' : [family_data['fc']['index'][3]]},
            prefix + '02M2' + suffix : { 'fc' : [family_data['fc']['index'][4]]},
            prefix + '02C2' + suffix : { 'fc' : [family_data['fc']['index'][5]]},
            prefix + '02C3' + suffix : { 'fc' : [family_data['fc']['index'][6]]},
            prefix + '03M1' + suffix : { 'fc' : [family_data['fc']['index'][7]]},
            prefix + '03M2' + suffix : { 'fc' : [family_data['fc']['index'][8]]},
            prefix + '03C2' + suffix : { 'fc' : [family_data['fc']['index'][9]]},
            prefix + '03C3' + suffix : { 'fc' : [family_data['fc']['index'][10]]},
            prefix + '04M1' + suffix : { 'fc' : [family_data['fc']['index'][11]]},
            prefix + '04M2' + suffix : { 'fc' : [family_data['fc']['index'][12]]},
            prefix + '04C2' + suffix : { 'fc' : [family_data['fc']['index'][13]]},
            prefix + '04C3' + suffix : { 'fc' : [family_data['fc']['index'][14]]},
            prefix + '05M1' + suffix : { 'fc' : [family_data['fc']['index'][15]]},
            prefix + '05M2' + suffix : { 'fc' : [family_data['fc']['index'][16]]},
            prefix + '05C2' + suffix : { 'fc' : [family_data['fc']['index'][17]]},
            prefix + '05C3' + suffix : { 'fc' : [family_data['fc']['index'][18]]},
            prefix + '06M1' + suffix : { 'fc' : [family_data['fc']['index'][19]]},
            prefix + '06M2' + suffix : { 'fc' : [family_data['fc']['index'][20]]},
            prefix + '06C2' + suffix : { 'fc' : [family_data['fc']['index'][21]]},
            prefix + '06C3' + suffix : { 'fc' : [family_data['fc']['index'][22]]},
            prefix + '07M1' + suffix : { 'fc' : [family_data['fc']['index'][23]]},
            prefix + '07M2' + suffix : { 'fc' : [family_data['fc']['index'][24]]},
            prefix + '07C2' + suffix : { 'fc' : [family_data['fc']['index'][25]]},
            prefix + '07C3' + suffix : { 'fc' : [family_data['fc']['index'][26]]},
            prefix + '08M1' + suffix : { 'fc' : [family_data['fc']['index'][27]]},
            prefix + '08M2' + suffix : { 'fc' : [family_data['fc']['index'][28]]},
            prefix + '08C2' + suffix : { 'fc' : [family_data['fc']['index'][29]]},
            prefix + '08C3' + suffix : { 'fc' : [family_data['fc']['index'][30]]},
            prefix + '09M1' + suffix : { 'fc' : [family_data['fc']['index'][31]]},
            prefix + '09M2' + suffix : { 'fc' : [family_data['fc']['index'][32]]},
            prefix + '09C2' + suffix : { 'fc' : [family_data['fc']['index'][33]]},
            prefix + '09C3' + suffix : { 'fc' : [family_data['fc']['index'][34]]},
            prefix + '10M1' + suffix : { 'fc' : [family_data['fc']['index'][35]]},
            prefix + '10M2' + suffix : { 'fc' : [family_data['fc']['index'][36]]},
            prefix + '10C2' + suffix : { 'fc' : [family_data['fc']['index'][37]]},
            prefix + '10C3' + suffix : { 'fc' : [family_data['fc']['index'][38]]},
            prefix + '11M1' + suffix : { 'fc' : [family_data['fc']['index'][39]]},
            prefix + '11M2' + suffix : { 'fc' : [family_data['fc']['index'][40]]},
            prefix + '11C2' + suffix : { 'fc' : [family_data['fc']['index'][41]]},
            prefix + '11C3' + suffix : { 'fc' : [family_data['fc']['index'][42]]},
            prefix + '12M1' + suffix : { 'fc' : [family_data['fc']['index'][43]]},
            prefix + '12M2' + suffix : { 'fc' : [family_data['fc']['index'][44]]},
            prefix + '12C2' + suffix : { 'fc' : [family_data['fc']['index'][45]]},
            prefix + '12C3' + suffix : { 'fc' : [family_data['fc']['index'][46]]},
            prefix + '13M1' + suffix : { 'fc' : [family_data['fc']['index'][47]]},
            prefix + '13M2' + suffix : { 'fc' : [family_data['fc']['index'][48]]},
            prefix + '13C2' + suffix : { 'fc' : [family_data['fc']['index'][49]]},
            prefix + '13C3' + suffix : { 'fc' : [family_data['fc']['index'][50]]},
            prefix + '14M1' + suffix : { 'fc' : [family_data['fc']['index'][51]]},
            prefix + '14M2' + suffix : { 'fc' : [family_data['fc']['index'][52]]},
            prefix + '14C2' + suffix : { 'fc' : [family_data['fc']['index'][53]]},
            prefix + '14C3' + suffix : { 'fc' : [family_data['fc']['index'][54]]},
            prefix + '15M1' + suffix : { 'fc' : [family_data['fc']['index'][55]]},
            prefix + '15M2' + suffix : { 'fc' : [family_data['fc']['index'][56]]},
            prefix + '15C2' + suffix : { 'fc' : [family_data['fc']['index'][57]]},
            prefix + '15C3' + suffix : { 'fc' : [family_data['fc']['index'][58]]},
            prefix + '16M1' + suffix : { 'fc' : [family_data['fc']['index'][59]]},
            prefix + '16M2' + suffix : { 'fc' : [family_data['fc']['index'][60]]},
            prefix + '16C2' + suffix : { 'fc' : [family_data['fc']['index'][61]]},
            prefix + '16C3' + suffix : { 'fc' : [family_data['fc']['index'][62]]},
            prefix + '17M1' + suffix : { 'fc' : [family_data['fc']['index'][63]]},
            prefix + '17M2' + suffix : { 'fc' : [family_data['fc']['index'][64]]},
            prefix + '17C2' + suffix : { 'fc' : [family_data['fc']['index'][65]]},
            prefix + '17C3' + suffix : { 'fc' : [family_data['fc']['index'][66]]},
            prefix + '18M1' + suffix : { 'fc' : [family_data['fc']['index'][67]]},
            prefix + '18M2' + suffix : { 'fc' : [family_data['fc']['index'][68]]},
            prefix + '18C2' + suffix : { 'fc' : [family_data['fc']['index'][69]]},
            prefix + '18C3' + suffix : { 'fc' : [family_data['fc']['index'][70]]},
            prefix + '19M1' + suffix : { 'fc' : [family_data['fc']['index'][71]]},
            prefix + '19M2' + suffix : { 'fc' : [family_data['fc']['index'][72]]},
            prefix + '19C2' + suffix : { 'fc' : [family_data['fc']['index'][73]]},
            prefix + '19C3' + suffix : { 'fc' : [family_data['fc']['index'][74]]},
            prefix + '20M1' + suffix : { 'fc' : [family_data['fc']['index'][75]]},
            prefix + '20M2' + suffix : { 'fc' : [family_data['fc']['index'][76]]},
            prefix + '20C2' + suffix : { 'fc' : [family_data['fc']['index'][77]]},
            prefix + '20C3' + suffix : { 'fc' : [family_data['fc']['index'][78]]},
            prefix + '01M1' + suffix : { 'fc' : [family_data['fc']['index'][79]]},
        }
        return _dict

    if element.lower() == 'qfa':
        prefix = prefix + 'QFA-'
        _dict = {
            prefix + '01M1' + suffix : { 'qfa' : [family_data['qfa']['index'][0]]},
            prefix + '01M2' + suffix : { 'qfa' : [family_data['qfa']['index'][1]]},
            prefix + '05M1' + suffix : { 'qfa' : [family_data['qfa']['index'][2]]},
            prefix + '05M2' + suffix : { 'qfa' : [family_data['qfa']['index'][3]]},
            prefix + '09M1' + suffix : { 'qfa' : [family_data['qfa']['index'][4]]},
            prefix + '09M2' + suffix : { 'qfa' : [family_data['qfa']['index'][5]]},
            prefix + '13M1' + suffix : { 'qfa' : [family_data['qfa']['index'][6]]},
            prefix + '13M2' + suffix : { 'qfa' : [family_data['qfa']['index'][7]]},
            prefix + '17M1' + suffix : { 'qfa' : [family_data['qfa']['index'][8]]},
            prefix + '17M2' + suffix : { 'qfa' : [family_data['qfa']['index'][9]]},
        }
        return _dict

    if element.lower() == 'qda':
        prefix = prefix + 'QDA-'
        _dict = {
            prefix + '01M1' + suffix : { 'qda' : [family_data['qda']['index'][0]]},
            prefix + '01M2' + suffix : { 'qda' : [family_data['qda']['index'][1]]},
            prefix + '05M1' + suffix : { 'qda' : [family_data['qda']['index'][2]]},
            prefix + '05M2' + suffix : { 'qda' : [family_data['qda']['index'][3]]},
            prefix + '09M1' + suffix : { 'qda' : [family_data['qda']['index'][4]]},
            prefix + '09M2' + suffix : { 'qda' : [family_data['qda']['index'][5]]},
            prefix + '13M1' + suffix : { 'qda' : [family_data['qda']['index'][6]]},
            prefix + '13M2' + suffix : { 'qda' : [family_data['qda']['index'][7]]},
            prefix + '17M1' + suffix : { 'qda' : [family_data['qda']['index'][8]]},
            prefix + '17M2' + suffix : { 'qda' : [family_data['qda']['index'][9]]},
        }
        return _dict

    if element.lower() == 'qdb2':
        prefix = prefix + 'QDB2-'
        _dict = {
            prefix + '02M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][0]]},
            prefix + '02M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][1]]},
            prefix + '04M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][2]]},
            prefix + '04M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][3]]},
            prefix + '06M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][4]]},
            prefix + '06M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][5]]},
            prefix + '08M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][6]]},
            prefix + '08M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][7]]},
            prefix + '10M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][8]]},
            prefix + '10M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][9]]},
            prefix + '12M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][10]]},
            prefix + '12M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][11]]},
            prefix + '14M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][12]]},
            prefix + '14M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][13]]},
            prefix + '16M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][14]]},
            prefix + '16M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][15]]},
            prefix + '18M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][16]]},
            prefix + '18M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][17]]},
            prefix + '20M1' + suffix : { 'qdb2' : [family_data['qdb2']['index'][18]]},
            prefix + '20M2' + suffix : { 'qdb2' : [family_data['qdb2']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qfb':
        prefix = prefix + 'QFB-'
        _dict = {
            prefix + '02M1' + suffix : { 'qfb' : [family_data['qfb']['index'][0]]},
            prefix + '02M2' + suffix : { 'qfb' : [family_data['qfb']['index'][1]]},
            prefix + '04M1' + suffix : { 'qfb' : [family_data['qfb']['index'][2]]},
            prefix + '04M2' + suffix : { 'qfb' : [family_data['qfb']['index'][3]]},
            prefix + '06M1' + suffix : { 'qfb' : [family_data['qfb']['index'][4]]},
            prefix + '06M2' + suffix : { 'qfb' : [family_data['qfb']['index'][5]]},
            prefix + '08M1' + suffix : { 'qfb' : [family_data['qfb']['index'][6]]},
            prefix + '08M2' + suffix : { 'qfb' : [family_data['qfb']['index'][7]]},
            prefix + '10M1' + suffix : { 'qfb' : [family_data['qfb']['index'][8]]},
            prefix + '10M2' + suffix : { 'qfb' : [family_data['qfb']['index'][9]]},
            prefix + '12M1' + suffix : { 'qfb' : [family_data['qfb']['index'][10]]},
            prefix + '12M2' + suffix : { 'qfb' : [family_data['qfb']['index'][11]]},
            prefix + '14M1' + suffix : { 'qfb' : [family_data['qfb']['index'][12]]},
            prefix + '14M2' + suffix : { 'qfb' : [family_data['qfb']['index'][13]]},
            prefix + '16M1' + suffix : { 'qfb' : [family_data['qfb']['index'][14]]},
            prefix + '16M2' + suffix : { 'qfb' : [family_data['qfb']['index'][15]]},
            prefix + '18M1' + suffix : { 'qfb' : [family_data['qfb']['index'][16]]},
            prefix + '18M2' + suffix : { 'qfb' : [family_data['qfb']['index'][17]]},
            prefix + '20M1' + suffix : { 'qfb' : [family_data['qfb']['index'][18]]},
            prefix + '20M2' + suffix : { 'qfb' : [family_data['qfb']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qdb1':
        prefix = prefix + 'QDB1-'
        _dict = {
            prefix + '02M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][0]]},
            prefix + '02M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][1]]},
            prefix + '04M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][2]]},
            prefix + '04M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][3]]},
            prefix + '06M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][4]]},
            prefix + '06M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][5]]},
            prefix + '08M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][6]]},
            prefix + '08M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][7]]},
            prefix + '10M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][8]]},
            prefix + '10M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][9]]},
            prefix + '12M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][10]]},
            prefix + '12M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][11]]},
            prefix + '14M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][12]]},
            prefix + '14M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][13]]},
            prefix + '16M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][14]]},
            prefix + '16M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][15]]},
            prefix + '18M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][16]]},
            prefix + '18M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][17]]},
            prefix + '20M1' + suffix : { 'qdb1' : [family_data['qdb1']['index'][18]]},
            prefix + '20M2' + suffix : { 'qdb1' : [family_data['qdb1']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qdp2':
        prefix = prefix + 'QDP2-'
        _dict = {
            prefix + '03M1' + suffix : { 'qdp2' : [family_data['qdp2']['index'][0]]},
            prefix + '03M2' + suffix : { 'qdp2' : [family_data['qdp2']['index'][1]]},
            prefix + '07M1' + suffix : { 'qdp2' : [family_data['qdp2']['index'][2]]},
            prefix + '07M2' + suffix : { 'qdp2' : [family_data['qdp2']['index'][3]]},
            prefix + '11M1' + suffix : { 'qdp2' : [family_data['qdp2']['index'][4]]},
            prefix + '11M2' + suffix : { 'qdp2' : [family_data['qdp2']['index'][5]]},
            prefix + '15M1' + suffix : { 'qdp2' : [family_data['qdp2']['index'][6]]},
            prefix + '15M2' + suffix : { 'qdp2' : [family_data['qdp2']['index'][7]]},
            prefix + '19M1' + suffix : { 'qdp2' : [family_data['qdp2']['index'][8]]},
            prefix + '19M2' + suffix : { 'qdp2' : [family_data['qdp2']['index'][9]]},
        }
        return _dict

    if element.lower() == 'qfp':
        prefix = prefix + 'QFP-'
        _dict = {
            prefix + '03M1' + suffix : { 'qfp' : [family_data['qfp']['index'][0]]},
            prefix + '03M2' + suffix : { 'qfp' : [family_data['qfp']['index'][1]]},
            prefix + '07M1' + suffix : { 'qfp' : [family_data['qfp']['index'][2]]},
            prefix + '07M2' + suffix : { 'qfp' : [family_data['qfp']['index'][3]]},
            prefix + '11M1' + suffix : { 'qfp' : [family_data['qfp']['index'][4]]},
            prefix + '11M2' + suffix : { 'qfp' : [family_data['qfp']['index'][5]]},
            prefix + '15M1' + suffix : { 'qfp' : [family_data['qfp']['index'][6]]},
            prefix + '15M2' + suffix : { 'qfp' : [family_data['qfp']['index'][7]]},
            prefix + '19M1' + suffix : { 'qfp' : [family_data['qfp']['index'][8]]},
            prefix + '19M2' + suffix : { 'qfp' : [family_data['qfp']['index'][9]]},
        }
        return _dict

    if element.lower() == 'qdp1':
        prefix = prefix + 'QDP1-'
        _dict = {
            prefix + '03M1' + suffix : { 'qdp1' : [family_data['qdp1']['index'][0]]},
            prefix + '03M2' + suffix : { 'qdp1' : [family_data['qdp1']['index'][1]]},
            prefix + '07M1' + suffix : { 'qdp1' : [family_data['qdp1']['index'][2]]},
            prefix + '07M2' + suffix : { 'qdp1' : [family_data['qdp1']['index'][3]]},
            prefix + '11M1' + suffix : { 'qdp1' : [family_data['qdp1']['index'][4]]},
            prefix + '11M2' + suffix : { 'qdp1' : [family_data['qdp1']['index'][5]]},
            prefix + '15M1' + suffix : { 'qdp1' : [family_data['qdp1']['index'][6]]},
            prefix + '15M2' + suffix : { 'qdp1' : [family_data['qdp1']['index'][7]]},
            prefix + '19M1' + suffix : { 'qdp1' : [family_data['qdp1']['index'][8]]},
            prefix + '19M2' + suffix : { 'qdp1' : [family_data['qdp1']['index'][9]]},
        }
        return _dict

    if element.lower() == 'q1':
        prefix = prefix + 'Q1-'
        _dict = {
            prefix + '01C1' + suffix : { 'q1' : [family_data['q1']['index'][0]]},
            prefix + '01C4' + suffix : { 'q1' : [family_data['q1']['index'][1]]},
            prefix + '02C1' + suffix : { 'q1' : [family_data['q1']['index'][2]]},
            prefix + '02C4' + suffix : { 'q1' : [family_data['q1']['index'][3]]},
            prefix + '03C1' + suffix : { 'q1' : [family_data['q1']['index'][4]]},
            prefix + '03C4' + suffix : { 'q1' : [family_data['q1']['index'][5]]},
            prefix + '04C1' + suffix : { 'q1' : [family_data['q1']['index'][6]]},
            prefix + '04C4' + suffix : { 'q1' : [family_data['q1']['index'][7]]},
            prefix + '05C1' + suffix : { 'q1' : [family_data['q1']['index'][8]]},
            prefix + '05C4' + suffix : { 'q1' : [family_data['q1']['index'][9]]},
            prefix + '06C1' + suffix : { 'q1' : [family_data['q1']['index'][10]]},
            prefix + '06C4' + suffix : { 'q1' : [family_data['q1']['index'][11]]},
            prefix + '07C1' + suffix : { 'q1' : [family_data['q1']['index'][12]]},
            prefix + '07C4' + suffix : { 'q1' : [family_data['q1']['index'][13]]},
            prefix + '08C1' + suffix : { 'q1' : [family_data['q1']['index'][14]]},
            prefix + '08C4' + suffix : { 'q1' : [family_data['q1']['index'][15]]},
            prefix + '09C1' + suffix : { 'q1' : [family_data['q1']['index'][16]]},
            prefix + '09C4' + suffix : { 'q1' : [family_data['q1']['index'][17]]},
            prefix + '10C1' + suffix : { 'q1' : [family_data['q1']['index'][18]]},
            prefix + '10C4' + suffix : { 'q1' : [family_data['q1']['index'][19]]},
            prefix + '11C1' + suffix : { 'q1' : [family_data['q1']['index'][20]]},
            prefix + '11C4' + suffix : { 'q1' : [family_data['q1']['index'][21]]},
            prefix + '12C1' + suffix : { 'q1' : [family_data['q1']['index'][22]]},
            prefix + '12C4' + suffix : { 'q1' : [family_data['q1']['index'][23]]},
            prefix + '13C1' + suffix : { 'q1' : [family_data['q1']['index'][24]]},
            prefix + '13C4' + suffix : { 'q1' : [family_data['q1']['index'][25]]},
            prefix + '14C1' + suffix : { 'q1' : [family_data['q1']['index'][26]]},
            prefix + '14C4' + suffix : { 'q1' : [family_data['q1']['index'][27]]},
            prefix + '15C1' + suffix : { 'q1' : [family_data['q1']['index'][28]]},
            prefix + '15C4' + suffix : { 'q1' : [family_data['q1']['index'][29]]},
            prefix + '16C1' + suffix : { 'q1' : [family_data['q1']['index'][30]]},
            prefix + '16C4' + suffix : { 'q1' : [family_data['q1']['index'][31]]},
            prefix + '17C1' + suffix : { 'q1' : [family_data['q1']['index'][32]]},
            prefix + '17C4' + suffix : { 'q1' : [family_data['q1']['index'][33]]},
            prefix + '18C1' + suffix : { 'q1' : [family_data['q1']['index'][34]]},
            prefix + '18C4' + suffix : { 'q1' : [family_data['q1']['index'][35]]},
            prefix + '19C1' + suffix : { 'q1' : [family_data['q1']['index'][36]]},
            prefix + '19C4' + suffix : { 'q1' : [family_data['q1']['index'][37]]},
            prefix + '20C1' + suffix : { 'q1' : [family_data['q1']['index'][38]]},
            prefix + '20C4' + suffix : { 'q1' : [family_data['q1']['index'][39]]},
        }
        return _dict

    if element.lower() == 'q2':
        prefix = prefix + 'Q2-'
        _dict = {
            prefix + '01C1' + suffix : { 'q2' : [family_data['q2']['index'][0]]},
            prefix + '01C4' + suffix : { 'q2' : [family_data['q2']['index'][1]]},
            prefix + '02C1' + suffix : { 'q2' : [family_data['q2']['index'][2]]},
            prefix + '02C4' + suffix : { 'q2' : [family_data['q2']['index'][3]]},
            prefix + '03C1' + suffix : { 'q2' : [family_data['q2']['index'][4]]},
            prefix + '03C4' + suffix : { 'q2' : [family_data['q2']['index'][5]]},
            prefix + '04C1' + suffix : { 'q2' : [family_data['q2']['index'][6]]},
            prefix + '04C4' + suffix : { 'q2' : [family_data['q2']['index'][7]]},
            prefix + '05C1' + suffix : { 'q2' : [family_data['q2']['index'][8]]},
            prefix + '05C4' + suffix : { 'q2' : [family_data['q2']['index'][9]]},
            prefix + '06C1' + suffix : { 'q2' : [family_data['q2']['index'][10]]},
            prefix + '06C4' + suffix : { 'q2' : [family_data['q2']['index'][11]]},
            prefix + '07C1' + suffix : { 'q2' : [family_data['q2']['index'][12]]},
            prefix + '07C4' + suffix : { 'q2' : [family_data['q2']['index'][13]]},
            prefix + '08C1' + suffix : { 'q2' : [family_data['q2']['index'][14]]},
            prefix + '08C4' + suffix : { 'q2' : [family_data['q2']['index'][15]]},
            prefix + '09C1' + suffix : { 'q2' : [family_data['q2']['index'][16]]},
            prefix + '09C4' + suffix : { 'q2' : [family_data['q2']['index'][17]]},
            prefix + '10C1' + suffix : { 'q2' : [family_data['q2']['index'][18]]},
            prefix + '10C4' + suffix : { 'q2' : [family_data['q2']['index'][19]]},
            prefix + '11C1' + suffix : { 'q2' : [family_data['q2']['index'][20]]},
            prefix + '11C4' + suffix : { 'q2' : [family_data['q2']['index'][21]]},
            prefix + '12C1' + suffix : { 'q2' : [family_data['q2']['index'][22]]},
            prefix + '12C4' + suffix : { 'q2' : [family_data['q2']['index'][23]]},
            prefix + '13C1' + suffix : { 'q2' : [family_data['q2']['index'][24]]},
            prefix + '13C4' + suffix : { 'q2' : [family_data['q2']['index'][25]]},
            prefix + '14C1' + suffix : { 'q2' : [family_data['q2']['index'][26]]},
            prefix + '14C4' + suffix : { 'q2' : [family_data['q2']['index'][27]]},
            prefix + '15C1' + suffix : { 'q2' : [family_data['q2']['index'][28]]},
            prefix + '15C4' + suffix : { 'q2' : [family_data['q2']['index'][29]]},
            prefix + '16C1' + suffix : { 'q2' : [family_data['q2']['index'][30]]},
            prefix + '16C4' + suffix : { 'q2' : [family_data['q2']['index'][31]]},
            prefix + '17C1' + suffix : { 'q2' : [family_data['q2']['index'][32]]},
            prefix + '17C4' + suffix : { 'q2' : [family_data['q2']['index'][33]]},
            prefix + '18C1' + suffix : { 'q2' : [family_data['q2']['index'][34]]},
            prefix + '18C4' + suffix : { 'q2' : [family_data['q2']['index'][35]]},
            prefix + '19C1' + suffix : { 'q2' : [family_data['q2']['index'][36]]},
            prefix + '19C4' + suffix : { 'q2' : [family_data['q2']['index'][37]]},
            prefix + '20C1' + suffix : { 'q2' : [family_data['q2']['index'][38]]},
            prefix + '20C4' + suffix : { 'q2' : [family_data['q2']['index'][39]]},
        }
        return _dict

    if element.lower() == 'q3':
        prefix = prefix + 'Q3-'
        _dict = {
            prefix + '01C2' + suffix : { 'q3' : [family_data['q3']['index'][0]]},
            prefix + '01C3' + suffix : { 'q3' : [family_data['q3']['index'][1]]},
            prefix + '02C2' + suffix : { 'q3' : [family_data['q3']['index'][2]]},
            prefix + '02C3' + suffix : { 'q3' : [family_data['q3']['index'][3]]},
            prefix + '03C2' + suffix : { 'q3' : [family_data['q3']['index'][4]]},
            prefix + '03C3' + suffix : { 'q3' : [family_data['q3']['index'][5]]},
            prefix + '04C2' + suffix : { 'q3' : [family_data['q3']['index'][6]]},
            prefix + '04C3' + suffix : { 'q3' : [family_data['q3']['index'][7]]},
            prefix + '05C2' + suffix : { 'q3' : [family_data['q3']['index'][8]]},
            prefix + '05C3' + suffix : { 'q3' : [family_data['q3']['index'][9]]},
            prefix + '06C2' + suffix : { 'q3' : [family_data['q3']['index'][10]]},
            prefix + '06C3' + suffix : { 'q3' : [family_data['q3']['index'][11]]},
            prefix + '07C2' + suffix : { 'q3' : [family_data['q3']['index'][12]]},
            prefix + '07C3' + suffix : { 'q3' : [family_data['q3']['index'][13]]},
            prefix + '08C2' + suffix : { 'q3' : [family_data['q3']['index'][14]]},
            prefix + '08C3' + suffix : { 'q3' : [family_data['q3']['index'][15]]},
            prefix + '09C2' + suffix : { 'q3' : [family_data['q3']['index'][16]]},
            prefix + '09C3' + suffix : { 'q3' : [family_data['q3']['index'][17]]},
            prefix + '10C2' + suffix : { 'q3' : [family_data['q3']['index'][18]]},
            prefix + '10C3' + suffix : { 'q3' : [family_data['q3']['index'][19]]},
            prefix + '11C2' + suffix : { 'q3' : [family_data['q3']['index'][20]]},
            prefix + '11C3' + suffix : { 'q3' : [family_data['q3']['index'][21]]},
            prefix + '12C2' + suffix : { 'q3' : [family_data['q3']['index'][22]]},
            prefix + '12C3' + suffix : { 'q3' : [family_data['q3']['index'][23]]},
            prefix + '13C2' + suffix : { 'q3' : [family_data['q3']['index'][24]]},
            prefix + '13C3' + suffix : { 'q3' : [family_data['q3']['index'][25]]},
            prefix + '14C2' + suffix : { 'q3' : [family_data['q3']['index'][26]]},
            prefix + '14C3' + suffix : { 'q3' : [family_data['q3']['index'][27]]},
            prefix + '15C2' + suffix : { 'q3' : [family_data['q3']['index'][28]]},
            prefix + '15C3' + suffix : { 'q3' : [family_data['q3']['index'][29]]},
            prefix + '16C2' + suffix : { 'q3' : [family_data['q3']['index'][30]]},
            prefix + '16C3' + suffix : { 'q3' : [family_data['q3']['index'][31]]},
            prefix + '17C2' + suffix : { 'q3' : [family_data['q3']['index'][32]]},
            prefix + '17C3' + suffix : { 'q3' : [family_data['q3']['index'][33]]},
            prefix + '18C2' + suffix : { 'q3' : [family_data['q3']['index'][34]]},
            prefix + '18C3' + suffix : { 'q3' : [family_data['q3']['index'][35]]},
            prefix + '19C2' + suffix : { 'q3' : [family_data['q3']['index'][36]]},
            prefix + '19C3' + suffix : { 'q3' : [family_data['q3']['index'][37]]},
            prefix + '20C2' + suffix : { 'q3' : [family_data['q3']['index'][38]]},
            prefix + '20C3' + suffix : { 'q3' : [family_data['q3']['index'][39]]},
        }
        return _dict

    if element.lower() == 'q4':
        prefix = prefix + 'Q4-'
        _dict = {
            prefix + '01C2' + suffix : { 'q4' : [family_data['q4']['index'][0]]},
            prefix + '01C3' + suffix : { 'q4' : [family_data['q4']['index'][1]]},
            prefix + '02C2' + suffix : { 'q4' : [family_data['q4']['index'][2]]},
            prefix + '02C3' + suffix : { 'q4' : [family_data['q4']['index'][3]]},
            prefix + '03C2' + suffix : { 'q4' : [family_data['q4']['index'][4]]},
            prefix + '03C3' + suffix : { 'q4' : [family_data['q4']['index'][5]]},
            prefix + '04C2' + suffix : { 'q4' : [family_data['q4']['index'][6]]},
            prefix + '04C3' + suffix : { 'q4' : [family_data['q4']['index'][7]]},
            prefix + '05C2' + suffix : { 'q4' : [family_data['q4']['index'][8]]},
            prefix + '05C3' + suffix : { 'q4' : [family_data['q4']['index'][9]]},
            prefix + '06C2' + suffix : { 'q4' : [family_data['q4']['index'][10]]},
            prefix + '06C3' + suffix : { 'q4' : [family_data['q4']['index'][11]]},
            prefix + '07C2' + suffix : { 'q4' : [family_data['q4']['index'][12]]},
            prefix + '07C3' + suffix : { 'q4' : [family_data['q4']['index'][13]]},
            prefix + '08C2' + suffix : { 'q4' : [family_data['q4']['index'][14]]},
            prefix + '08C3' + suffix : { 'q4' : [family_data['q4']['index'][15]]},
            prefix + '09C2' + suffix : { 'q4' : [family_data['q4']['index'][16]]},
            prefix + '09C3' + suffix : { 'q4' : [family_data['q4']['index'][17]]},
            prefix + '10C2' + suffix : { 'q4' : [family_data['q4']['index'][18]]},
            prefix + '10C3' + suffix : { 'q4' : [family_data['q4']['index'][19]]},
            prefix + '11C2' + suffix : { 'q4' : [family_data['q4']['index'][20]]},
            prefix + '11C3' + suffix : { 'q4' : [family_data['q4']['index'][21]]},
            prefix + '12C2' + suffix : { 'q4' : [family_data['q4']['index'][22]]},
            prefix + '12C3' + suffix : { 'q4' : [family_data['q4']['index'][23]]},
            prefix + '13C2' + suffix : { 'q4' : [family_data['q4']['index'][24]]},
            prefix + '13C3' + suffix : { 'q4' : [family_data['q4']['index'][25]]},
            prefix + '14C2' + suffix : { 'q4' : [family_data['q4']['index'][26]]},
            prefix + '14C3' + suffix : { 'q4' : [family_data['q4']['index'][27]]},
            prefix + '15C2' + suffix : { 'q4' : [family_data['q4']['index'][28]]},
            prefix + '15C3' + suffix : { 'q4' : [family_data['q4']['index'][29]]},
            prefix + '16C2' + suffix : { 'q4' : [family_data['q4']['index'][30]]},
            prefix + '16C3' + suffix : { 'q4' : [family_data['q4']['index'][31]]},
            prefix + '17C2' + suffix : { 'q4' : [family_data['q4']['index'][32]]},
            prefix + '17C3' + suffix : { 'q4' : [family_data['q4']['index'][33]]},
            prefix + '18C2' + suffix : { 'q4' : [family_data['q4']['index'][34]]},
            prefix + '18C3' + suffix : { 'q4' : [family_data['q4']['index'][35]]},
            prefix + '19C2' + suffix : { 'q4' : [family_data['q4']['index'][36]]},
            prefix + '19C3' + suffix : { 'q4' : [family_data['q4']['index'][37]]},
            prefix + '20C2' + suffix : { 'q4' : [family_data['q4']['index'][38]]},
            prefix + '20C3' + suffix : { 'q4' : [family_data['q4']['index'][39]]},
        }
        return _dict

    if element.lower() == 'sda0':
        prefix = prefix + 'SDA0-'
        _dict = {
            prefix + '01M1' + suffix : { 'sda0' : [family_data['sda0']['index'][0]]},
            prefix + '01M2' + suffix : { 'sda0' : [family_data['sda0']['index'][1]]},
            prefix + '05M1' + suffix : { 'sda0' : [family_data['sda0']['index'][2]]},
            prefix + '05M2' + suffix : { 'sda0' : [family_data['sda0']['index'][3]]},
            prefix + '09M1' + suffix : { 'sda0' : [family_data['sda0']['index'][4]]},
            prefix + '09M2' + suffix : { 'sda0' : [family_data['sda0']['index'][5]]},
            prefix + '13M1' + suffix : { 'sda0' : [family_data['sda0']['index'][6]]},
            prefix + '13M2' + suffix : { 'sda0' : [family_data['sda0']['index'][7]]},
            prefix + '17M1' + suffix : { 'sda0' : [family_data['sda0']['index'][8]]},
            prefix + '17M2' + suffix : { 'sda0' : [family_data['sda0']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sdb0':
        prefix = prefix + 'SDB0-'
        _dict = {
            prefix + '02M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][0]]},
            prefix + '02M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][1]]},
            prefix + '04M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][2]]},
            prefix + '04M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][3]]},
            prefix + '06M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][4]]},
            prefix + '06M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][5]]},
            prefix + '08M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][6]]},
            prefix + '08M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][7]]},
            prefix + '10M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][8]]},
            prefix + '10M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][9]]},
            prefix + '12M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][10]]},
            prefix + '12M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][11]]},
            prefix + '14M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][12]]},
            prefix + '14M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][13]]},
            prefix + '16M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][14]]},
            prefix + '16M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][15]]},
            prefix + '18M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][16]]},
            prefix + '18M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][17]]},
            prefix + '20M1' + suffix : { 'sdb0' : [family_data['sdb0']['index'][18]]},
            prefix + '20M2' + suffix : { 'sdb0' : [family_data['sdb0']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sdp0':
        prefix = prefix + 'SDP0-'
        _dict = {
            prefix + '03M1' + suffix : { 'sdp0' : [family_data['sdp0']['index'][0]]},
            prefix + '03M2' + suffix : { 'sdp0' : [family_data['sdp0']['index'][1]]},
            prefix + '07M1' + suffix : { 'sdp0' : [family_data['sdp0']['index'][2]]},
            prefix + '07M2' + suffix : { 'sdp0' : [family_data['sdp0']['index'][3]]},
            prefix + '11M1' + suffix : { 'sdp0' : [family_data['sdp0']['index'][4]]},
            prefix + '11M2' + suffix : { 'sdp0' : [family_data['sdp0']['index'][5]]},
            prefix + '15M1' + suffix : { 'sdp0' : [family_data['sdp0']['index'][6]]},
            prefix + '15M2' + suffix : { 'sdp0' : [family_data['sdp0']['index'][7]]},
            prefix + '19M1' + suffix : { 'sdp0' : [family_data['sdp0']['index'][8]]},
            prefix + '19M2' + suffix : { 'sdp0' : [family_data['sdp0']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sda1':
        prefix = prefix + 'SDA1-'
        _dict = {
            prefix + '01C1' + suffix : { 'sda1' : [family_data['sda1']['index'][0]]},
            prefix + '04C4' + suffix : { 'sda1' : [family_data['sda1']['index'][1]]},
            prefix + '05C1' + suffix : { 'sda1' : [family_data['sda1']['index'][2]]},
            prefix + '08C4' + suffix : { 'sda1' : [family_data['sda1']['index'][3]]},
            prefix + '09C1' + suffix : { 'sda1' : [family_data['sda1']['index'][4]]},
            prefix + '12C4' + suffix : { 'sda1' : [family_data['sda1']['index'][5]]},
            prefix + '13C1' + suffix : { 'sda1' : [family_data['sda1']['index'][6]]},
            prefix + '16C4' + suffix : { 'sda1' : [family_data['sda1']['index'][7]]},
            prefix + '17C1' + suffix : { 'sda1' : [family_data['sda1']['index'][8]]},
            prefix + '20C4' + suffix : { 'sda1' : [family_data['sda1']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sdb1':
        prefix = prefix + 'SDB1-'
        _dict = {
            prefix + '01C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][0]]},
            prefix + '02C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][1]]},
            prefix + '03C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][2]]},
            prefix + '04C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][3]]},
            prefix + '05C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][4]]},
            prefix + '06C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][5]]},
            prefix + '07C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][6]]},
            prefix + '08C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][7]]},
            prefix + '09C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][8]]},
            prefix + '10C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][9]]},
            prefix + '11C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][10]]},
            prefix + '12C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][11]]},
            prefix + '13C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][12]]},
            prefix + '14C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][13]]},
            prefix + '15C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][14]]},
            prefix + '16C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][15]]},
            prefix + '17C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][16]]},
            prefix + '18C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][17]]},
            prefix + '19C4' + suffix : { 'sdb1' : [family_data['sdb1']['index'][18]]},
            prefix + '20C1' + suffix : { 'sdb1' : [family_data['sdb1']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sdp1':
        prefix = prefix + 'SDP1-'
        _dict = {
            prefix + '02C4' + suffix : { 'sdp1' : [family_data['sdp1']['index'][0]]},
            prefix + '03C1' + suffix : { 'sdp1' : [family_data['sdp1']['index'][1]]},
            prefix + '06C4' + suffix : { 'sdp1' : [family_data['sdp1']['index'][2]]},
            prefix + '07C1' + suffix : { 'sdp1' : [family_data['sdp1']['index'][3]]},
            prefix + '10C4' + suffix : { 'sdp1' : [family_data['sdp1']['index'][4]]},
            prefix + '11C1' + suffix : { 'sdp1' : [family_data['sdp1']['index'][5]]},
            prefix + '14C4' + suffix : { 'sdp1' : [family_data['sdp1']['index'][6]]},
            prefix + '15C1' + suffix : { 'sdp1' : [family_data['sdp1']['index'][7]]},
            prefix + '18C4' + suffix : { 'sdp1' : [family_data['sdp1']['index'][8]]},
            prefix + '19C1' + suffix : { 'sdp1' : [family_data['sdp1']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sda2':
        prefix = prefix + 'SDA2-'
        _dict = {
            prefix + '01C1' + suffix : { 'sda2' : [family_data['sda2']['index'][0]]},
            prefix + '04C4' + suffix : { 'sda2' : [family_data['sda2']['index'][1]]},
            prefix + '05C1' + suffix : { 'sda2' : [family_data['sda2']['index'][2]]},
            prefix + '08C4' + suffix : { 'sda2' : [family_data['sda2']['index'][3]]},
            prefix + '09C1' + suffix : { 'sda2' : [family_data['sda2']['index'][4]]},
            prefix + '12C4' + suffix : { 'sda2' : [family_data['sda2']['index'][5]]},
            prefix + '13C1' + suffix : { 'sda2' : [family_data['sda2']['index'][6]]},
            prefix + '16C4' + suffix : { 'sda2' : [family_data['sda2']['index'][7]]},
            prefix + '17C1' + suffix : { 'sda2' : [family_data['sda2']['index'][8]]},
            prefix + '20C4' + suffix : { 'sda2' : [family_data['sda2']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sdb2':
        prefix = prefix + 'SDB2-'
        _dict = {
            prefix + '01C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][0]]},
            prefix + '02C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][10]]},
            prefix + '03C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][11]]},
            prefix + '04C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][1]]},
            prefix + '05C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][2]]},
            prefix + '06C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][12]]},
            prefix + '07C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][13]]},
            prefix + '08C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][3]]},
            prefix + '09C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][4]]},
            prefix + '10C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][14]]},
            prefix + '11C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][15]]},
            prefix + '12C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][5]]},
            prefix + '13C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][6]]},
            prefix + '14C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][16]]},
            prefix + '15C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][17]]},
            prefix + '16C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][7]]},
            prefix + '17C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][8]]},
            prefix + '18C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][18]]},
            prefix + '19C4' + suffix : { 'sdb2' : [family_data['sdb2']['index'][19]]},
            prefix + '20C1' + suffix : { 'sdb2' : [family_data['sdb2']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sdp2':
        prefix = prefix + 'SDP2-'
        _dict = {
            prefix + '02C4' + suffix : { 'sdp2' : [family_data['sdp2']['index'][0]]},
            prefix + '03C1' + suffix : { 'sdp2' : [family_data['sdp2']['index'][1]]},
            prefix + '06C4' + suffix : { 'sdp2' : [family_data['sdp2']['index'][2]]},
            prefix + '07C1' + suffix : { 'sdp2' : [family_data['sdp2']['index'][3]]},
            prefix + '10C4' + suffix : { 'sdp2' : [family_data['sdp2']['index'][4]]},
            prefix + '11C1' + suffix : { 'sdp2' : [family_data['sdp2']['index'][5]]},
            prefix + '14C4' + suffix : { 'sdp2' : [family_data['sdp2']['index'][6]]},
            prefix + '15C1' + suffix : { 'sdp2' : [family_data['sdp2']['index'][7]]},
            prefix + '18C4' + suffix : { 'sdp2' : [family_data['sdp2']['index'][8]]},
            prefix + '19C1' + suffix : { 'sdp2' : [family_data['sdp2']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sda3':
        prefix = prefix + 'SDA3-'
        _dict = {
            prefix + '01C2' + suffix : { 'sda3' : [family_data['sda3']['index'][0]]},
            prefix + '04C3' + suffix : { 'sda3' : [family_data['sda3']['index'][1]]},
            prefix + '05C2' + suffix : { 'sda3' : [family_data['sda3']['index'][2]]},
            prefix + '08C3' + suffix : { 'sda3' : [family_data['sda3']['index'][3]]},
            prefix + '09C2' + suffix : { 'sda3' : [family_data['sda3']['index'][4]]},
            prefix + '12C3' + suffix : { 'sda3' : [family_data['sda3']['index'][5]]},
            prefix + '13C2' + suffix : { 'sda3' : [family_data['sda3']['index'][6]]},
            prefix + '16C3' + suffix : { 'sda3' : [family_data['sda3']['index'][7]]},
            prefix + '17C2' + suffix : { 'sda3' : [family_data['sda3']['index'][8]]},
            prefix + '20C3' + suffix : { 'sda3' : [family_data['sda3']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sdb3':
        prefix = prefix + 'SDB3-'
        _dict = {
            prefix + '01C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][0]]},
            prefix + '02C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][1]]},
            prefix + '03C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][2]]},
            prefix + '04C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][3]]},
            prefix + '05C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][4]]},
            prefix + '06C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][5]]},
            prefix + '07C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][6]]},
            prefix + '08C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][7]]},
            prefix + '09C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][8]]},
            prefix + '10C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][9]]},
            prefix + '11C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][10]]},
            prefix + '12C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][11]]},
            prefix + '13C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][12]]},
            prefix + '14C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][13]]},
            prefix + '15C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][14]]},
            prefix + '16C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][15]]},
            prefix + '17C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][16]]},
            prefix + '18C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][17]]},
            prefix + '19C3' + suffix : { 'sdb3' : [family_data['sdb3']['index'][18]]},
            prefix + '20C2' + suffix : { 'sdb3' : [family_data['sdb3']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sdp3':
        prefix = prefix + 'SDP3-'
        _dict = {
            prefix + '02C3' + suffix : { 'sdp3' : [family_data['sdp3']['index'][0]]},
            prefix + '03C2' + suffix : { 'sdp3' : [family_data['sdp3']['index'][1]]},
            prefix + '06C3' + suffix : { 'sdp3' : [family_data['sdp3']['index'][2]]},
            prefix + '07C2' + suffix : { 'sdp3' : [family_data['sdp3']['index'][3]]},
            prefix + '10C3' + suffix : { 'sdp3' : [family_data['sdp3']['index'][4]]},
            prefix + '11C2' + suffix : { 'sdp3' : [family_data['sdp3']['index'][5]]},
            prefix + '14C3' + suffix : { 'sdp3' : [family_data['sdp3']['index'][6]]},
            prefix + '15C2' + suffix : { 'sdp3' : [family_data['sdp3']['index'][7]]},
            prefix + '18C3' + suffix : { 'sdp3' : [family_data['sdp3']['index'][8]]},
            prefix + '19C2' + suffix : { 'sdp3' : [family_data['sdp3']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sfa0':
        prefix = prefix + 'SFA0-'
        _dict = {
            prefix + '01M1' + suffix : { 'sfa0' : [family_data['sfa0']['index'][0]]},
            prefix + '01M2' + suffix : { 'sfa0' : [family_data['sfa0']['index'][1]]},
            prefix + '05M1' + suffix : { 'sfa0' : [family_data['sfa0']['index'][2]]},
            prefix + '05M2' + suffix : { 'sfa0' : [family_data['sfa0']['index'][3]]},
            prefix + '09M1' + suffix : { 'sfa0' : [family_data['sfa0']['index'][4]]},
            prefix + '09M2' + suffix : { 'sfa0' : [family_data['sfa0']['index'][5]]},
            prefix + '13M1' + suffix : { 'sfa0' : [family_data['sfa0']['index'][6]]},
            prefix + '13M2' + suffix : { 'sfa0' : [family_data['sfa0']['index'][7]]},
            prefix + '17M1' + suffix : { 'sfa0' : [family_data['sfa0']['index'][8]]},
            prefix + '17M2' + suffix : { 'sfa0' : [family_data['sfa0']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sfb0':
        prefix = prefix + 'SFB0-'
        _dict = {
            prefix + '02M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][0]]},
            prefix + '02M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][1]]},
            prefix + '04M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][2]]},
            prefix + '04M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][3]]},
            prefix + '06M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][4]]},
            prefix + '06M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][5]]},
            prefix + '08M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][6]]},
            prefix + '08M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][7]]},
            prefix + '10M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][8]]},
            prefix + '10M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][9]]},
            prefix + '12M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][10]]},
            prefix + '12M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][11]]},
            prefix + '14M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][12]]},
            prefix + '14M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][13]]},
            prefix + '16M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][14]]},
            prefix + '16M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][15]]},
            prefix + '18M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][16]]},
            prefix + '18M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][17]]},
            prefix + '20M1' + suffix : { 'sfb0' : [family_data['sfb0']['index'][18]]},
            prefix + '20M2' + suffix : { 'sfb0' : [family_data['sfb0']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sfp0':
        prefix = prefix + 'SFP0-'
        _dict = {
            prefix + '03M1' + suffix : { 'sfp0' : [family_data['sfp0']['index'][0]]},
            prefix + '03M2' + suffix : { 'sfp0' : [family_data['sfp0']['index'][1]]},
            prefix + '07M1' + suffix : { 'sfp0' : [family_data['sfp0']['index'][2]]},
            prefix + '07M2' + suffix : { 'sfp0' : [family_data['sfp0']['index'][3]]},
            prefix + '11M1' + suffix : { 'sfp0' : [family_data['sfp0']['index'][4]]},
            prefix + '11M2' + suffix : { 'sfp0' : [family_data['sfp0']['index'][5]]},
            prefix + '15M1' + suffix : { 'sfp0' : [family_data['sfp0']['index'][6]]},
            prefix + '15M2' + suffix : { 'sfp0' : [family_data['sfp0']['index'][7]]},
            prefix + '19M1' + suffix : { 'sfp0' : [family_data['sfp0']['index'][8]]},
            prefix + '19M2' + suffix : { 'sfp0' : [family_data['sfp0']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sfa1':
        prefix = prefix + 'SFA1-'
        _dict = {
            prefix + '01C1' + suffix : { 'sfa1' : [family_data['sfa1']['index'][0]]},
            prefix + '04C4' + suffix : { 'sfa1' : [family_data['sfa1']['index'][1]]},
            prefix + '05C1' + suffix : { 'sfa1' : [family_data['sfa1']['index'][2]]},
            prefix + '08C4' + suffix : { 'sfa1' : [family_data['sfa1']['index'][3]]},
            prefix + '09C1' + suffix : { 'sfa1' : [family_data['sfa1']['index'][4]]},
            prefix + '12C4' + suffix : { 'sfa1' : [family_data['sfa1']['index'][5]]},
            prefix + '13C1' + suffix : { 'sfa1' : [family_data['sfa1']['index'][6]]},
            prefix + '16C4' + suffix : { 'sfa1' : [family_data['sfa1']['index'][7]]},
            prefix + '17C1' + suffix : { 'sfa1' : [family_data['sfa1']['index'][8]]},
            prefix + '20C4' + suffix : { 'sfa1' : [family_data['sfa1']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sfb1':
        prefix = prefix + 'SFB1-'
        _dict = {
            prefix + '01C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][0]]},
            prefix + '02C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][1]]},
            prefix + '03C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][2]]},
            prefix + '04C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][3]]},
            prefix + '05C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][4]]},
            prefix + '06C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][5]]},
            prefix + '07C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][6]]},
            prefix + '08C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][7]]},
            prefix + '09C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][8]]},
            prefix + '10C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][9]]},
            prefix + '11C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][10]]},
            prefix + '12C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][11]]},
            prefix + '13C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][12]]},
            prefix + '14C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][13]]},
            prefix + '15C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][14]]},
            prefix + '16C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][15]]},
            prefix + '17C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][16]]},
            prefix + '18C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][17]]},
            prefix + '19C4' + suffix : { 'sfb1' : [family_data['sfb1']['index'][18]]},
            prefix + '20C1' + suffix : { 'sfb1' : [family_data['sfb1']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sfp1':
        prefix = prefix + 'SFP1-'
        _dict = {
            prefix + '02C4' + suffix : { 'sfp1' : [family_data['sfp1']['index'][0]]},
            prefix + '03C1' + suffix : { 'sfp1' : [family_data['sfp1']['index'][1]]},
            prefix + '06C4' + suffix : { 'sfp1' : [family_data['sfp1']['index'][2]]},
            prefix + '07C1' + suffix : { 'sfp1' : [family_data['sfp1']['index'][3]]},
            prefix + '10C4' + suffix : { 'sfp1' : [family_data['sfp1']['index'][4]]},
            prefix + '11C1' + suffix : { 'sfp1' : [family_data['sfp1']['index'][5]]},
            prefix + '14C4' + suffix : { 'sfp1' : [family_data['sfp1']['index'][6]]},
            prefix + '15C1' + suffix : { 'sfp1' : [family_data['sfp1']['index'][7]]},
            prefix + '18C4' + suffix : { 'sfp1' : [family_data['sfp1']['index'][8]]},
            prefix + '19C1' + suffix : { 'sfp1' : [family_data['sfp1']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sfa2':
        prefix = prefix + 'SFA2-'
        _dict = {
            prefix + '01C2' + suffix : { 'sfa2' : [family_data['sfa2']['index'][0]]},
            prefix + '04C3' + suffix : { 'sfa2' : [family_data['sfa2']['index'][1]]},
            prefix + '05C2' + suffix : { 'sfa2' : [family_data['sfa2']['index'][2]]},
            prefix + '08C3' + suffix : { 'sfa2' : [family_data['sfa2']['index'][3]]},
            prefix + '09C2' + suffix : { 'sfa2' : [family_data['sfa2']['index'][4]]},
            prefix + '12C3' + suffix : { 'sfa2' : [family_data['sfa2']['index'][5]]},
            prefix + '13C2' + suffix : { 'sfa2' : [family_data['sfa2']['index'][6]]},
            prefix + '16C3' + suffix : { 'sfa2' : [family_data['sfa2']['index'][7]]},
            prefix + '17C2' + suffix : { 'sfa2' : [family_data['sfa2']['index'][8]]},
            prefix + '20C3' + suffix : { 'sfa2' : [family_data['sfa2']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sfb2':
        prefix = prefix + 'SFB2-'
        _dict = {
            prefix + '01C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][0]]},
            prefix + '02C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][1]]},
            prefix + '03C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][2]]},
            prefix + '04C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][3]]},
            prefix + '05C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][4]]},
            prefix + '06C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][5]]},
            prefix + '07C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][6]]},
            prefix + '08C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][7]]},
            prefix + '09C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][8]]},
            prefix + '10C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][9]]},
            prefix + '11C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][10]]},
            prefix + '12C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][11]]},
            prefix + '13C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][12]]},
            prefix + '14C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][13]]},
            prefix + '15C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][14]]},
            prefix + '16C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][15]]},
            prefix + '17C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][16]]},
            prefix + '18C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][17]]},
            prefix + '19C3' + suffix : { 'sfb2' : [family_data['sfb2']['index'][18]]},
            prefix + '20C2' + suffix : { 'sfb2' : [family_data['sfb2']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sfp2':
        prefix = prefix + 'SFP2-'
        _dict = {
            prefix + '02C3' + suffix : { 'sfp2' : [family_data['sfp2']['index'][0]]},
            prefix + '03C2' + suffix : { 'sfp2' : [family_data['sfp2']['index'][1]]},
            prefix + '06C3' + suffix : { 'sfp2' : [family_data['sfp2']['index'][2]]},
            prefix + '07C2' + suffix : { 'sfp2' : [family_data['sfp2']['index'][3]]},
            prefix + '10C3' + suffix : { 'sfp2' : [family_data['sfp2']['index'][4]]},
            prefix + '11C2' + suffix : { 'sfp2' : [family_data['sfp2']['index'][5]]},
            prefix + '14C3' + suffix : { 'sfp2' : [family_data['sfp2']['index'][6]]},
            prefix + '15C2' + suffix : { 'sfp2' : [family_data['sfp2']['index'][7]]},
            prefix + '18C3' + suffix : { 'sfp2' : [family_data['sfp2']['index'][8]]},
            prefix + '19C2' + suffix : { 'sfp2' : [family_data['sfp2']['index'][9]]},
        }
        return _dict

    if element.lower() == 'pmm':
        prefix = prefix + 'PMM-'
        _dict = {prefix + '01M2' + suffix: {'pmm' : family_data['pmm']['index']}}
        return _dict

    if element.lower() == 'kick' or element.lower() == 'kicker' or element.lower() == 'kick_in':
        prefix = prefix + 'KICKERINJ-'
        _dict = {prefix + '01M2' + suffix: {'kick_in' : family_data['kick_in']['index']}}
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_device_names(accelerator, 'sima')
    _dict.update(get_device_names(accelerator, 'sipm'))
    return _dict
