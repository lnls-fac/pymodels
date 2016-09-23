
from . import families as _families

system = 'si'

_pvnaming_rule = 2 # 1 : PV Naming Proposol#1; 2 : PV Naming Proposol#2
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
        subsystems = ['ap', 'di', 'rf', 'ps', 'ti', 'pu']
        device_names_dict = {}
        for subsystem in subsystems:
            device_names_dict.update(get_device_names(family_data, subsystem))
        return device_names_dict

    if subsystem.lower() == 'rf':
        indices = family_data['cav']['index']
        _dict = {
            join_name(system, subsystem, 'FREQUENCY', _pvnaming_glob) : {'cav':indices},
            join_name(system, subsystem, 'VOLTAGE', _pvnaming_glob)   : {'cav':indices},
        }
        return _dict

    if subsystem.lower() == 'ap':
        _dict = {
                join_name(system, subsystem, 'CHROMX', _pvnaming_glob) : {},
                join_name(system, subsystem, 'CHROMY', _pvnaming_glob) : {},
                join_name(system, subsystem, 'LIFETIME', _pvnaming_glob) : {},
                join_name(system, subsystem, 'BLIFETIME', _pvnaming_glob) : {},
                join_name(system, subsystem, 'SIGX', _pvnaming_glob) : {},
                join_name(system, subsystem, 'SIGY', _pvnaming_glob) : {},
                join_name(system, subsystem, 'SIGS', _pvnaming_glob) : {},
                join_name(system, subsystem, 'EMITX', _pvnaming_glob) : {},
                join_name(system, subsystem, 'EMITY', _pvnaming_glob) : {},
        }
        return _dict

    if subsystem.lower() == 'di':

        _dict = {
            join_name(system, subsystem, 'TunePkp', '01SA') : {},
            join_name(system, subsystem, 'DCCT', '13SA') : {},
        }
        _dict.update(get_element_names(family_data, subsystem, element = 'bpm'))
        _dict.update(get_family_names(family_data, subsystem, family = 'bpm'))
        return _dict

    if subsystem.lower() == 'ps':
        element_dict = {}
        element_dict.update(get_element_names(family_data, subsystem, element = 'quad'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'hcorr'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'vcorr'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'qs'))

        family_dict = {}
        family_dict.update(get_family_names(family_data, subsystem, family = 'bend'))
        family_dict.update(get_family_names(family_data, subsystem, family = 'quad'))
        family_dict.update(get_family_names(family_data, subsystem, family = 'sext'))

        _dict = {}
        _dict.update(element_dict)
        _dict.update(family_dict)
        return _dict

    if subsystem.lower() == 'pu':
        _dict = get_element_names(family_data, subsystem, element='pulsed_magnets')
        return _dict

    if subsystem.lower() == 'ma':
        element_dict = {}
        element_dict.update(get_element_names(family_data, subsystem, element = 'bend'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'quad'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'sext'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'hcorr'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'vcorr'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'qs'))

        return element_dict

    if subsystem.lower() == 'pm':
        _dict = get_element_names(family_data, subsystem, element = 'pulsed_magnets')
        return _dict

    # Examples
    # LI-EGun:TI-STDMOE:TrigDelayCh01 # EGun
    # LI-EGun:TI-STDMOE:TrigEnblCh01 #EGun
    # SI-01SA:TI-SOE:TrigDelayCh01 # OnAxisInjKicker
    # SI-01SA:TI-SOE:TrigEnblCh01 # OnAxisInjKicker
    # TS-04:TI-SOE:TrigEnblCh01 # ThinInjSept
    if subsystem.lower() == 'ti':
        _dict = {
            join_name(system, subsystem, 'SOE', '01SA') : {},
        }
        return _dict

    else:
        raise Exception('Subsystem %s not found'%subsystem)


def get_magnet_names(accelerator):
    _dict = get_device_names(accelerator, 'ma')
    _dict.update(get_device_names(accelerator, 'pm'))
    return _dict


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

    family_names = []
    family_names += _families.families_dipoles()
    family_names += _families.families_quadrupoles()
    family_names += _families.families_sextupoles()
    family_names += ['bpm']

    if family == None:
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, subsystem, family))
        return _dict

    if family == 'bend':
        _dict = {
            join_name(system, subsystem, family.upper(), _pvnaming_fam) :
                {'b1' : family_data['b1']['index'],
                 'b2' : family_data['b2']['index'],
                }
        }
        return _dict

    if family == 'quad':
        family_names = _families.families_quadrupoles()
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, subsystem, family))
        return _dict

    if family == 'sext':
        family_names = _families.families_sextupoles()
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
        elements += _families.families_sextupoles()
        elements += _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        elements += _families.families_skew_correctors()
        elements += _families.families_pulsed_magnets()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'bend':
        _dict = {}
        _dict.update(get_element_names(family_data, subsystem, 'b1'))
        _dict.update(get_element_names(family_data, subsystem, 'b2'))
        _dict.update(get_element_names(family_data, subsystem, 'bc'))
        return _dict

    if element == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'sext':
        elements = _families.families_sextupoles()
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

    if element == 'pulsed_magnets':
        elements = _families.families_pulsed_magnets()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, subsystem, element))
        return _dict

    if element == 'b1':
        _dict = {
            join_name(system, subsystem, element.upper(), '01', '1') : { 'b1' : [family_data['b1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01', '2') : { 'b1' : [family_data['b1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '02', '1') : { 'b1' : [family_data['b1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02', '2') : { 'b1' : [family_data['b1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '03', '1') : { 'b1' : [family_data['b1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '03', '2') : { 'b1' : [family_data['b1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '04', '1') : { 'b1' : [family_data['b1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '04', '2') : { 'b1' : [family_data['b1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '05', '1') : { 'b1' : [family_data['b1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '05', '2') : { 'b1' : [family_data['b1']['index'][9]]},
            join_name(system, subsystem, element.upper(), '06', '1') : { 'b1' : [family_data['b1']['index'][10]]},
            join_name(system, subsystem, element.upper(), '06', '2') : { 'b1' : [family_data['b1']['index'][11]]},
            join_name(system, subsystem, element.upper(), '07', '1') : { 'b1' : [family_data['b1']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07', '2') : { 'b1' : [family_data['b1']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08', '1') : { 'b1' : [family_data['b1']['index'][14]]},
            join_name(system, subsystem, element.upper(), '08', '2') : { 'b1' : [family_data['b1']['index'][15]]},
            join_name(system, subsystem, element.upper(), '09', '1') : { 'b1' : [family_data['b1']['index'][16]]},
            join_name(system, subsystem, element.upper(), '09', '2') : { 'b1' : [family_data['b1']['index'][17]]},
            join_name(system, subsystem, element.upper(), '10', '1') : { 'b1' : [family_data['b1']['index'][18]]},
            join_name(system, subsystem, element.upper(), '10', '2') : { 'b1' : [family_data['b1']['index'][19]]},
            join_name(system, subsystem, element.upper(), '11', '1') : { 'b1' : [family_data['b1']['index'][20]]},
            join_name(system, subsystem, element.upper(), '11', '2') : { 'b1' : [family_data['b1']['index'][21]]},
            join_name(system, subsystem, element.upper(), '12', '1') : { 'b1' : [family_data['b1']['index'][22]]},
            join_name(system, subsystem, element.upper(), '12', '2') : { 'b1' : [family_data['b1']['index'][23]]},
            join_name(system, subsystem, element.upper(), '13', '1') : { 'b1' : [family_data['b1']['index'][24]]},
            join_name(system, subsystem, element.upper(), '13', '2') : { 'b1' : [family_data['b1']['index'][25]]},
            join_name(system, subsystem, element.upper(), '14', '1') : { 'b1' : [family_data['b1']['index'][26]]},
            join_name(system, subsystem, element.upper(), '14', '2') : { 'b1' : [family_data['b1']['index'][27]]},
            join_name(system, subsystem, element.upper(), '15', '1') : { 'b1' : [family_data['b1']['index'][28]]},
            join_name(system, subsystem, element.upper(), '15', '2') : { 'b1' : [family_data['b1']['index'][29]]},
            join_name(system, subsystem, element.upper(), '16', '1') : { 'b1' : [family_data['b1']['index'][30]]},
            join_name(system, subsystem, element.upper(), '16', '2') : { 'b1' : [family_data['b1']['index'][31]]},
            join_name(system, subsystem, element.upper(), '17', '1') : { 'b1' : [family_data['b1']['index'][32]]},
            join_name(system, subsystem, element.upper(), '17', '2') : { 'b1' : [family_data['b1']['index'][33]]},
            join_name(system, subsystem, element.upper(), '18', '1') : { 'b1' : [family_data['b1']['index'][34]]},
            join_name(system, subsystem, element.upper(), '18', '2') : { 'b1' : [family_data['b1']['index'][35]]},
            join_name(system, subsystem, element.upper(), '19', '1') : { 'b1' : [family_data['b1']['index'][36]]},
            join_name(system, subsystem, element.upper(), '19', '2') : { 'b1' : [family_data['b1']['index'][37]]},
            join_name(system, subsystem, element.upper(), '20', '1') : { 'b1' : [family_data['b1']['index'][38]]},
            join_name(system, subsystem, element.upper(), '20', '2') : { 'b1' : [family_data['b1']['index'][39]]},
        }
        return _dict

    if element == 'b2':
        _dict = {
            join_name(system, subsystem, element.upper(), '01', '1') : { 'b2' : [family_data['b2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01', '2') : { 'b2' : [family_data['b2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '02', '1') : { 'b2' : [family_data['b2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02', '2') : { 'b2' : [family_data['b2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '03', '1') : { 'b2' : [family_data['b2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '03', '2') : { 'b2' : [family_data['b2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '04', '1') : { 'b2' : [family_data['b2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '04', '2') : { 'b2' : [family_data['b2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '05', '1') : { 'b2' : [family_data['b2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '05', '2') : { 'b2' : [family_data['b2']['index'][9]]},
            join_name(system, subsystem, element.upper(), '06', '1') : { 'b2' : [family_data['b2']['index'][10]]},
            join_name(system, subsystem, element.upper(), '06', '2') : { 'b2' : [family_data['b2']['index'][11]]},
            join_name(system, subsystem, element.upper(), '07', '1') : { 'b2' : [family_data['b2']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07', '2') : { 'b2' : [family_data['b2']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08', '1') : { 'b2' : [family_data['b2']['index'][14]]},
            join_name(system, subsystem, element.upper(), '08', '2') : { 'b2' : [family_data['b2']['index'][15]]},
            join_name(system, subsystem, element.upper(), '09', '1') : { 'b2' : [family_data['b2']['index'][16]]},
            join_name(system, subsystem, element.upper(), '09', '2') : { 'b2' : [family_data['b2']['index'][17]]},
            join_name(system, subsystem, element.upper(), '10', '1') : { 'b2' : [family_data['b2']['index'][18]]},
            join_name(system, subsystem, element.upper(), '10', '2') : { 'b2' : [family_data['b2']['index'][19]]},
            join_name(system, subsystem, element.upper(), '11', '1') : { 'b2' : [family_data['b2']['index'][20]]},
            join_name(system, subsystem, element.upper(), '11', '2') : { 'b2' : [family_data['b2']['index'][21]]},
            join_name(system, subsystem, element.upper(), '12', '1') : { 'b2' : [family_data['b2']['index'][22]]},
            join_name(system, subsystem, element.upper(), '12', '2') : { 'b2' : [family_data['b2']['index'][23]]},
            join_name(system, subsystem, element.upper(), '13', '1') : { 'b2' : [family_data['b2']['index'][24]]},
            join_name(system, subsystem, element.upper(), '13', '2') : { 'b2' : [family_data['b2']['index'][25]]},
            join_name(system, subsystem, element.upper(), '14', '1') : { 'b2' : [family_data['b2']['index'][26]]},
            join_name(system, subsystem, element.upper(), '14', '2') : { 'b2' : [family_data['b2']['index'][27]]},
            join_name(system, subsystem, element.upper(), '15', '1') : { 'b2' : [family_data['b2']['index'][28]]},
            join_name(system, subsystem, element.upper(), '15', '2') : { 'b2' : [family_data['b2']['index'][29]]},
            join_name(system, subsystem, element.upper(), '16', '1') : { 'b2' : [family_data['b2']['index'][30]]},
            join_name(system, subsystem, element.upper(), '16', '2') : { 'b2' : [family_data['b2']['index'][31]]},
            join_name(system, subsystem, element.upper(), '17', '1') : { 'b2' : [family_data['b2']['index'][32]]},
            join_name(system, subsystem, element.upper(), '17', '2') : { 'b2' : [family_data['b2']['index'][33]]},
            join_name(system, subsystem, element.upper(), '18', '1') : { 'b2' : [family_data['b2']['index'][34]]},
            join_name(system, subsystem, element.upper(), '18', '2') : { 'b2' : [family_data['b2']['index'][35]]},
            join_name(system, subsystem, element.upper(), '19', '1') : { 'b2' : [family_data['b2']['index'][36]]},
            join_name(system, subsystem, element.upper(), '19', '2') : { 'b2' : [family_data['b2']['index'][37]]},
            join_name(system, subsystem, element.upper(), '20', '1') : { 'b2' : [family_data['b2']['index'][38]]},
            join_name(system, subsystem, element.upper(), '20', '2') : { 'b2' : [family_data['b2']['index'][39]]},
        }
        return _dict

    if element == 'bpm':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'bpm' : [family_data['bpm']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C1', '1') : { 'bpm' : [family_data['bpm']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C1', '2') : { 'bpm' : [family_data['bpm']['index'][2]]},
            join_name(system, subsystem, element.upper(), '01C2') : { 'bpm' : [family_data['bpm']['index'][3]]},
            join_name(system, subsystem, element.upper(), '01C3', '1') : { 'bpm' : [family_data['bpm']['index'][4]]},
            join_name(system, subsystem, element.upper(), '01C3', '2') : { 'bpm' : [family_data['bpm']['index'][5]]},
            join_name(system, subsystem, element.upper(), '01C4') : { 'bpm' : [family_data['bpm']['index'][6]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'bpm' : [family_data['bpm']['index'][7]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'bpm' : [family_data['bpm']['index'][8]]},
            join_name(system, subsystem, element.upper(), '02C1', '1') : { 'bpm' : [family_data['bpm']['index'][9]]},
            join_name(system, subsystem, element.upper(), '02C1', '2') : { 'bpm' : [family_data['bpm']['index'][10]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'bpm' : [family_data['bpm']['index'][11]]},
            join_name(system, subsystem, element.upper(), '02C3', '1') : { 'bpm' : [family_data['bpm']['index'][12]]},
            join_name(system, subsystem, element.upper(), '02C3', '2') : { 'bpm' : [family_data['bpm']['index'][13]]},
            join_name(system, subsystem, element.upper(), '02C4') : { 'bpm' : [family_data['bpm']['index'][14]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'bpm' : [family_data['bpm']['index'][15]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'bpm' : [family_data['bpm']['index'][16]]},
            join_name(system, subsystem, element.upper(), '03C1', '1') : { 'bpm' : [family_data['bpm']['index'][17]]},
            join_name(system, subsystem, element.upper(), '03C1', '2') : { 'bpm' : [family_data['bpm']['index'][18]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'bpm' : [family_data['bpm']['index'][19]]},
            join_name(system, subsystem, element.upper(), '03C3', '1') : { 'bpm' : [family_data['bpm']['index'][20]]},
            join_name(system, subsystem, element.upper(), '03C3', '2') : { 'bpm' : [family_data['bpm']['index'][21]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'bpm' : [family_data['bpm']['index'][22]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'bpm' : [family_data['bpm']['index'][23]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'bpm' : [family_data['bpm']['index'][24]]},
            join_name(system, subsystem, element.upper(), '04C1', '1') : { 'bpm' : [family_data['bpm']['index'][25]]},
            join_name(system, subsystem, element.upper(), '04C1', '2') : { 'bpm' : [family_data['bpm']['index'][26]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'bpm' : [family_data['bpm']['index'][27]]},
            join_name(system, subsystem, element.upper(), '04C3', '1') : { 'bpm' : [family_data['bpm']['index'][28]]},
            join_name(system, subsystem, element.upper(), '04C3', '2') : { 'bpm' : [family_data['bpm']['index'][29]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'bpm' : [family_data['bpm']['index'][30]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'bpm' : [family_data['bpm']['index'][31]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'bpm' : [family_data['bpm']['index'][32]]},
            join_name(system, subsystem, element.upper(), '05C1', '1') : { 'bpm' : [family_data['bpm']['index'][33]]},
            join_name(system, subsystem, element.upper(), '05C1', '2') : { 'bpm' : [family_data['bpm']['index'][34]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'bpm' : [family_data['bpm']['index'][35]]},
            join_name(system, subsystem, element.upper(), '05C3', '1') : { 'bpm' : [family_data['bpm']['index'][36]]},
            join_name(system, subsystem, element.upper(), '05C3', '2') : { 'bpm' : [family_data['bpm']['index'][37]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'bpm' : [family_data['bpm']['index'][38]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'bpm' : [family_data['bpm']['index'][39]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'bpm' : [family_data['bpm']['index'][40]]},
            join_name(system, subsystem, element.upper(), '06C1', '1') : { 'bpm' : [family_data['bpm']['index'][41]]},
            join_name(system, subsystem, element.upper(), '06C1', '2') : { 'bpm' : [family_data['bpm']['index'][42]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'bpm' : [family_data['bpm']['index'][43]]},
            join_name(system, subsystem, element.upper(), '06C3', '1') : { 'bpm' : [family_data['bpm']['index'][44]]},
            join_name(system, subsystem, element.upper(), '06C3', '2') : { 'bpm' : [family_data['bpm']['index'][45]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'bpm' : [family_data['bpm']['index'][46]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'bpm' : [family_data['bpm']['index'][47]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'bpm' : [family_data['bpm']['index'][48]]},
            join_name(system, subsystem, element.upper(), '07C1', '1') : { 'bpm' : [family_data['bpm']['index'][49]]},
            join_name(system, subsystem, element.upper(), '07C1', '2') : { 'bpm' : [family_data['bpm']['index'][50]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'bpm' : [family_data['bpm']['index'][51]]},
            join_name(system, subsystem, element.upper(), '07C3', '1') : { 'bpm' : [family_data['bpm']['index'][52]]},
            join_name(system, subsystem, element.upper(), '07C3', '2') : { 'bpm' : [family_data['bpm']['index'][53]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'bpm' : [family_data['bpm']['index'][54]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'bpm' : [family_data['bpm']['index'][55]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'bpm' : [family_data['bpm']['index'][56]]},
            join_name(system, subsystem, element.upper(), '08C1', '1') : { 'bpm' : [family_data['bpm']['index'][57]]},
            join_name(system, subsystem, element.upper(), '08C1', '2') : { 'bpm' : [family_data['bpm']['index'][58]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'bpm' : [family_data['bpm']['index'][59]]},
            join_name(system, subsystem, element.upper(), '08C3', '1') : { 'bpm' : [family_data['bpm']['index'][60]]},
            join_name(system, subsystem, element.upper(), '08C3', '2') : { 'bpm' : [family_data['bpm']['index'][61]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'bpm' : [family_data['bpm']['index'][62]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'bpm' : [family_data['bpm']['index'][63]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'bpm' : [family_data['bpm']['index'][64]]},
            join_name(system, subsystem, element.upper(), '09C1', '1') : { 'bpm' : [family_data['bpm']['index'][65]]},
            join_name(system, subsystem, element.upper(), '09C1', '2') : { 'bpm' : [family_data['bpm']['index'][66]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'bpm' : [family_data['bpm']['index'][67]]},
            join_name(system, subsystem, element.upper(), '09C3', '1') : { 'bpm' : [family_data['bpm']['index'][68]]},
            join_name(system, subsystem, element.upper(), '09C3', '2') : { 'bpm' : [family_data['bpm']['index'][69]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'bpm' : [family_data['bpm']['index'][70]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'bpm' : [family_data['bpm']['index'][71]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'bpm' : [family_data['bpm']['index'][72]]},
            join_name(system, subsystem, element.upper(), '10C1', '1') : { 'bpm' : [family_data['bpm']['index'][73]]},
            join_name(system, subsystem, element.upper(), '10C1', '2') : { 'bpm' : [family_data['bpm']['index'][74]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'bpm' : [family_data['bpm']['index'][75]]},
            join_name(system, subsystem, element.upper(), '10C3', '1') : { 'bpm' : [family_data['bpm']['index'][76]]},
            join_name(system, subsystem, element.upper(), '10C3', '2') : { 'bpm' : [family_data['bpm']['index'][77]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'bpm' : [family_data['bpm']['index'][78]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'bpm' : [family_data['bpm']['index'][79]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'bpm' : [family_data['bpm']['index'][80]]},
            join_name(system, subsystem, element.upper(), '11C1', '1') : { 'bpm' : [family_data['bpm']['index'][81]]},
            join_name(system, subsystem, element.upper(), '11C1', '2') : { 'bpm' : [family_data['bpm']['index'][82]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'bpm' : [family_data['bpm']['index'][83]]},
            join_name(system, subsystem, element.upper(), '11C3', '1') : { 'bpm' : [family_data['bpm']['index'][84]]},
            join_name(system, subsystem, element.upper(), '11C3', '2') : { 'bpm' : [family_data['bpm']['index'][85]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'bpm' : [family_data['bpm']['index'][86]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'bpm' : [family_data['bpm']['index'][87]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'bpm' : [family_data['bpm']['index'][88]]},
            join_name(system, subsystem, element.upper(), '12C1', '1') : { 'bpm' : [family_data['bpm']['index'][89]]},
            join_name(system, subsystem, element.upper(), '12C1', '2') : { 'bpm' : [family_data['bpm']['index'][90]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'bpm' : [family_data['bpm']['index'][91]]},
            join_name(system, subsystem, element.upper(), '12C3', '1') : { 'bpm' : [family_data['bpm']['index'][92]]},
            join_name(system, subsystem, element.upper(), '12C3', '2') : { 'bpm' : [family_data['bpm']['index'][93]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'bpm' : [family_data['bpm']['index'][94]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'bpm' : [family_data['bpm']['index'][95]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'bpm' : [family_data['bpm']['index'][96]]},
            join_name(system, subsystem, element.upper(), '13C1', '1') : { 'bpm' : [family_data['bpm']['index'][97]]},
            join_name(system, subsystem, element.upper(), '13C1', '2') : { 'bpm' : [family_data['bpm']['index'][98]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'bpm' : [family_data['bpm']['index'][99]]},
            join_name(system, subsystem, element.upper(), '13C3', '1') : { 'bpm' : [family_data['bpm']['index'][100]]},
            join_name(system, subsystem, element.upper(), '13C3', '2') : { 'bpm' : [family_data['bpm']['index'][101]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'bpm' : [family_data['bpm']['index'][102]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'bpm' : [family_data['bpm']['index'][103]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'bpm' : [family_data['bpm']['index'][104]]},
            join_name(system, subsystem, element.upper(), '14C1', '1') : { 'bpm' : [family_data['bpm']['index'][105]]},
            join_name(system, subsystem, element.upper(), '14C1', '2') : { 'bpm' : [family_data['bpm']['index'][106]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'bpm' : [family_data['bpm']['index'][107]]},
            join_name(system, subsystem, element.upper(), '14C3', '1') : { 'bpm' : [family_data['bpm']['index'][108]]},
            join_name(system, subsystem, element.upper(), '14C3', '2') : { 'bpm' : [family_data['bpm']['index'][109]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'bpm' : [family_data['bpm']['index'][110]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'bpm' : [family_data['bpm']['index'][111]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'bpm' : [family_data['bpm']['index'][112]]},
            join_name(system, subsystem, element.upper(), '15C1', '1') : { 'bpm' : [family_data['bpm']['index'][113]]},
            join_name(system, subsystem, element.upper(), '15C1', '2') : { 'bpm' : [family_data['bpm']['index'][114]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'bpm' : [family_data['bpm']['index'][115]]},
            join_name(system, subsystem, element.upper(), '15C3', '1') : { 'bpm' : [family_data['bpm']['index'][116]]},
            join_name(system, subsystem, element.upper(), '15C3', '2') : { 'bpm' : [family_data['bpm']['index'][117]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'bpm' : [family_data['bpm']['index'][118]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'bpm' : [family_data['bpm']['index'][119]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'bpm' : [family_data['bpm']['index'][120]]},
            join_name(system, subsystem, element.upper(), '16C1', '1') : { 'bpm' : [family_data['bpm']['index'][121]]},
            join_name(system, subsystem, element.upper(), '16C1', '2') : { 'bpm' : [family_data['bpm']['index'][122]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'bpm' : [family_data['bpm']['index'][123]]},
            join_name(system, subsystem, element.upper(), '16C3', '1') : { 'bpm' : [family_data['bpm']['index'][124]]},
            join_name(system, subsystem, element.upper(), '16C3', '2') : { 'bpm' : [family_data['bpm']['index'][125]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'bpm' : [family_data['bpm']['index'][126]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'bpm' : [family_data['bpm']['index'][127]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'bpm' : [family_data['bpm']['index'][128]]},
            join_name(system, subsystem, element.upper(), '17C1', '1') : { 'bpm' : [family_data['bpm']['index'][129]]},
            join_name(system, subsystem, element.upper(), '17C1', '2') : { 'bpm' : [family_data['bpm']['index'][130]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'bpm' : [family_data['bpm']['index'][131]]},
            join_name(system, subsystem, element.upper(), '17C3', '1') : { 'bpm' : [family_data['bpm']['index'][132]]},
            join_name(system, subsystem, element.upper(), '17C3', '2') : { 'bpm' : [family_data['bpm']['index'][133]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'bpm' : [family_data['bpm']['index'][134]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'bpm' : [family_data['bpm']['index'][135]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'bpm' : [family_data['bpm']['index'][136]]},
            join_name(system, subsystem, element.upper(), '18C1', '1') : { 'bpm' : [family_data['bpm']['index'][137]]},
            join_name(system, subsystem, element.upper(), '18C1', '2') : { 'bpm' : [family_data['bpm']['index'][138]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'bpm' : [family_data['bpm']['index'][139]]},
            join_name(system, subsystem, element.upper(), '18C3', '1') : { 'bpm' : [family_data['bpm']['index'][140]]},
            join_name(system, subsystem, element.upper(), '18C3', '2') : { 'bpm' : [family_data['bpm']['index'][141]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'bpm' : [family_data['bpm']['index'][142]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'bpm' : [family_data['bpm']['index'][143]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'bpm' : [family_data['bpm']['index'][144]]},
            join_name(system, subsystem, element.upper(), '19C1', '1') : { 'bpm' : [family_data['bpm']['index'][145]]},
            join_name(system, subsystem, element.upper(), '19C1', '2') : { 'bpm' : [family_data['bpm']['index'][146]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'bpm' : [family_data['bpm']['index'][147]]},
            join_name(system, subsystem, element.upper(), '19C3', '1') : { 'bpm' : [family_data['bpm']['index'][148]]},
            join_name(system, subsystem, element.upper(), '19C3', '2') : { 'bpm' : [family_data['bpm']['index'][149]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'bpm' : [family_data['bpm']['index'][150]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'bpm' : [family_data['bpm']['index'][151]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'bpm' : [family_data['bpm']['index'][152]]},
            join_name(system, subsystem, element.upper(), '20C1', '1') : { 'bpm' : [family_data['bpm']['index'][153]]},
            join_name(system, subsystem, element.upper(), '20C1', '2') : { 'bpm' : [family_data['bpm']['index'][154]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'bpm' : [family_data['bpm']['index'][155]]},
            join_name(system, subsystem, element.upper(), '20C3', '1') : { 'bpm' : [family_data['bpm']['index'][156]]},
            join_name(system, subsystem, element.upper(), '20C3', '2') : { 'bpm' : [family_data['bpm']['index'][157]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'bpm' : [family_data['bpm']['index'][158]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'bpm' : [family_data['bpm']['index'][159]]},
        }
        return _dict


    if element == 'bc':
        _dict = {
            join_name(system, subsystem, element.upper(), '01'): {'bc' : sorted([family_data['bc_lf']['index'][0]] + [family_data['bc_hf']['index'][0]])},
            join_name(system, subsystem, element.upper(), '02'): {'bc' : sorted([family_data['bc_lf']['index'][1]] + [family_data['bc_hf']['index'][1]])},
            join_name(system, subsystem, element.upper(), '03'): {'bc' : sorted([family_data['bc_lf']['index'][2]] + [family_data['bc_hf']['index'][2]])},
            join_name(system, subsystem, element.upper(), '04'): {'bc' : sorted([family_data['bc_lf']['index'][3]] + [family_data['bc_hf']['index'][3]])},
            join_name(system, subsystem, element.upper(), '05'): {'bc' : sorted([family_data['bc_lf']['index'][4]] + [family_data['bc_hf']['index'][4]])},
            join_name(system, subsystem, element.upper(), '06'): {'bc' : sorted([family_data['bc_lf']['index'][5]] + [family_data['bc_hf']['index'][5]])},
            join_name(system, subsystem, element.upper(), '07'): {'bc' : sorted([family_data['bc_lf']['index'][6]] + [family_data['bc_hf']['index'][6]])},
            join_name(system, subsystem, element.upper(), '08'): {'bc' : sorted([family_data['bc_lf']['index'][7]] + [family_data['bc_hf']['index'][7]])},
            join_name(system, subsystem, element.upper(), '09'): {'bc' : sorted([family_data['bc_lf']['index'][8]] + [family_data['bc_hf']['index'][8]])},
            join_name(system, subsystem, element.upper(), '10'): {'bc' : sorted([family_data['bc_lf']['index'][9]] + [family_data['bc_hf']['index'][9]])},
            join_name(system, subsystem, element.upper(), '11'): {'bc' : sorted([family_data['bc_lf']['index'][10]] + [family_data['bc_hf']['index'][10]])},
            join_name(system, subsystem, element.upper(), '12'): {'bc' : sorted([family_data['bc_lf']['index'][11]] + [family_data['bc_hf']['index'][11]])},
            join_name(system, subsystem, element.upper(), '13'): {'bc' : sorted([family_data['bc_lf']['index'][12]] + [family_data['bc_hf']['index'][12]])},
            join_name(system, subsystem, element.upper(), '14'): {'bc' : sorted([family_data['bc_lf']['index'][13]] + [family_data['bc_hf']['index'][13]])},
            join_name(system, subsystem, element.upper(), '15'): {'bc' : sorted([family_data['bc_lf']['index'][14]] + [family_data['bc_hf']['index'][14]])},
            join_name(system, subsystem, element.upper(), '16'): {'bc' : sorted([family_data['bc_lf']['index'][15]] + [family_data['bc_hf']['index'][15]])},
            join_name(system, subsystem, element.upper(), '17'): {'bc' : sorted([family_data['bc_lf']['index'][16]] + [family_data['bc_hf']['index'][16]])},
            join_name(system, subsystem, element.upper(), '18'): {'bc' : sorted([family_data['bc_lf']['index'][17]] + [family_data['bc_hf']['index'][17]])},
            join_name(system, subsystem, element.upper(), '19'): {'bc' : sorted([family_data['bc_lf']['index'][18]] + [family_data['bc_hf']['index'][18]])},
            join_name(system, subsystem, element.upper(), '20'): {'bc' : sorted([family_data['bc_lf']['index'][19]] + [family_data['bc_hf']['index'][19]])},
        }
        return _dict


    if element == 'fch':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'fch' : [family_data['fch']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C2') : { 'fch' : [family_data['fch']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'fch' : [family_data['fch']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'fch' : [family_data['fch']['index'][3]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'fch' : [family_data['fch']['index'][4]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'fch' : [family_data['fch']['index'][5]]},
            join_name(system, subsystem, element.upper(), '02C3') : { 'fch' : [family_data['fch']['index'][6]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'fch' : [family_data['fch']['index'][7]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'fch' : [family_data['fch']['index'][8]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'fch' : [family_data['fch']['index'][9]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'fch' : [family_data['fch']['index'][10]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'fch' : [family_data['fch']['index'][11]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'fch' : [family_data['fch']['index'][12]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'fch' : [family_data['fch']['index'][13]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'fch' : [family_data['fch']['index'][14]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'fch' : [family_data['fch']['index'][15]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'fch' : [family_data['fch']['index'][16]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'fch' : [family_data['fch']['index'][17]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'fch' : [family_data['fch']['index'][18]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'fch' : [family_data['fch']['index'][19]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'fch' : [family_data['fch']['index'][20]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'fch' : [family_data['fch']['index'][21]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'fch' : [family_data['fch']['index'][22]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'fch' : [family_data['fch']['index'][23]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'fch' : [family_data['fch']['index'][24]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'fch' : [family_data['fch']['index'][25]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'fch' : [family_data['fch']['index'][26]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'fch' : [family_data['fch']['index'][27]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'fch' : [family_data['fch']['index'][28]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'fch' : [family_data['fch']['index'][29]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'fch' : [family_data['fch']['index'][30]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'fch' : [family_data['fch']['index'][31]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'fch' : [family_data['fch']['index'][32]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'fch' : [family_data['fch']['index'][33]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'fch' : [family_data['fch']['index'][34]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'fch' : [family_data['fch']['index'][35]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'fch' : [family_data['fch']['index'][36]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'fch' : [family_data['fch']['index'][37]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'fch' : [family_data['fch']['index'][38]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'fch' : [family_data['fch']['index'][39]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'fch' : [family_data['fch']['index'][40]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'fch' : [family_data['fch']['index'][41]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'fch' : [family_data['fch']['index'][42]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'fch' : [family_data['fch']['index'][43]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'fch' : [family_data['fch']['index'][44]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'fch' : [family_data['fch']['index'][45]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'fch' : [family_data['fch']['index'][46]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'fch' : [family_data['fch']['index'][47]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'fch' : [family_data['fch']['index'][48]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'fch' : [family_data['fch']['index'][49]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'fch' : [family_data['fch']['index'][50]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'fch' : [family_data['fch']['index'][51]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'fch' : [family_data['fch']['index'][52]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'fch' : [family_data['fch']['index'][53]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'fch' : [family_data['fch']['index'][54]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'fch' : [family_data['fch']['index'][55]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'fch' : [family_data['fch']['index'][56]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'fch' : [family_data['fch']['index'][57]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'fch' : [family_data['fch']['index'][58]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'fch' : [family_data['fch']['index'][59]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'fch' : [family_data['fch']['index'][60]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'fch' : [family_data['fch']['index'][61]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'fch' : [family_data['fch']['index'][62]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'fch' : [family_data['fch']['index'][63]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'fch' : [family_data['fch']['index'][64]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'fch' : [family_data['fch']['index'][65]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'fch' : [family_data['fch']['index'][66]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'fch' : [family_data['fch']['index'][67]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'fch' : [family_data['fch']['index'][68]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'fch' : [family_data['fch']['index'][69]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'fch' : [family_data['fch']['index'][70]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'fch' : [family_data['fch']['index'][71]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'fch' : [family_data['fch']['index'][72]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'fch' : [family_data['fch']['index'][73]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'fch' : [family_data['fch']['index'][74]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'fch' : [family_data['fch']['index'][75]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'fch' : [family_data['fch']['index'][76]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'fch' : [family_data['fch']['index'][77]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'fch' : [family_data['fch']['index'][78]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'fch' : [family_data['fch']['index'][79]]},
        }
        return _dict

    if element == 'cv':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'cv' : [family_data['cv']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C1') : { 'cv' : [family_data['cv']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C2', '1') : { 'cv' : [family_data['cv']['index'][2]]},
            join_name(system, subsystem, element.upper(), '01C2', '2') : { 'cv' : [family_data['cv']['index'][3]]},
            join_name(system, subsystem, element.upper(), '01C3', '1') : { 'cv' : [family_data['cv']['index'][4]]},
            join_name(system, subsystem, element.upper(), '01C3', '2') : { 'cv' : [family_data['cv']['index'][5]]},
            join_name(system, subsystem, element.upper(), '01C4') : { 'cv' : [family_data['cv']['index'][6]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'cv' : [family_data['cv']['index'][7]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'cv' : [family_data['cv']['index'][8]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'cv' : [family_data['cv']['index'][9]]},
            join_name(system, subsystem, element.upper(), '02C2', '1') : { 'cv' : [family_data['cv']['index'][10]]},
            join_name(system, subsystem, element.upper(), '02C2', '2') : { 'cv' : [family_data['cv']['index'][11]]},
            join_name(system, subsystem, element.upper(), '02C3', '1') : { 'cv' : [family_data['cv']['index'][12]]},
            join_name(system, subsystem, element.upper(), '02C3', '2') : { 'cv' : [family_data['cv']['index'][13]]},
            join_name(system, subsystem, element.upper(), '02C4') : { 'cv' : [family_data['cv']['index'][14]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'cv' : [family_data['cv']['index'][15]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'cv' : [family_data['cv']['index'][16]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'cv' : [family_data['cv']['index'][17]]},
            join_name(system, subsystem, element.upper(), '03C2', '1') : { 'cv' : [family_data['cv']['index'][18]]},
            join_name(system, subsystem, element.upper(), '03C2', '2') : { 'cv' : [family_data['cv']['index'][19]]},
            join_name(system, subsystem, element.upper(), '03C3', '1') : { 'cv' : [family_data['cv']['index'][20]]},
            join_name(system, subsystem, element.upper(), '03C3', '2') : { 'cv' : [family_data['cv']['index'][21]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'cv' : [family_data['cv']['index'][22]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'cv' : [family_data['cv']['index'][23]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'cv' : [family_data['cv']['index'][24]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'cv' : [family_data['cv']['index'][25]]},
            join_name(system, subsystem, element.upper(), '04C2', '1') : { 'cv' : [family_data['cv']['index'][26]]},
            join_name(system, subsystem, element.upper(), '04C2', '2') : { 'cv' : [family_data['cv']['index'][27]]},
            join_name(system, subsystem, element.upper(), '04C3', '1') : { 'cv' : [family_data['cv']['index'][28]]},
            join_name(system, subsystem, element.upper(), '04C3', '2') : { 'cv' : [family_data['cv']['index'][29]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'cv' : [family_data['cv']['index'][30]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'cv' : [family_data['cv']['index'][31]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'cv' : [family_data['cv']['index'][32]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'cv' : [family_data['cv']['index'][33]]},
            join_name(system, subsystem, element.upper(), '05C2', '1') : { 'cv' : [family_data['cv']['index'][34]]},
            join_name(system, subsystem, element.upper(), '05C2', '2') : { 'cv' : [family_data['cv']['index'][35]]},
            join_name(system, subsystem, element.upper(), '05C3', '1') : { 'cv' : [family_data['cv']['index'][36]]},
            join_name(system, subsystem, element.upper(), '05C3', '2') : { 'cv' : [family_data['cv']['index'][37]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'cv' : [family_data['cv']['index'][38]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'cv' : [family_data['cv']['index'][39]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'cv' : [family_data['cv']['index'][40]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'cv' : [family_data['cv']['index'][41]]},
            join_name(system, subsystem, element.upper(), '06C2', '1') : { 'cv' : [family_data['cv']['index'][42]]},
            join_name(system, subsystem, element.upper(), '06C2', '2') : { 'cv' : [family_data['cv']['index'][43]]},
            join_name(system, subsystem, element.upper(), '06C3', '1') : { 'cv' : [family_data['cv']['index'][44]]},
            join_name(system, subsystem, element.upper(), '06C3', '2') : { 'cv' : [family_data['cv']['index'][45]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'cv' : [family_data['cv']['index'][46]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'cv' : [family_data['cv']['index'][47]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'cv' : [family_data['cv']['index'][48]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'cv' : [family_data['cv']['index'][49]]},
            join_name(system, subsystem, element.upper(), '07C2', '1') : { 'cv' : [family_data['cv']['index'][50]]},
            join_name(system, subsystem, element.upper(), '07C2', '2') : { 'cv' : [family_data['cv']['index'][51]]},
            join_name(system, subsystem, element.upper(), '07C3', '1') : { 'cv' : [family_data['cv']['index'][52]]},
            join_name(system, subsystem, element.upper(), '07C3', '2') : { 'cv' : [family_data['cv']['index'][53]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'cv' : [family_data['cv']['index'][54]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'cv' : [family_data['cv']['index'][55]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'cv' : [family_data['cv']['index'][56]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'cv' : [family_data['cv']['index'][57]]},
            join_name(system, subsystem, element.upper(), '08C2', '1') : { 'cv' : [family_data['cv']['index'][58]]},
            join_name(system, subsystem, element.upper(), '08C2', '2') : { 'cv' : [family_data['cv']['index'][59]]},
            join_name(system, subsystem, element.upper(), '08C3', '1') : { 'cv' : [family_data['cv']['index'][60]]},
            join_name(system, subsystem, element.upper(), '08C3', '2') : { 'cv' : [family_data['cv']['index'][61]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'cv' : [family_data['cv']['index'][62]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'cv' : [family_data['cv']['index'][63]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'cv' : [family_data['cv']['index'][64]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'cv' : [family_data['cv']['index'][65]]},
            join_name(system, subsystem, element.upper(), '09C2', '1') : { 'cv' : [family_data['cv']['index'][66]]},
            join_name(system, subsystem, element.upper(), '09C2', '2') : { 'cv' : [family_data['cv']['index'][67]]},
            join_name(system, subsystem, element.upper(), '09C3', '1') : { 'cv' : [family_data['cv']['index'][68]]},
            join_name(system, subsystem, element.upper(), '09C3', '2') : { 'cv' : [family_data['cv']['index'][69]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'cv' : [family_data['cv']['index'][70]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'cv' : [family_data['cv']['index'][71]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'cv' : [family_data['cv']['index'][72]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'cv' : [family_data['cv']['index'][73]]},
            join_name(system, subsystem, element.upper(), '10C2', '1') : { 'cv' : [family_data['cv']['index'][74]]},
            join_name(system, subsystem, element.upper(), '10C2', '2') : { 'cv' : [family_data['cv']['index'][75]]},
            join_name(system, subsystem, element.upper(), '10C3', '1') : { 'cv' : [family_data['cv']['index'][76]]},
            join_name(system, subsystem, element.upper(), '10C3', '2') : { 'cv' : [family_data['cv']['index'][77]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'cv' : [family_data['cv']['index'][78]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'cv' : [family_data['cv']['index'][79]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'cv' : [family_data['cv']['index'][80]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'cv' : [family_data['cv']['index'][81]]},
            join_name(system, subsystem, element.upper(), '11C2', '1') : { 'cv' : [family_data['cv']['index'][82]]},
            join_name(system, subsystem, element.upper(), '11C2', '2') : { 'cv' : [family_data['cv']['index'][83]]},
            join_name(system, subsystem, element.upper(), '11C3', '1') : { 'cv' : [family_data['cv']['index'][84]]},
            join_name(system, subsystem, element.upper(), '11C3', '2') : { 'cv' : [family_data['cv']['index'][85]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'cv' : [family_data['cv']['index'][86]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'cv' : [family_data['cv']['index'][87]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'cv' : [family_data['cv']['index'][88]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'cv' : [family_data['cv']['index'][89]]},
            join_name(system, subsystem, element.upper(), '12C2', '1') : { 'cv' : [family_data['cv']['index'][90]]},
            join_name(system, subsystem, element.upper(), '12C2', '2') : { 'cv' : [family_data['cv']['index'][91]]},
            join_name(system, subsystem, element.upper(), '12C3', '1') : { 'cv' : [family_data['cv']['index'][92]]},
            join_name(system, subsystem, element.upper(), '12C3', '2') : { 'cv' : [family_data['cv']['index'][93]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'cv' : [family_data['cv']['index'][94]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'cv' : [family_data['cv']['index'][95]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'cv' : [family_data['cv']['index'][96]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'cv' : [family_data['cv']['index'][97]]},
            join_name(system, subsystem, element.upper(), '13C2', '1') : { 'cv' : [family_data['cv']['index'][98]]},
            join_name(system, subsystem, element.upper(), '13C2', '2') : { 'cv' : [family_data['cv']['index'][99]]},
            join_name(system, subsystem, element.upper(), '13C3', '1') : { 'cv' : [family_data['cv']['index'][100]]},
            join_name(system, subsystem, element.upper(), '13C3', '2') : { 'cv' : [family_data['cv']['index'][101]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'cv' : [family_data['cv']['index'][102]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'cv' : [family_data['cv']['index'][103]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'cv' : [family_data['cv']['index'][104]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'cv' : [family_data['cv']['index'][105]]},
            join_name(system, subsystem, element.upper(), '14C2', '1') : { 'cv' : [family_data['cv']['index'][106]]},
            join_name(system, subsystem, element.upper(), '14C2', '2') : { 'cv' : [family_data['cv']['index'][107]]},
            join_name(system, subsystem, element.upper(), '14C3', '1') : { 'cv' : [family_data['cv']['index'][108]]},
            join_name(system, subsystem, element.upper(), '14C3', '2') : { 'cv' : [family_data['cv']['index'][109]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'cv' : [family_data['cv']['index'][110]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'cv' : [family_data['cv']['index'][111]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'cv' : [family_data['cv']['index'][112]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'cv' : [family_data['cv']['index'][113]]},
            join_name(system, subsystem, element.upper(), '15C2', '1') : { 'cv' : [family_data['cv']['index'][114]]},
            join_name(system, subsystem, element.upper(), '15C2', '2') : { 'cv' : [family_data['cv']['index'][115]]},
            join_name(system, subsystem, element.upper(), '15C3', '1') : { 'cv' : [family_data['cv']['index'][116]]},
            join_name(system, subsystem, element.upper(), '15C3', '2') : { 'cv' : [family_data['cv']['index'][117]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'cv' : [family_data['cv']['index'][118]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'cv' : [family_data['cv']['index'][119]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'cv' : [family_data['cv']['index'][120]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'cv' : [family_data['cv']['index'][121]]},
            join_name(system, subsystem, element.upper(), '16C2', '1') : { 'cv' : [family_data['cv']['index'][122]]},
            join_name(system, subsystem, element.upper(), '16C2', '2') : { 'cv' : [family_data['cv']['index'][123]]},
            join_name(system, subsystem, element.upper(), '16C3', '1') : { 'cv' : [family_data['cv']['index'][124]]},
            join_name(system, subsystem, element.upper(), '16C3', '2') : { 'cv' : [family_data['cv']['index'][125]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'cv' : [family_data['cv']['index'][126]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'cv' : [family_data['cv']['index'][127]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'cv' : [family_data['cv']['index'][128]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'cv' : [family_data['cv']['index'][129]]},
            join_name(system, subsystem, element.upper(), '17C2', '1') : { 'cv' : [family_data['cv']['index'][130]]},
            join_name(system, subsystem, element.upper(), '17C2', '2') : { 'cv' : [family_data['cv']['index'][131]]},
            join_name(system, subsystem, element.upper(), '17C3', '1') : { 'cv' : [family_data['cv']['index'][132]]},
            join_name(system, subsystem, element.upper(), '17C3', '2') : { 'cv' : [family_data['cv']['index'][133]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'cv' : [family_data['cv']['index'][134]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'cv' : [family_data['cv']['index'][135]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'cv' : [family_data['cv']['index'][136]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'cv' : [family_data['cv']['index'][137]]},
            join_name(system, subsystem, element.upper(), '18C2', '1') : { 'cv' : [family_data['cv']['index'][138]]},
            join_name(system, subsystem, element.upper(), '18C2', '2') : { 'cv' : [family_data['cv']['index'][139]]},
            join_name(system, subsystem, element.upper(), '18C3', '1') : { 'cv' : [family_data['cv']['index'][140]]},
            join_name(system, subsystem, element.upper(), '18C3', '2') : { 'cv' : [family_data['cv']['index'][141]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'cv' : [family_data['cv']['index'][142]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'cv' : [family_data['cv']['index'][143]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'cv' : [family_data['cv']['index'][144]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'cv' : [family_data['cv']['index'][145]]},
            join_name(system, subsystem, element.upper(), '19C2', '1') : { 'cv' : [family_data['cv']['index'][146]]},
            join_name(system, subsystem, element.upper(), '19C2', '2') : { 'cv' : [family_data['cv']['index'][147]]},
            join_name(system, subsystem, element.upper(), '19C3', '1') : { 'cv' : [family_data['cv']['index'][148]]},
            join_name(system, subsystem, element.upper(), '19C3', '2') : { 'cv' : [family_data['cv']['index'][149]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'cv' : [family_data['cv']['index'][150]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'cv' : [family_data['cv']['index'][151]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'cv' : [family_data['cv']['index'][152]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'cv' : [family_data['cv']['index'][153]]},
            join_name(system, subsystem, element.upper(), '20C2', '1') : { 'cv' : [family_data['cv']['index'][154]]},
            join_name(system, subsystem, element.upper(), '20C2', '2') : { 'cv' : [family_data['cv']['index'][155]]},
            join_name(system, subsystem, element.upper(), '20C3', '1') : { 'cv' : [family_data['cv']['index'][156]]},
            join_name(system, subsystem, element.upper(), '20C3', '2') : { 'cv' : [family_data['cv']['index'][157]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'cv' : [family_data['cv']['index'][158]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'cv' : [family_data['cv']['index'][159]]},
        }
        return _dict

    if element == 'qs':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'qs' : [family_data['qs']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C1') : { 'qs' : [family_data['qs']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C2') : { 'qs' : [family_data['qs']['index'][2]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'qs' : [family_data['qs']['index'][3]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'qs' : [family_data['qs']['index'][4]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'qs' : [family_data['qs']['index'][5]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'qs' : [family_data['qs']['index'][6]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'qs' : [family_data['qs']['index'][7]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'qs' : [family_data['qs']['index'][8]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'qs' : [family_data['qs']['index'][9]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'qs' : [family_data['qs']['index'][10]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'qs' : [family_data['qs']['index'][11]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'qs' : [family_data['qs']['index'][12]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'qs' : [family_data['qs']['index'][13]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'qs' : [family_data['qs']['index'][14]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'qs' : [family_data['qs']['index'][15]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'qs' : [family_data['qs']['index'][16]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'qs' : [family_data['qs']['index'][17]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'qs' : [family_data['qs']['index'][18]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'qs' : [family_data['qs']['index'][19]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'qs' : [family_data['qs']['index'][20]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'qs' : [family_data['qs']['index'][21]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'qs' : [family_data['qs']['index'][22]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'qs' : [family_data['qs']['index'][23]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'qs' : [family_data['qs']['index'][24]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'qs' : [family_data['qs']['index'][25]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'qs' : [family_data['qs']['index'][26]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'qs' : [family_data['qs']['index'][27]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'qs' : [family_data['qs']['index'][28]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'qs' : [family_data['qs']['index'][29]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'qs' : [family_data['qs']['index'][30]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'qs' : [family_data['qs']['index'][31]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'qs' : [family_data['qs']['index'][32]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'qs' : [family_data['qs']['index'][33]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'qs' : [family_data['qs']['index'][34]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'qs' : [family_data['qs']['index'][35]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'qs' : [family_data['qs']['index'][36]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'qs' : [family_data['qs']['index'][37]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'qs' : [family_data['qs']['index'][38]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'qs' : [family_data['qs']['index'][39]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'qs' : [family_data['qs']['index'][40]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'qs' : [family_data['qs']['index'][41]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'qs' : [family_data['qs']['index'][42]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'qs' : [family_data['qs']['index'][43]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'qs' : [family_data['qs']['index'][44]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'qs' : [family_data['qs']['index'][45]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'qs' : [family_data['qs']['index'][46]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'qs' : [family_data['qs']['index'][47]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'qs' : [family_data['qs']['index'][48]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'qs' : [family_data['qs']['index'][49]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'qs' : [family_data['qs']['index'][50]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'qs' : [family_data['qs']['index'][51]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'qs' : [family_data['qs']['index'][52]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'qs' : [family_data['qs']['index'][53]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'qs' : [family_data['qs']['index'][54]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'qs' : [family_data['qs']['index'][55]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'qs' : [family_data['qs']['index'][56]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'qs' : [family_data['qs']['index'][57]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'qs' : [family_data['qs']['index'][58]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'qs' : [family_data['qs']['index'][59]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'qs' : [family_data['qs']['index'][60]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'qs' : [family_data['qs']['index'][61]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'qs' : [family_data['qs']['index'][62]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'qs' : [family_data['qs']['index'][63]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'qs' : [family_data['qs']['index'][64]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'qs' : [family_data['qs']['index'][65]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'qs' : [family_data['qs']['index'][66]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'qs' : [family_data['qs']['index'][67]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'qs' : [family_data['qs']['index'][68]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'qs' : [family_data['qs']['index'][69]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'qs' : [family_data['qs']['index'][70]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'qs' : [family_data['qs']['index'][71]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'qs' : [family_data['qs']['index'][72]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'qs' : [family_data['qs']['index'][73]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'qs' : [family_data['qs']['index'][74]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'qs' : [family_data['qs']['index'][75]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'qs' : [family_data['qs']['index'][76]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'qs' : [family_data['qs']['index'][77]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'qs' : [family_data['qs']['index'][78]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'qs' : [family_data['qs']['index'][79]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'qs' : [family_data['qs']['index'][80]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'qs' : [family_data['qs']['index'][81]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'qs' : [family_data['qs']['index'][82]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'qs' : [family_data['qs']['index'][83]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'qs' : [family_data['qs']['index'][84]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'qs' : [family_data['qs']['index'][85]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'qs' : [family_data['qs']['index'][86]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'qs' : [family_data['qs']['index'][87]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'qs' : [family_data['qs']['index'][88]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'qs' : [family_data['qs']['index'][89]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'qs' : [family_data['qs']['index'][90]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'qs' : [family_data['qs']['index'][91]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'qs' : [family_data['qs']['index'][92]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'qs' : [family_data['qs']['index'][93]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'qs' : [family_data['qs']['index'][94]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'qs' : [family_data['qs']['index'][95]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'qs' : [family_data['qs']['index'][96]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'qs' : [family_data['qs']['index'][97]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'qs' : [family_data['qs']['index'][98]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'qs' : [family_data['qs']['index'][99]]},
        }
        return _dict

    if element == 'ch':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'ch' : [family_data['ch']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C1') : { 'ch' : [family_data['ch']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C2') : { 'ch' : [family_data['ch']['index'][2]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'ch' : [family_data['ch']['index'][3]]},
            join_name(system, subsystem, element.upper(), '01C4') : { 'ch' : [family_data['ch']['index'][4]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'ch' : [family_data['ch']['index'][5]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'ch' : [family_data['ch']['index'][6]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'ch' : [family_data['ch']['index'][7]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'ch' : [family_data['ch']['index'][8]]},
            join_name(system, subsystem, element.upper(), '02C3') : { 'ch' : [family_data['ch']['index'][9]]},
            join_name(system, subsystem, element.upper(), '02C4') : { 'ch' : [family_data['ch']['index'][10]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'ch' : [family_data['ch']['index'][11]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'ch' : [family_data['ch']['index'][12]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'ch' : [family_data['ch']['index'][13]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'ch' : [family_data['ch']['index'][14]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'ch' : [family_data['ch']['index'][15]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'ch' : [family_data['ch']['index'][16]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'ch' : [family_data['ch']['index'][17]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'ch' : [family_data['ch']['index'][18]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'ch' : [family_data['ch']['index'][19]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'ch' : [family_data['ch']['index'][20]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'ch' : [family_data['ch']['index'][21]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'ch' : [family_data['ch']['index'][22]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'ch' : [family_data['ch']['index'][23]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'ch' : [family_data['ch']['index'][24]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'ch' : [family_data['ch']['index'][25]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'ch' : [family_data['ch']['index'][26]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'ch' : [family_data['ch']['index'][27]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'ch' : [family_data['ch']['index'][28]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'ch' : [family_data['ch']['index'][29]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'ch' : [family_data['ch']['index'][30]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'ch' : [family_data['ch']['index'][31]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'ch' : [family_data['ch']['index'][32]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'ch' : [family_data['ch']['index'][33]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'ch' : [family_data['ch']['index'][34]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'ch' : [family_data['ch']['index'][35]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'ch' : [family_data['ch']['index'][36]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'ch' : [family_data['ch']['index'][37]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'ch' : [family_data['ch']['index'][38]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'ch' : [family_data['ch']['index'][39]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'ch' : [family_data['ch']['index'][40]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'ch' : [family_data['ch']['index'][41]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'ch' : [family_data['ch']['index'][42]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'ch' : [family_data['ch']['index'][43]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'ch' : [family_data['ch']['index'][44]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'ch' : [family_data['ch']['index'][45]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'ch' : [family_data['ch']['index'][46]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'ch' : [family_data['ch']['index'][47]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'ch' : [family_data['ch']['index'][48]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'ch' : [family_data['ch']['index'][49]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'ch' : [family_data['ch']['index'][50]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'ch' : [family_data['ch']['index'][51]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'ch' : [family_data['ch']['index'][52]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'ch' : [family_data['ch']['index'][53]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'ch' : [family_data['ch']['index'][54]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'ch' : [family_data['ch']['index'][55]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'ch' : [family_data['ch']['index'][56]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'ch' : [family_data['ch']['index'][57]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'ch' : [family_data['ch']['index'][58]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'ch' : [family_data['ch']['index'][59]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'ch' : [family_data['ch']['index'][60]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'ch' : [family_data['ch']['index'][61]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'ch' : [family_data['ch']['index'][62]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'ch' : [family_data['ch']['index'][63]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'ch' : [family_data['ch']['index'][64]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'ch' : [family_data['ch']['index'][65]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'ch' : [family_data['ch']['index'][66]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'ch' : [family_data['ch']['index'][67]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'ch' : [family_data['ch']['index'][68]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'ch' : [family_data['ch']['index'][69]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'ch' : [family_data['ch']['index'][70]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'ch' : [family_data['ch']['index'][71]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'ch' : [family_data['ch']['index'][72]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'ch' : [family_data['ch']['index'][73]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'ch' : [family_data['ch']['index'][74]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'ch' : [family_data['ch']['index'][75]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'ch' : [family_data['ch']['index'][76]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'ch' : [family_data['ch']['index'][77]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'ch' : [family_data['ch']['index'][78]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'ch' : [family_data['ch']['index'][79]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'ch' : [family_data['ch']['index'][80]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'ch' : [family_data['ch']['index'][81]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'ch' : [family_data['ch']['index'][82]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'ch' : [family_data['ch']['index'][83]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'ch' : [family_data['ch']['index'][84]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'ch' : [family_data['ch']['index'][85]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'ch' : [family_data['ch']['index'][86]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'ch' : [family_data['ch']['index'][87]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'ch' : [family_data['ch']['index'][88]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'ch' : [family_data['ch']['index'][89]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'ch' : [family_data['ch']['index'][90]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'ch' : [family_data['ch']['index'][91]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'ch' : [family_data['ch']['index'][92]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'ch' : [family_data['ch']['index'][93]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'ch' : [family_data['ch']['index'][94]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'ch' : [family_data['ch']['index'][95]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'ch' : [family_data['ch']['index'][96]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'ch' : [family_data['ch']['index'][97]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'ch' : [family_data['ch']['index'][98]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'ch' : [family_data['ch']['index'][99]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'ch' : [family_data['ch']['index'][100]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'ch' : [family_data['ch']['index'][101]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'ch' : [family_data['ch']['index'][102]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'ch' : [family_data['ch']['index'][103]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'ch' : [family_data['ch']['index'][104]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'ch' : [family_data['ch']['index'][105]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'ch' : [family_data['ch']['index'][106]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'ch' : [family_data['ch']['index'][107]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'ch' : [family_data['ch']['index'][108]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'ch' : [family_data['ch']['index'][109]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'ch' : [family_data['ch']['index'][110]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'ch' : [family_data['ch']['index'][111]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'ch' : [family_data['ch']['index'][112]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'ch' : [family_data['ch']['index'][113]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'ch' : [family_data['ch']['index'][114]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'ch' : [family_data['ch']['index'][115]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'ch' : [family_data['ch']['index'][116]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'ch' : [family_data['ch']['index'][117]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'ch' : [family_data['ch']['index'][118]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'ch' : [family_data['ch']['index'][119]]},
        }
        return _dict

    if element == 'fcv':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'fcv' : [family_data['fcv']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C2') : { 'fcv' : [family_data['fcv']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'fcv' : [family_data['fcv']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'fcv' : [family_data['fcv']['index'][3]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'fcv' : [family_data['fcv']['index'][4]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'fcv' : [family_data['fcv']['index'][5]]},
            join_name(system, subsystem, element.upper(), '02C3') : { 'fcv' : [family_data['fcv']['index'][6]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'fcv' : [family_data['fcv']['index'][7]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'fcv' : [family_data['fcv']['index'][8]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'fcv' : [family_data['fcv']['index'][9]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'fcv' : [family_data['fcv']['index'][10]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'fcv' : [family_data['fcv']['index'][11]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'fcv' : [family_data['fcv']['index'][12]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'fcv' : [family_data['fcv']['index'][13]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'fcv' : [family_data['fcv']['index'][14]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'fcv' : [family_data['fcv']['index'][15]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'fcv' : [family_data['fcv']['index'][16]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'fcv' : [family_data['fcv']['index'][17]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'fcv' : [family_data['fcv']['index'][18]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'fcv' : [family_data['fcv']['index'][19]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'fcv' : [family_data['fcv']['index'][20]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'fcv' : [family_data['fcv']['index'][21]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'fcv' : [family_data['fcv']['index'][22]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'fcv' : [family_data['fcv']['index'][23]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'fcv' : [family_data['fcv']['index'][24]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'fcv' : [family_data['fcv']['index'][25]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'fcv' : [family_data['fcv']['index'][26]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'fcv' : [family_data['fcv']['index'][27]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'fcv' : [family_data['fcv']['index'][28]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'fcv' : [family_data['fcv']['index'][29]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'fcv' : [family_data['fcv']['index'][30]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'fcv' : [family_data['fcv']['index'][31]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'fcv' : [family_data['fcv']['index'][32]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'fcv' : [family_data['fcv']['index'][33]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'fcv' : [family_data['fcv']['index'][34]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'fcv' : [family_data['fcv']['index'][35]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'fcv' : [family_data['fcv']['index'][36]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'fcv' : [family_data['fcv']['index'][37]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'fcv' : [family_data['fcv']['index'][38]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'fcv' : [family_data['fcv']['index'][39]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'fcv' : [family_data['fcv']['index'][40]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'fcv' : [family_data['fcv']['index'][41]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'fcv' : [family_data['fcv']['index'][42]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'fcv' : [family_data['fcv']['index'][43]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'fcv' : [family_data['fcv']['index'][44]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'fcv' : [family_data['fcv']['index'][45]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'fcv' : [family_data['fcv']['index'][46]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'fcv' : [family_data['fcv']['index'][47]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'fcv' : [family_data['fcv']['index'][48]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'fcv' : [family_data['fcv']['index'][49]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'fcv' : [family_data['fcv']['index'][50]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'fcv' : [family_data['fcv']['index'][51]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'fcv' : [family_data['fcv']['index'][52]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'fcv' : [family_data['fcv']['index'][53]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'fcv' : [family_data['fcv']['index'][54]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'fcv' : [family_data['fcv']['index'][55]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'fcv' : [family_data['fcv']['index'][56]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'fcv' : [family_data['fcv']['index'][57]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'fcv' : [family_data['fcv']['index'][58]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'fcv' : [family_data['fcv']['index'][59]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'fcv' : [family_data['fcv']['index'][60]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'fcv' : [family_data['fcv']['index'][61]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'fcv' : [family_data['fcv']['index'][62]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'fcv' : [family_data['fcv']['index'][63]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'fcv' : [family_data['fcv']['index'][64]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'fcv' : [family_data['fcv']['index'][65]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'fcv' : [family_data['fcv']['index'][66]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'fcv' : [family_data['fcv']['index'][67]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'fcv' : [family_data['fcv']['index'][68]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'fcv' : [family_data['fcv']['index'][69]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'fcv' : [family_data['fcv']['index'][70]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'fcv' : [family_data['fcv']['index'][71]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'fcv' : [family_data['fcv']['index'][72]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'fcv' : [family_data['fcv']['index'][73]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'fcv' : [family_data['fcv']['index'][74]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'fcv' : [family_data['fcv']['index'][75]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'fcv' : [family_data['fcv']['index'][76]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'fcv' : [family_data['fcv']['index'][77]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'fcv' : [family_data['fcv']['index'][78]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'fcv' : [family_data['fcv']['index'][79]]},
        }
        return _dict


    if element == 'fc':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M2') : { 'fc' : [family_data['fc']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C2') : { 'fc' : [family_data['fc']['index'][1]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'fc' : [family_data['fc']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02M1') : { 'fc' : [family_data['fc']['index'][3]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'fc' : [family_data['fc']['index'][4]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'fc' : [family_data['fc']['index'][5]]},
            join_name(system, subsystem, element.upper(), '02C3') : { 'fc' : [family_data['fc']['index'][6]]},
            join_name(system, subsystem, element.upper(), '03M1') : { 'fc' : [family_data['fc']['index'][7]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'fc' : [family_data['fc']['index'][8]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'fc' : [family_data['fc']['index'][9]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'fc' : [family_data['fc']['index'][10]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'fc' : [family_data['fc']['index'][11]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'fc' : [family_data['fc']['index'][12]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'fc' : [family_data['fc']['index'][13]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'fc' : [family_data['fc']['index'][14]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'fc' : [family_data['fc']['index'][15]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'fc' : [family_data['fc']['index'][16]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'fc' : [family_data['fc']['index'][17]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'fc' : [family_data['fc']['index'][18]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'fc' : [family_data['fc']['index'][19]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'fc' : [family_data['fc']['index'][20]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'fc' : [family_data['fc']['index'][21]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'fc' : [family_data['fc']['index'][22]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'fc' : [family_data['fc']['index'][23]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'fc' : [family_data['fc']['index'][24]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'fc' : [family_data['fc']['index'][25]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'fc' : [family_data['fc']['index'][26]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'fc' : [family_data['fc']['index'][27]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'fc' : [family_data['fc']['index'][28]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'fc' : [family_data['fc']['index'][29]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'fc' : [family_data['fc']['index'][30]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'fc' : [family_data['fc']['index'][31]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'fc' : [family_data['fc']['index'][32]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'fc' : [family_data['fc']['index'][33]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'fc' : [family_data['fc']['index'][34]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'fc' : [family_data['fc']['index'][35]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'fc' : [family_data['fc']['index'][36]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'fc' : [family_data['fc']['index'][37]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'fc' : [family_data['fc']['index'][38]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'fc' : [family_data['fc']['index'][39]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'fc' : [family_data['fc']['index'][40]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'fc' : [family_data['fc']['index'][41]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'fc' : [family_data['fc']['index'][42]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'fc' : [family_data['fc']['index'][43]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'fc' : [family_data['fc']['index'][44]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'fc' : [family_data['fc']['index'][45]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'fc' : [family_data['fc']['index'][46]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'fc' : [family_data['fc']['index'][47]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'fc' : [family_data['fc']['index'][48]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'fc' : [family_data['fc']['index'][49]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'fc' : [family_data['fc']['index'][50]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'fc' : [family_data['fc']['index'][51]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'fc' : [family_data['fc']['index'][52]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'fc' : [family_data['fc']['index'][53]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'fc' : [family_data['fc']['index'][54]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'fc' : [family_data['fc']['index'][55]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'fc' : [family_data['fc']['index'][56]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'fc' : [family_data['fc']['index'][57]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'fc' : [family_data['fc']['index'][58]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'fc' : [family_data['fc']['index'][59]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'fc' : [family_data['fc']['index'][60]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'fc' : [family_data['fc']['index'][61]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'fc' : [family_data['fc']['index'][62]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'fc' : [family_data['fc']['index'][63]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'fc' : [family_data['fc']['index'][64]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'fc' : [family_data['fc']['index'][65]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'fc' : [family_data['fc']['index'][66]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'fc' : [family_data['fc']['index'][67]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'fc' : [family_data['fc']['index'][68]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'fc' : [family_data['fc']['index'][69]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'fc' : [family_data['fc']['index'][70]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'fc' : [family_data['fc']['index'][71]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'fc' : [family_data['fc']['index'][72]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'fc' : [family_data['fc']['index'][73]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'fc' : [family_data['fc']['index'][74]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'fc' : [family_data['fc']['index'][75]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'fc' : [family_data['fc']['index'][76]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'fc' : [family_data['fc']['index'][77]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'fc' : [family_data['fc']['index'][78]]},
            join_name(system, subsystem, element.upper(), '01M1') : { 'fc' : [family_data['fc']['index'][79]]},
        }
        return _dict

    if element == 'qfa':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M1') : { 'qfa' : [family_data['qfa']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01M2') : { 'qfa' : [family_data['qfa']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'qfa' : [family_data['qfa']['index'][2]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'qfa' : [family_data['qfa']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'qfa' : [family_data['qfa']['index'][4]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'qfa' : [family_data['qfa']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'qfa' : [family_data['qfa']['index'][6]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'qfa' : [family_data['qfa']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'qfa' : [family_data['qfa']['index'][8]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'qfa' : [family_data['qfa']['index'][9]]},
        }
        return _dict

    if element == 'qda':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M1') : { 'qda' : [family_data['qda']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01M2') : { 'qda' : [family_data['qda']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'qda' : [family_data['qda']['index'][2]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'qda' : [family_data['qda']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'qda' : [family_data['qda']['index'][4]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'qda' : [family_data['qda']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'qda' : [family_data['qda']['index'][6]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'qda' : [family_data['qda']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'qda' : [family_data['qda']['index'][8]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'qda' : [family_data['qda']['index'][9]]},
        }
        return _dict

    if element == 'qdb2':
        _dict = {
            join_name(system, subsystem, element.upper(), '02M1') : { 'qdb2' : [family_data['qdb2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'qdb2' : [family_data['qdb2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'qdb2' : [family_data['qdb2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'qdb2' : [family_data['qdb2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'qdb2' : [family_data['qdb2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'qdb2' : [family_data['qdb2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'qdb2' : [family_data['qdb2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'qdb2' : [family_data['qdb2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'qdb2' : [family_data['qdb2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'qdb2' : [family_data['qdb2']['index'][9]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'qdb2' : [family_data['qdb2']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'qdb2' : [family_data['qdb2']['index'][11]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'qdb2' : [family_data['qdb2']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'qdb2' : [family_data['qdb2']['index'][13]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'qdb2' : [family_data['qdb2']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'qdb2' : [family_data['qdb2']['index'][15]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'qdb2' : [family_data['qdb2']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'qdb2' : [family_data['qdb2']['index'][17]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'qdb2' : [family_data['qdb2']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'qdb2' : [family_data['qdb2']['index'][19]]},
        }
        return _dict

    if element == 'qfb':
        _dict = {
            join_name(system, subsystem, element.upper(), '02M1') : { 'qfb' : [family_data['qfb']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'qfb' : [family_data['qfb']['index'][1]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'qfb' : [family_data['qfb']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'qfb' : [family_data['qfb']['index'][3]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'qfb' : [family_data['qfb']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'qfb' : [family_data['qfb']['index'][5]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'qfb' : [family_data['qfb']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'qfb' : [family_data['qfb']['index'][7]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'qfb' : [family_data['qfb']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'qfb' : [family_data['qfb']['index'][9]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'qfb' : [family_data['qfb']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'qfb' : [family_data['qfb']['index'][11]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'qfb' : [family_data['qfb']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'qfb' : [family_data['qfb']['index'][13]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'qfb' : [family_data['qfb']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'qfb' : [family_data['qfb']['index'][15]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'qfb' : [family_data['qfb']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'qfb' : [family_data['qfb']['index'][17]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'qfb' : [family_data['qfb']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'qfb' : [family_data['qfb']['index'][19]]},
        }
        return _dict

    if element == 'qdb1':
        _dict = {
            join_name(system, subsystem, element.upper(), '02M1') : { 'qdb1' : [family_data['qdb1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'qdb1' : [family_data['qdb1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'qdb1' : [family_data['qdb1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'qdb1' : [family_data['qdb1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'qdb1' : [family_data['qdb1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'qdb1' : [family_data['qdb1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'qdb1' : [family_data['qdb1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'qdb1' : [family_data['qdb1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'qdb1' : [family_data['qdb1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'qdb1' : [family_data['qdb1']['index'][9]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'qdb1' : [family_data['qdb1']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'qdb1' : [family_data['qdb1']['index'][11]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'qdb1' : [family_data['qdb1']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'qdb1' : [family_data['qdb1']['index'][13]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'qdb1' : [family_data['qdb1']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'qdb1' : [family_data['qdb1']['index'][15]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'qdb1' : [family_data['qdb1']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'qdb1' : [family_data['qdb1']['index'][17]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'qdb1' : [family_data['qdb1']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'qdb1' : [family_data['qdb1']['index'][19]]},
        }
        return _dict

    if element == 'qdp2':
        _dict = {
            join_name(system, subsystem, element.upper(), '03M1') : { 'qdp2' : [family_data['qdp2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'qdp2' : [family_data['qdp2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'qdp2' : [family_data['qdp2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'qdp2' : [family_data['qdp2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'qdp2' : [family_data['qdp2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'qdp2' : [family_data['qdp2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'qdp2' : [family_data['qdp2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'qdp2' : [family_data['qdp2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'qdp2' : [family_data['qdp2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'qdp2' : [family_data['qdp2']['index'][9]]},
        }
        return _dict

    if element == 'qfp':
        _dict = {
            join_name(system, subsystem, element.upper(), '03M1') : { 'qfp' : [family_data['qfp']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'qfp' : [family_data['qfp']['index'][1]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'qfp' : [family_data['qfp']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'qfp' : [family_data['qfp']['index'][3]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'qfp' : [family_data['qfp']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'qfp' : [family_data['qfp']['index'][5]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'qfp' : [family_data['qfp']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'qfp' : [family_data['qfp']['index'][7]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'qfp' : [family_data['qfp']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'qfp' : [family_data['qfp']['index'][9]]},
        }
        return _dict

    if element == 'qdp1':
        _dict = {
            join_name(system, subsystem, element.upper(), '03M1') : { 'qdp1' : [family_data['qdp1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'qdp1' : [family_data['qdp1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'qdp1' : [family_data['qdp1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'qdp1' : [family_data['qdp1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'qdp1' : [family_data['qdp1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'qdp1' : [family_data['qdp1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'qdp1' : [family_data['qdp1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'qdp1' : [family_data['qdp1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'qdp1' : [family_data['qdp1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'qdp1' : [family_data['qdp1']['index'][9]]},
        }
        return _dict

    if element == 'q1':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C1') : { 'q1' : [family_data['q1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C4') : { 'q1' : [family_data['q1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'q1' : [family_data['q1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02C4') : { 'q1' : [family_data['q1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'q1' : [family_data['q1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'q1' : [family_data['q1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'q1' : [family_data['q1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'q1' : [family_data['q1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'q1' : [family_data['q1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'q1' : [family_data['q1']['index'][9]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'q1' : [family_data['q1']['index'][10]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'q1' : [family_data['q1']['index'][11]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'q1' : [family_data['q1']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'q1' : [family_data['q1']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'q1' : [family_data['q1']['index'][14]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'q1' : [family_data['q1']['index'][15]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'q1' : [family_data['q1']['index'][16]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'q1' : [family_data['q1']['index'][17]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'q1' : [family_data['q1']['index'][18]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'q1' : [family_data['q1']['index'][19]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'q1' : [family_data['q1']['index'][20]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'q1' : [family_data['q1']['index'][21]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'q1' : [family_data['q1']['index'][22]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'q1' : [family_data['q1']['index'][23]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'q1' : [family_data['q1']['index'][24]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'q1' : [family_data['q1']['index'][25]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'q1' : [family_data['q1']['index'][26]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'q1' : [family_data['q1']['index'][27]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'q1' : [family_data['q1']['index'][28]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'q1' : [family_data['q1']['index'][29]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'q1' : [family_data['q1']['index'][30]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'q1' : [family_data['q1']['index'][31]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'q1' : [family_data['q1']['index'][32]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'q1' : [family_data['q1']['index'][33]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'q1' : [family_data['q1']['index'][34]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'q1' : [family_data['q1']['index'][35]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'q1' : [family_data['q1']['index'][36]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'q1' : [family_data['q1']['index'][37]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'q1' : [family_data['q1']['index'][38]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'q1' : [family_data['q1']['index'][39]]},
        }
        return _dict

    if element == 'q2':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C1') : { 'q2' : [family_data['q2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C4') : { 'q2' : [family_data['q2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'q2' : [family_data['q2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02C4') : { 'q2' : [family_data['q2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'q2' : [family_data['q2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'q2' : [family_data['q2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'q2' : [family_data['q2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'q2' : [family_data['q2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'q2' : [family_data['q2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'q2' : [family_data['q2']['index'][9]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'q2' : [family_data['q2']['index'][10]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'q2' : [family_data['q2']['index'][11]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'q2' : [family_data['q2']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'q2' : [family_data['q2']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'q2' : [family_data['q2']['index'][14]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'q2' : [family_data['q2']['index'][15]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'q2' : [family_data['q2']['index'][16]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'q2' : [family_data['q2']['index'][17]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'q2' : [family_data['q2']['index'][18]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'q2' : [family_data['q2']['index'][19]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'q2' : [family_data['q2']['index'][20]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'q2' : [family_data['q2']['index'][21]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'q2' : [family_data['q2']['index'][22]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'q2' : [family_data['q2']['index'][23]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'q2' : [family_data['q2']['index'][24]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'q2' : [family_data['q2']['index'][25]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'q2' : [family_data['q2']['index'][26]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'q2' : [family_data['q2']['index'][27]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'q2' : [family_data['q2']['index'][28]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'q2' : [family_data['q2']['index'][29]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'q2' : [family_data['q2']['index'][30]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'q2' : [family_data['q2']['index'][31]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'q2' : [family_data['q2']['index'][32]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'q2' : [family_data['q2']['index'][33]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'q2' : [family_data['q2']['index'][34]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'q2' : [family_data['q2']['index'][35]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'q2' : [family_data['q2']['index'][36]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'q2' : [family_data['q2']['index'][37]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'q2' : [family_data['q2']['index'][38]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'q2' : [family_data['q2']['index'][39]]},
        }
        return _dict

    if element == 'q3':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C2') : { 'q3' : [family_data['q3']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'q3' : [family_data['q3']['index'][1]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'q3' : [family_data['q3']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02C3') : { 'q3' : [family_data['q3']['index'][3]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'q3' : [family_data['q3']['index'][4]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'q3' : [family_data['q3']['index'][5]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'q3' : [family_data['q3']['index'][6]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'q3' : [family_data['q3']['index'][7]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'q3' : [family_data['q3']['index'][8]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'q3' : [family_data['q3']['index'][9]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'q3' : [family_data['q3']['index'][10]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'q3' : [family_data['q3']['index'][11]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'q3' : [family_data['q3']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'q3' : [family_data['q3']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'q3' : [family_data['q3']['index'][14]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'q3' : [family_data['q3']['index'][15]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'q3' : [family_data['q3']['index'][16]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'q3' : [family_data['q3']['index'][17]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'q3' : [family_data['q3']['index'][18]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'q3' : [family_data['q3']['index'][19]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'q3' : [family_data['q3']['index'][20]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'q3' : [family_data['q3']['index'][21]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'q3' : [family_data['q3']['index'][22]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'q3' : [family_data['q3']['index'][23]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'q3' : [family_data['q3']['index'][24]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'q3' : [family_data['q3']['index'][25]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'q3' : [family_data['q3']['index'][26]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'q3' : [family_data['q3']['index'][27]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'q3' : [family_data['q3']['index'][28]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'q3' : [family_data['q3']['index'][29]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'q3' : [family_data['q3']['index'][30]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'q3' : [family_data['q3']['index'][31]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'q3' : [family_data['q3']['index'][32]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'q3' : [family_data['q3']['index'][33]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'q3' : [family_data['q3']['index'][34]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'q3' : [family_data['q3']['index'][35]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'q3' : [family_data['q3']['index'][36]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'q3' : [family_data['q3']['index'][37]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'q3' : [family_data['q3']['index'][38]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'q3' : [family_data['q3']['index'][39]]},
        }
        return _dict

    if element == 'q4':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C2') : { 'q4' : [family_data['q4']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01C3') : { 'q4' : [family_data['q4']['index'][1]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'q4' : [family_data['q4']['index'][2]]},
            join_name(system, subsystem, element.upper(), '02C3') : { 'q4' : [family_data['q4']['index'][3]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'q4' : [family_data['q4']['index'][4]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'q4' : [family_data['q4']['index'][5]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'q4' : [family_data['q4']['index'][6]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'q4' : [family_data['q4']['index'][7]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'q4' : [family_data['q4']['index'][8]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'q4' : [family_data['q4']['index'][9]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'q4' : [family_data['q4']['index'][10]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'q4' : [family_data['q4']['index'][11]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'q4' : [family_data['q4']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'q4' : [family_data['q4']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'q4' : [family_data['q4']['index'][14]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'q4' : [family_data['q4']['index'][15]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'q4' : [family_data['q4']['index'][16]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'q4' : [family_data['q4']['index'][17]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'q4' : [family_data['q4']['index'][18]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'q4' : [family_data['q4']['index'][19]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'q4' : [family_data['q4']['index'][20]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'q4' : [family_data['q4']['index'][21]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'q4' : [family_data['q4']['index'][22]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'q4' : [family_data['q4']['index'][23]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'q4' : [family_data['q4']['index'][24]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'q4' : [family_data['q4']['index'][25]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'q4' : [family_data['q4']['index'][26]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'q4' : [family_data['q4']['index'][27]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'q4' : [family_data['q4']['index'][28]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'q4' : [family_data['q4']['index'][29]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'q4' : [family_data['q4']['index'][30]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'q4' : [family_data['q4']['index'][31]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'q4' : [family_data['q4']['index'][32]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'q4' : [family_data['q4']['index'][33]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'q4' : [family_data['q4']['index'][34]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'q4' : [family_data['q4']['index'][35]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'q4' : [family_data['q4']['index'][36]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'q4' : [family_data['q4']['index'][37]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'q4' : [family_data['q4']['index'][38]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'q4' : [family_data['q4']['index'][39]]},
        }
        return _dict

    if element == 'sda0':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M1') : { 'sda0' : [family_data['sda0']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01M2') : { 'sda0' : [family_data['sda0']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'sda0' : [family_data['sda0']['index'][2]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'sda0' : [family_data['sda0']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'sda0' : [family_data['sda0']['index'][4]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'sda0' : [family_data['sda0']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'sda0' : [family_data['sda0']['index'][6]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'sda0' : [family_data['sda0']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'sda0' : [family_data['sda0']['index'][8]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'sda0' : [family_data['sda0']['index'][9]]},
        }
        return _dict

    if element == 'sdb0':
        _dict = {
            join_name(system, subsystem, element.upper(), '02M1') : { 'sdb0' : [family_data['sdb0']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'sdb0' : [family_data['sdb0']['index'][1]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'sdb0' : [family_data['sdb0']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'sdb0' : [family_data['sdb0']['index'][3]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'sdb0' : [family_data['sdb0']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'sdb0' : [family_data['sdb0']['index'][5]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'sdb0' : [family_data['sdb0']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'sdb0' : [family_data['sdb0']['index'][7]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'sdb0' : [family_data['sdb0']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'sdb0' : [family_data['sdb0']['index'][9]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'sdb0' : [family_data['sdb0']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'sdb0' : [family_data['sdb0']['index'][11]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'sdb0' : [family_data['sdb0']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'sdb0' : [family_data['sdb0']['index'][13]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'sdb0' : [family_data['sdb0']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'sdb0' : [family_data['sdb0']['index'][15]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'sdb0' : [family_data['sdb0']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'sdb0' : [family_data['sdb0']['index'][17]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'sdb0' : [family_data['sdb0']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'sdb0' : [family_data['sdb0']['index'][19]]},
        }
        return _dict

    if element == 'sdp0':
        _dict = {
            join_name(system, subsystem, element.upper(), '03M1') : { 'sdp0' : [family_data['sdp0']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'sdp0' : [family_data['sdp0']['index'][1]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'sdp0' : [family_data['sdp0']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'sdp0' : [family_data['sdp0']['index'][3]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'sdp0' : [family_data['sdp0']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'sdp0' : [family_data['sdp0']['index'][5]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'sdp0' : [family_data['sdp0']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'sdp0' : [family_data['sdp0']['index'][7]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'sdp0' : [family_data['sdp0']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'sdp0' : [family_data['sdp0']['index'][9]]},
        }
        return _dict

    if element == 'sda1':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C1') : { 'sda1' : [family_data['sda1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'sda1' : [family_data['sda1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'sda1' : [family_data['sda1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'sda1' : [family_data['sda1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'sda1' : [family_data['sda1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'sda1' : [family_data['sda1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'sda1' : [family_data['sda1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'sda1' : [family_data['sda1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'sda1' : [family_data['sda1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'sda1' : [family_data['sda1']['index'][9]]},
        }
        return _dict

    if element == 'sdb1':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C4') : { 'sdb1' : [family_data['sdb1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'sdb1' : [family_data['sdb1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'sdb1' : [family_data['sdb1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'sdb1' : [family_data['sdb1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'sdb1' : [family_data['sdb1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'sdb1' : [family_data['sdb1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'sdb1' : [family_data['sdb1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'sdb1' : [family_data['sdb1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'sdb1' : [family_data['sdb1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'sdb1' : [family_data['sdb1']['index'][9]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'sdb1' : [family_data['sdb1']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'sdb1' : [family_data['sdb1']['index'][11]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'sdb1' : [family_data['sdb1']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'sdb1' : [family_data['sdb1']['index'][13]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'sdb1' : [family_data['sdb1']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'sdb1' : [family_data['sdb1']['index'][15]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'sdb1' : [family_data['sdb1']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'sdb1' : [family_data['sdb1']['index'][17]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'sdb1' : [family_data['sdb1']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'sdb1' : [family_data['sdb1']['index'][19]]},
        }
        return _dict

    if element == 'sdp1':
        _dict = {
            join_name(system, subsystem, element.upper(), '02C4') : { 'sdp1' : [family_data['sdp1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'sdp1' : [family_data['sdp1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'sdp1' : [family_data['sdp1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'sdp1' : [family_data['sdp1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'sdp1' : [family_data['sdp1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'sdp1' : [family_data['sdp1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'sdp1' : [family_data['sdp1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'sdp1' : [family_data['sdp1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'sdp1' : [family_data['sdp1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'sdp1' : [family_data['sdp1']['index'][9]]},
        }
        return _dict

    if element == 'sda2':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C1') : { 'sda2' : [family_data['sda2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'sda2' : [family_data['sda2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'sda2' : [family_data['sda2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'sda2' : [family_data['sda2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'sda2' : [family_data['sda2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'sda2' : [family_data['sda2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'sda2' : [family_data['sda2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'sda2' : [family_data['sda2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'sda2' : [family_data['sda2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'sda2' : [family_data['sda2']['index'][9]]},
        }
        return _dict

    if element == 'sdb2':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C4') : { 'sdb2' : [family_data['sdb2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'sdb2' : [family_data['sdb2']['index'][10]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'sdb2' : [family_data['sdb2']['index'][11]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'sdb2' : [family_data['sdb2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'sdb2' : [family_data['sdb2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'sdb2' : [family_data['sdb2']['index'][12]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'sdb2' : [family_data['sdb2']['index'][13]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'sdb2' : [family_data['sdb2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'sdb2' : [family_data['sdb2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'sdb2' : [family_data['sdb2']['index'][14]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'sdb2' : [family_data['sdb2']['index'][15]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'sdb2' : [family_data['sdb2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'sdb2' : [family_data['sdb2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'sdb2' : [family_data['sdb2']['index'][16]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'sdb2' : [family_data['sdb2']['index'][17]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'sdb2' : [family_data['sdb2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'sdb2' : [family_data['sdb2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'sdb2' : [family_data['sdb2']['index'][18]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'sdb2' : [family_data['sdb2']['index'][19]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'sdb2' : [family_data['sdb2']['index'][9]]},
        }
        return _dict

    if element == 'sdp2':
        _dict = {
            join_name(system, subsystem, element.upper(), '02C4') : { 'sdp2' : [family_data['sdp2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'sdp2' : [family_data['sdp2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'sdp2' : [family_data['sdp2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'sdp2' : [family_data['sdp2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'sdp2' : [family_data['sdp2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'sdp2' : [family_data['sdp2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'sdp2' : [family_data['sdp2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'sdp2' : [family_data['sdp2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'sdp2' : [family_data['sdp2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'sdp2' : [family_data['sdp2']['index'][9]]},
        }
        return _dict

    if element == 'sda3':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C2') : { 'sda3' : [family_data['sda3']['index'][0]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'sda3' : [family_data['sda3']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'sda3' : [family_data['sda3']['index'][2]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'sda3' : [family_data['sda3']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'sda3' : [family_data['sda3']['index'][4]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'sda3' : [family_data['sda3']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'sda3' : [family_data['sda3']['index'][6]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'sda3' : [family_data['sda3']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'sda3' : [family_data['sda3']['index'][8]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'sda3' : [family_data['sda3']['index'][9]]},
        }
        return _dict

    if element == 'sdb3':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C3') : { 'sdb3' : [family_data['sdb3']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'sdb3' : [family_data['sdb3']['index'][1]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'sdb3' : [family_data['sdb3']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'sdb3' : [family_data['sdb3']['index'][3]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'sdb3' : [family_data['sdb3']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'sdb3' : [family_data['sdb3']['index'][5]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'sdb3' : [family_data['sdb3']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'sdb3' : [family_data['sdb3']['index'][7]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'sdb3' : [family_data['sdb3']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'sdb3' : [family_data['sdb3']['index'][9]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'sdb3' : [family_data['sdb3']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'sdb3' : [family_data['sdb3']['index'][11]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'sdb3' : [family_data['sdb3']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'sdb3' : [family_data['sdb3']['index'][13]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'sdb3' : [family_data['sdb3']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'sdb3' : [family_data['sdb3']['index'][15]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'sdb3' : [family_data['sdb3']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'sdb3' : [family_data['sdb3']['index'][17]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'sdb3' : [family_data['sdb3']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'sdb3' : [family_data['sdb3']['index'][19]]},
        }
        return _dict

    if element == 'sdp3':
        _dict = {
            join_name(system, subsystem, element.upper(), '02C3') : { 'sdp3' : [family_data['sdp3']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'sdp3' : [family_data['sdp3']['index'][1]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'sdp3' : [family_data['sdp3']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'sdp3' : [family_data['sdp3']['index'][3]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'sdp3' : [family_data['sdp3']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'sdp3' : [family_data['sdp3']['index'][5]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'sdp3' : [family_data['sdp3']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'sdp3' : [family_data['sdp3']['index'][7]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'sdp3' : [family_data['sdp3']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'sdp3' : [family_data['sdp3']['index'][9]]},
        }
        return _dict

    if element == 'sfa0':
        _dict = {
            join_name(system, subsystem, element.upper(), '01M1') : { 'sfa0' : [family_data['sfa0']['index'][0]]},
            join_name(system, subsystem, element.upper(), '01M2') : { 'sfa0' : [family_data['sfa0']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05M1') : { 'sfa0' : [family_data['sfa0']['index'][2]]},
            join_name(system, subsystem, element.upper(), '05M2') : { 'sfa0' : [family_data['sfa0']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09M1') : { 'sfa0' : [family_data['sfa0']['index'][4]]},
            join_name(system, subsystem, element.upper(), '09M2') : { 'sfa0' : [family_data['sfa0']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13M1') : { 'sfa0' : [family_data['sfa0']['index'][6]]},
            join_name(system, subsystem, element.upper(), '13M2') : { 'sfa0' : [family_data['sfa0']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17M1') : { 'sfa0' : [family_data['sfa0']['index'][8]]},
            join_name(system, subsystem, element.upper(), '17M2') : { 'sfa0' : [family_data['sfa0']['index'][9]]},
        }
        return _dict

    if element == 'sfb0':
        _dict = {
            join_name(system, subsystem, element.upper(), '02M1') : { 'sfb0' : [family_data['sfb0']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02M2') : { 'sfb0' : [family_data['sfb0']['index'][1]]},
            join_name(system, subsystem, element.upper(), '04M1') : { 'sfb0' : [family_data['sfb0']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04M2') : { 'sfb0' : [family_data['sfb0']['index'][3]]},
            join_name(system, subsystem, element.upper(), '06M1') : { 'sfb0' : [family_data['sfb0']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06M2') : { 'sfb0' : [family_data['sfb0']['index'][5]]},
            join_name(system, subsystem, element.upper(), '08M1') : { 'sfb0' : [family_data['sfb0']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08M2') : { 'sfb0' : [family_data['sfb0']['index'][7]]},
            join_name(system, subsystem, element.upper(), '10M1') : { 'sfb0' : [family_data['sfb0']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10M2') : { 'sfb0' : [family_data['sfb0']['index'][9]]},
            join_name(system, subsystem, element.upper(), '12M1') : { 'sfb0' : [family_data['sfb0']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12M2') : { 'sfb0' : [family_data['sfb0']['index'][11]]},
            join_name(system, subsystem, element.upper(), '14M1') : { 'sfb0' : [family_data['sfb0']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14M2') : { 'sfb0' : [family_data['sfb0']['index'][13]]},
            join_name(system, subsystem, element.upper(), '16M1') : { 'sfb0' : [family_data['sfb0']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16M2') : { 'sfb0' : [family_data['sfb0']['index'][15]]},
            join_name(system, subsystem, element.upper(), '18M1') : { 'sfb0' : [family_data['sfb0']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18M2') : { 'sfb0' : [family_data['sfb0']['index'][17]]},
            join_name(system, subsystem, element.upper(), '20M1') : { 'sfb0' : [family_data['sfb0']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20M2') : { 'sfb0' : [family_data['sfb0']['index'][19]]},
        }
        return _dict

    if element == 'sfp0':
        _dict = {
            join_name(system, subsystem, element.upper(), '03M1') : { 'sfp0' : [family_data['sfp0']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03M2') : { 'sfp0' : [family_data['sfp0']['index'][1]]},
            join_name(system, subsystem, element.upper(), '07M1') : { 'sfp0' : [family_data['sfp0']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07M2') : { 'sfp0' : [family_data['sfp0']['index'][3]]},
            join_name(system, subsystem, element.upper(), '11M1') : { 'sfp0' : [family_data['sfp0']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11M2') : { 'sfp0' : [family_data['sfp0']['index'][5]]},
            join_name(system, subsystem, element.upper(), '15M1') : { 'sfp0' : [family_data['sfp0']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15M2') : { 'sfp0' : [family_data['sfp0']['index'][7]]},
            join_name(system, subsystem, element.upper(), '19M1') : { 'sfp0' : [family_data['sfp0']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19M2') : { 'sfp0' : [family_data['sfp0']['index'][9]]},
        }
        return _dict

    if element == 'sfa1':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C1') : { 'sfa1' : [family_data['sfa1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '04C4') : { 'sfa1' : [family_data['sfa1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05C1') : { 'sfa1' : [family_data['sfa1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '08C4') : { 'sfa1' : [family_data['sfa1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09C1') : { 'sfa1' : [family_data['sfa1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '12C4') : { 'sfa1' : [family_data['sfa1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13C1') : { 'sfa1' : [family_data['sfa1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '16C4') : { 'sfa1' : [family_data['sfa1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17C1') : { 'sfa1' : [family_data['sfa1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '20C4') : { 'sfa1' : [family_data['sfa1']['index'][9]]},
        }
        return _dict

    if element == 'sfb1':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C4') : { 'sfb1' : [family_data['sfb1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02C1') : { 'sfb1' : [family_data['sfb1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '03C4') : { 'sfb1' : [family_data['sfb1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04C1') : { 'sfb1' : [family_data['sfb1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '05C4') : { 'sfb1' : [family_data['sfb1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06C1') : { 'sfb1' : [family_data['sfb1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '07C4') : { 'sfb1' : [family_data['sfb1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08C1') : { 'sfb1' : [family_data['sfb1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '09C4') : { 'sfb1' : [family_data['sfb1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10C1') : { 'sfb1' : [family_data['sfb1']['index'][9]]},
            join_name(system, subsystem, element.upper(), '11C4') : { 'sfb1' : [family_data['sfb1']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12C1') : { 'sfb1' : [family_data['sfb1']['index'][11]]},
            join_name(system, subsystem, element.upper(), '13C4') : { 'sfb1' : [family_data['sfb1']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14C1') : { 'sfb1' : [family_data['sfb1']['index'][13]]},
            join_name(system, subsystem, element.upper(), '15C4') : { 'sfb1' : [family_data['sfb1']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16C1') : { 'sfb1' : [family_data['sfb1']['index'][15]]},
            join_name(system, subsystem, element.upper(), '17C4') : { 'sfb1' : [family_data['sfb1']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18C1') : { 'sfb1' : [family_data['sfb1']['index'][17]]},
            join_name(system, subsystem, element.upper(), '19C4') : { 'sfb1' : [family_data['sfb1']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20C1') : { 'sfb1' : [family_data['sfb1']['index'][19]]},
        }
        return _dict

    if element == 'sfp1':
        _dict = {
            join_name(system, subsystem, element.upper(), '02C4') : { 'sfp1' : [family_data['sfp1']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03C1') : { 'sfp1' : [family_data['sfp1']['index'][1]]},
            join_name(system, subsystem, element.upper(), '06C4') : { 'sfp1' : [family_data['sfp1']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07C1') : { 'sfp1' : [family_data['sfp1']['index'][3]]},
            join_name(system, subsystem, element.upper(), '10C4') : { 'sfp1' : [family_data['sfp1']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11C1') : { 'sfp1' : [family_data['sfp1']['index'][5]]},
            join_name(system, subsystem, element.upper(), '14C4') : { 'sfp1' : [family_data['sfp1']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15C1') : { 'sfp1' : [family_data['sfp1']['index'][7]]},
            join_name(system, subsystem, element.upper(), '18C4') : { 'sfp1' : [family_data['sfp1']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19C1') : { 'sfp1' : [family_data['sfp1']['index'][9]]},
        }
        return _dict

    if element == 'sfa2':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C2') : { 'sfa2' : [family_data['sfa2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '04C3') : { 'sfa2' : [family_data['sfa2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '05C2') : { 'sfa2' : [family_data['sfa2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '08C3') : { 'sfa2' : [family_data['sfa2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '09C2') : { 'sfa2' : [family_data['sfa2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '12C3') : { 'sfa2' : [family_data['sfa2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '13C2') : { 'sfa2' : [family_data['sfa2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '16C3') : { 'sfa2' : [family_data['sfa2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '17C2') : { 'sfa2' : [family_data['sfa2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '20C3') : { 'sfa2' : [family_data['sfa2']['index'][9]]},
        }
        return _dict

    if element == 'sfb2':
        _dict = {
            join_name(system, subsystem, element.upper(), '01C3') : { 'sfb2' : [family_data['sfb2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '02C2') : { 'sfb2' : [family_data['sfb2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '03C3') : { 'sfb2' : [family_data['sfb2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '04C2') : { 'sfb2' : [family_data['sfb2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '05C3') : { 'sfb2' : [family_data['sfb2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '06C2') : { 'sfb2' : [family_data['sfb2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '07C3') : { 'sfb2' : [family_data['sfb2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '08C2') : { 'sfb2' : [family_data['sfb2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '09C3') : { 'sfb2' : [family_data['sfb2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '10C2') : { 'sfb2' : [family_data['sfb2']['index'][9]]},
            join_name(system, subsystem, element.upper(), '11C3') : { 'sfb2' : [family_data['sfb2']['index'][10]]},
            join_name(system, subsystem, element.upper(), '12C2') : { 'sfb2' : [family_data['sfb2']['index'][11]]},
            join_name(system, subsystem, element.upper(), '13C3') : { 'sfb2' : [family_data['sfb2']['index'][12]]},
            join_name(system, subsystem, element.upper(), '14C2') : { 'sfb2' : [family_data['sfb2']['index'][13]]},
            join_name(system, subsystem, element.upper(), '15C3') : { 'sfb2' : [family_data['sfb2']['index'][14]]},
            join_name(system, subsystem, element.upper(), '16C2') : { 'sfb2' : [family_data['sfb2']['index'][15]]},
            join_name(system, subsystem, element.upper(), '17C3') : { 'sfb2' : [family_data['sfb2']['index'][16]]},
            join_name(system, subsystem, element.upper(), '18C2') : { 'sfb2' : [family_data['sfb2']['index'][17]]},
            join_name(system, subsystem, element.upper(), '19C3') : { 'sfb2' : [family_data['sfb2']['index'][18]]},
            join_name(system, subsystem, element.upper(), '20C2') : { 'sfb2' : [family_data['sfb2']['index'][19]]},
        }
        return _dict

    if element == 'sfp2':
        _dict = {
            join_name(system, subsystem, element.upper(), '02C3') : { 'sfp2' : [family_data['sfp2']['index'][0]]},
            join_name(system, subsystem, element.upper(), '03C2') : { 'sfp2' : [family_data['sfp2']['index'][1]]},
            join_name(system, subsystem, element.upper(), '06C3') : { 'sfp2' : [family_data['sfp2']['index'][2]]},
            join_name(system, subsystem, element.upper(), '07C2') : { 'sfp2' : [family_data['sfp2']['index'][3]]},
            join_name(system, subsystem, element.upper(), '10C3') : { 'sfp2' : [family_data['sfp2']['index'][4]]},
            join_name(system, subsystem, element.upper(), '11C2') : { 'sfp2' : [family_data['sfp2']['index'][5]]},
            join_name(system, subsystem, element.upper(), '14C3') : { 'sfp2' : [family_data['sfp2']['index'][6]]},
            join_name(system, subsystem, element.upper(), '15C2') : { 'sfp2' : [family_data['sfp2']['index'][7]]},
            join_name(system, subsystem, element.upper(), '18C3') : { 'sfp2' : [family_data['sfp2']['index'][8]]},
            join_name(system, subsystem, element.upper(), '19C2') : { 'sfp2' : [family_data['sfp2']['index'][9]]},
        }
        return _dict

    if element == 'nlk':
        _dict = {join_name(system, subsystem, element.upper(), '01M2') : {'nlk' : family_data['nlk']['index']}}
        return _dict

    if element == 'dipk' or element == 'kicker' or element == 'kick_in':
        _dict = {join_name(system, subsystem, 'KICKERINJ', '01M2'): {'dipk' : family_data['dipk']['index']}}
        return _dict

    else:
        raise Exception('Element %s not found'%element)
