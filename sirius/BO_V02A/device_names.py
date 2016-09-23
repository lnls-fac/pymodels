
from . import families as _families

system = 'bo'

_pvnaming_rule = 2 # 1 : PV Naming Proposal#1; 2 : PV Naming Proposal#2
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
            join_name(system, subsystem, 'TunePkp', '02D') : {},
            join_name(system, subsystem, 'DCCT',    '35D') : {},
        }
        _dict.update(get_element_names(family_data, subsystem, element = 'bpm'))
        _dict.update(get_family_names(family_data, subsystem, family = 'bpm'))
        return _dict

    if subsystem.lower() == 'ps':
        family_dict = {}
        family_dict.update(get_family_names(family_data, subsystem, family = 'bend'))
        family_dict.update(get_family_names(family_data, subsystem, family = 'quad'))
        family_dict.update(get_family_names(family_data, subsystem, family = 'sext'))

        element_dict = {}
        element_dict.update(get_element_names(family_data, subsystem, element = 'hcorr'))
        element_dict.update(get_element_names(family_data, subsystem, element = 'vcorr'))

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

        return element_dict

    if subsystem.lower() == 'pm':
        _dict = get_element_names(family_data, subsystem, element = 'pulsed_magnets')
        return _dict

    if subsystem.lower() == 'ti':
        _dict = {
            join_name(system, subsystem, 'SOE',    '01D') : {},
            join_name(system, subsystem, 'STDMOE', '48D') : {},
            join_name(system, subsystem, 'STDMOE',  _pvnaming_glob) : {},
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

    if family == 'bend' or family == 'b':
        _dict = {
            join_name(system, subsystem, 'BEND', _pvnaming_fam) : {'bend' : family_data['b']['index']}
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

    if element.lower() == 'bpm':
        _dict = {
            join_name(system, subsystem, element.upper(),'01U')  : {'bpm' : [family_data['bpm']['index'][49]]},
            join_name(system, subsystem, element.upper(),'02U')  : {'bpm' : [family_data['bpm']['index'][0]]},
            join_name(system, subsystem, element.upper(),'03U')  : {'bpm' : [family_data['bpm']['index'][1]]},
            join_name(system, subsystem, element.upper(),'04U')  : {'bpm' : [family_data['bpm']['index'][2]]},
            join_name(system, subsystem, element.upper(),'05U')  : {'bpm' : [family_data['bpm']['index'][3]]},
            join_name(system, subsystem, element.upper(),'06U')  : {'bpm' : [family_data['bpm']['index'][4]]},
            join_name(system, subsystem, element.upper(),'07U')  : {'bpm' : [family_data['bpm']['index'][5]]},
            join_name(system, subsystem, element.upper(),'08U')  : {'bpm' : [family_data['bpm']['index'][6]]},
            join_name(system, subsystem, element.upper(),'09U')  : {'bpm' : [family_data['bpm']['index'][7]]},
            join_name(system, subsystem, element.upper(),'10U')  : {'bpm' : [family_data['bpm']['index'][8]]},
            join_name(system, subsystem, element.upper(),'11U')  : {'bpm' : [family_data['bpm']['index'][9]]},
            join_name(system, subsystem, element.upper(),'12U')  : {'bpm' : [family_data['bpm']['index'][10]]},
            join_name(system, subsystem, element.upper(),'13U')  : {'bpm' : [family_data['bpm']['index'][11]]},
            join_name(system, subsystem, element.upper(),'14U')  : {'bpm' : [family_data['bpm']['index'][12]]},
            join_name(system, subsystem, element.upper(),'15U')  : {'bpm' : [family_data['bpm']['index'][13]]},
            join_name(system, subsystem, element.upper(),'16U')  : {'bpm' : [family_data['bpm']['index'][14]]},
            join_name(system, subsystem, element.upper(),'17U')  : {'bpm' : [family_data['bpm']['index'][15]]},
            join_name(system, subsystem, element.upper(),'18U')  : {'bpm' : [family_data['bpm']['index'][16]]},
            join_name(system, subsystem, element.upper(),'19U')  : {'bpm' : [family_data['bpm']['index'][17]]},
            join_name(system, subsystem, element.upper(),'20U')  : {'bpm' : [family_data['bpm']['index'][18]]},
            join_name(system, subsystem, element.upper(),'21U')  : {'bpm' : [family_data['bpm']['index'][19]]},
            join_name(system, subsystem, element.upper(),'22U')  : {'bpm' : [family_data['bpm']['index'][20]]},
            join_name(system, subsystem, element.upper(),'23U')  : {'bpm' : [family_data['bpm']['index'][21]]},
            join_name(system, subsystem, element.upper(),'24U')  : {'bpm' : [family_data['bpm']['index'][22]]},
            join_name(system, subsystem, element.upper(),'25U')  : {'bpm' : [family_data['bpm']['index'][23]]},
            join_name(system, subsystem, element.upper(),'26U')  : {'bpm' : [family_data['bpm']['index'][24]]},
            join_name(system, subsystem, element.upper(),'27U')  : {'bpm' : [family_data['bpm']['index'][25]]},
            join_name(system, subsystem, element.upper(),'28U')  : {'bpm' : [family_data['bpm']['index'][26]]},
            join_name(system, subsystem, element.upper(),'29U')  : {'bpm' : [family_data['bpm']['index'][27]]},
            join_name(system, subsystem, element.upper(),'30U')  : {'bpm' : [family_data['bpm']['index'][28]]},
            join_name(system, subsystem, element.upper(),'31U')  : {'bpm' : [family_data['bpm']['index'][29]]},
            join_name(system, subsystem, element.upper(),'32U')  : {'bpm' : [family_data['bpm']['index'][30]]},
            join_name(system, subsystem, element.upper(),'33U')  : {'bpm' : [family_data['bpm']['index'][31]]},
            join_name(system, subsystem, element.upper(),'34U')  : {'bpm' : [family_data['bpm']['index'][32]]},
            join_name(system, subsystem, element.upper(),'35U')  : {'bpm' : [family_data['bpm']['index'][33]]},
            join_name(system, subsystem, element.upper(),'36U')  : {'bpm' : [family_data['bpm']['index'][34]]},
            join_name(system, subsystem, element.upper(),'37U')  : {'bpm' : [family_data['bpm']['index'][35]]},
            join_name(system, subsystem, element.upper(),'38U')  : {'bpm' : [family_data['bpm']['index'][36]]},
            join_name(system, subsystem, element.upper(),'39U')  : {'bpm' : [family_data['bpm']['index'][37]]},
            join_name(system, subsystem, element.upper(),'40U')  : {'bpm' : [family_data['bpm']['index'][38]]},
            join_name(system, subsystem, element.upper(),'41U')  : {'bpm' : [family_data['bpm']['index'][39]]},
            join_name(system, subsystem, element.upper(),'42U')  : {'bpm' : [family_data['bpm']['index'][40]]},
            join_name(system, subsystem, element.upper(),'43U')  : {'bpm' : [family_data['bpm']['index'][41]]},
            join_name(system, subsystem, element.upper(),'44U')  : {'bpm' : [family_data['bpm']['index'][42]]},
            join_name(system, subsystem, element.upper(),'45U')  : {'bpm' : [family_data['bpm']['index'][43]]},
            join_name(system, subsystem, element.upper(),'46U')  : {'bpm' : [family_data['bpm']['index'][44]]},
            join_name(system, subsystem, element.upper(),'47U')  : {'bpm' : [family_data['bpm']['index'][45]]},
            join_name(system, subsystem, element.upper(),'48U')  : {'bpm' : [family_data['bpm']['index'][46]]},
            join_name(system, subsystem, element.upper(),'49U')  : {'bpm' : [family_data['bpm']['index'][47]]},
            join_name(system, subsystem, element.upper(),'50U')  : {'bpm' : [family_data['bpm']['index'][48]]},
        }
        return _dict

    if element.lower() == 'bend' or element.lower() == 'b':
        _dict = {
            join_name(system, subsystem, 'BEND', '01')  : {'bend' : [family_data['b']['index'][0]]},
            join_name(system, subsystem, 'BEND' ,'02')  : {'bend' : [family_data['b']['index'][1]]},
            join_name(system, subsystem, 'BEND' ,'03')  : {'bend' : [family_data['b']['index'][2]]},
            join_name(system, subsystem, 'BEND' ,'04')  : {'bend' : [family_data['b']['index'][3]]},
            join_name(system, subsystem, 'BEND' ,'05')  : {'bend' : [family_data['b']['index'][4]]},
            join_name(system, subsystem, 'BEND' ,'06')  : {'bend' : [family_data['b']['index'][5]]},
            join_name(system, subsystem, 'BEND' ,'07')  : {'bend' : [family_data['b']['index'][6]]},
            join_name(system, subsystem, 'BEND' ,'08')  : {'bend' : [family_data['b']['index'][7]]},
            join_name(system, subsystem, 'BEND' ,'09')  : {'bend' : [family_data['b']['index'][8]]},
            join_name(system, subsystem, 'BEND' ,'10')  : {'bend' : [family_data['b']['index'][9]]},
            join_name(system, subsystem, 'BEND' ,'11')  : {'bend' : [family_data['b']['index'][10]]},
            join_name(system, subsystem, 'BEND' ,'12')  : {'bend' : [family_data['b']['index'][11]]},
            join_name(system, subsystem, 'BEND' ,'13')  : {'bend' : [family_data['b']['index'][12]]},
            join_name(system, subsystem, 'BEND' ,'14')  : {'bend' : [family_data['b']['index'][13]]},
            join_name(system, subsystem, 'BEND' ,'15')  : {'bend' : [family_data['b']['index'][14]]},
            join_name(system, subsystem, 'BEND' ,'16')  : {'bend' : [family_data['b']['index'][15]]},
            join_name(system, subsystem, 'BEND' ,'17')  : {'bend' : [family_data['b']['index'][16]]},
            join_name(system, subsystem, 'BEND' ,'18')  : {'bend' : [family_data['b']['index'][17]]},
            join_name(system, subsystem, 'BEND' ,'19')  : {'bend' : [family_data['b']['index'][18]]},
            join_name(system, subsystem, 'BEND' ,'20')  : {'bend' : [family_data['b']['index'][19]]},
            join_name(system, subsystem, 'BEND' ,'21')  : {'bend' : [family_data['b']['index'][20]]},
            join_name(system, subsystem, 'BEND' ,'22')  : {'bend' : [family_data['b']['index'][21]]},
            join_name(system, subsystem, 'BEND' ,'23')  : {'bend' : [family_data['b']['index'][22]]},
            join_name(system, subsystem, 'BEND' ,'24')  : {'bend' : [family_data['b']['index'][23]]},
            join_name(system, subsystem, 'BEND' ,'25')  : {'bend' : [family_data['b']['index'][24]]},
            join_name(system, subsystem, 'BEND' ,'26')  : {'bend' : [family_data['b']['index'][25]]},
            join_name(system, subsystem, 'BEND' ,'27')  : {'bend' : [family_data['b']['index'][26]]},
            join_name(system, subsystem, 'BEND' ,'28')  : {'bend' : [family_data['b']['index'][27]]},
            join_name(system, subsystem, 'BEND' ,'29')  : {'bend' : [family_data['b']['index'][28]]},
            join_name(system, subsystem, 'BEND' ,'30')  : {'bend' : [family_data['b']['index'][29]]},
            join_name(system, subsystem, 'BEND' ,'31')  : {'bend' : [family_data['b']['index'][30]]},
            join_name(system, subsystem, 'BEND' ,'32')  : {'bend' : [family_data['b']['index'][31]]},
            join_name(system, subsystem, 'BEND' ,'33')  : {'bend' : [family_data['b']['index'][32]]},
            join_name(system, subsystem, 'BEND' ,'34')  : {'bend' : [family_data['b']['index'][33]]},
            join_name(system, subsystem, 'BEND' ,'35')  : {'bend' : [family_data['b']['index'][34]]},
            join_name(system, subsystem, 'BEND' ,'36')  : {'bend' : [family_data['b']['index'][35]]},
            join_name(system, subsystem, 'BEND' ,'37')  : {'bend' : [family_data['b']['index'][36]]},
            join_name(system, subsystem, 'BEND' ,'38')  : {'bend' : [family_data['b']['index'][37]]},
            join_name(system, subsystem, 'BEND' ,'39')  : {'bend' : [family_data['b']['index'][38]]},
            join_name(system, subsystem, 'BEND' ,'40')  : {'bend' : [family_data['b']['index'][39]]},
            join_name(system, subsystem, 'BEND' ,'41')  : {'bend' : [family_data['b']['index'][40]]},
            join_name(system, subsystem, 'BEND' ,'42')  : {'bend' : [family_data['b']['index'][41]]},
            join_name(system, subsystem, 'BEND' ,'43')  : {'bend' : [family_data['b']['index'][42]]},
            join_name(system, subsystem, 'BEND' ,'44')  : {'bend' : [family_data['b']['index'][43]]},
            join_name(system, subsystem, 'BEND' ,'45')  : {'bend' : [family_data['b']['index'][44]]},
            join_name(system, subsystem, 'BEND' ,'46')  : {'bend' : [family_data['b']['index'][45]]},
            join_name(system, subsystem, 'BEND' ,'47')  : {'bend' : [family_data['b']['index'][46]]},
            join_name(system, subsystem, 'BEND' ,'48')  : {'bend' : [family_data['b']['index'][47]]},
            join_name(system, subsystem, 'BEND' ,'49')  : {'bend' : [family_data['b']['index'][48]]},
            join_name(system, subsystem, 'BEND' ,'50')  : {'bend' : [family_data['b']['index'][49]]},
        }
        return _dict

    if element.lower() == 'cv':
        _dict = {
            join_name(system, subsystem, element.upper(),'01U')  : {'cv' : [family_data['cv']['index'][24]]},
            join_name(system, subsystem, element.upper(),'03U')  : {'cv' : [family_data['cv']['index'][0]]},
            join_name(system, subsystem, element.upper(),'05U')  : {'cv' : [family_data['cv']['index'][1]]},
            join_name(system, subsystem, element.upper(),'07U')  : {'cv' : [family_data['cv']['index'][2]]},
            join_name(system, subsystem, element.upper(),'09U')  : {'cv' : [family_data['cv']['index'][3]]},
            join_name(system, subsystem, element.upper(),'11U')  : {'cv' : [family_data['cv']['index'][4]]},
            join_name(system, subsystem, element.upper(),'13U')  : {'cv' : [family_data['cv']['index'][5]]},
            join_name(system, subsystem, element.upper(),'15U')  : {'cv' : [family_data['cv']['index'][6]]},
            join_name(system, subsystem, element.upper(),'17U')  : {'cv' : [family_data['cv']['index'][7]]},
            join_name(system, subsystem, element.upper(),'19U')  : {'cv' : [family_data['cv']['index'][8]]},
            join_name(system, subsystem, element.upper(),'21U')  : {'cv' : [family_data['cv']['index'][9]]},
            join_name(system, subsystem, element.upper(),'23U')  : {'cv' : [family_data['cv']['index'][10]]},
            join_name(system, subsystem, element.upper(),'25U')  : {'cv' : [family_data['cv']['index'][11]]},
            join_name(system, subsystem, element.upper(),'27U')  : {'cv' : [family_data['cv']['index'][12]]},
            join_name(system, subsystem, element.upper(),'29U')  : {'cv' : [family_data['cv']['index'][13]]},
            join_name(system, subsystem, element.upper(),'31U')  : {'cv' : [family_data['cv']['index'][14]]},
            join_name(system, subsystem, element.upper(),'33U')  : {'cv' : [family_data['cv']['index'][15]]},
            join_name(system, subsystem, element.upper(),'35U')  : {'cv' : [family_data['cv']['index'][16]]},
            join_name(system, subsystem, element.upper(),'37U')  : {'cv' : [family_data['cv']['index'][17]]},
            join_name(system, subsystem, element.upper(),'39U')  : {'cv' : [family_data['cv']['index'][18]]},
            join_name(system, subsystem, element.upper(),'41U')  : {'cv' : [family_data['cv']['index'][19]]},
            join_name(system, subsystem, element.upper(),'43U')  : {'cv' : [family_data['cv']['index'][20]]},
            join_name(system, subsystem, element.upper(),'45U')  : {'cv' : [family_data['cv']['index'][21]]},
            join_name(system, subsystem, element.upper(),'47U')  : {'cv' : [family_data['cv']['index'][22]]},
            join_name(system, subsystem, element.upper(),'49U')  : {'cv' : [family_data['cv']['index'][23]]},
        }
        return _dict

    if element.lower() == 'ch':
        _dict = {
            join_name(system, subsystem, element.upper(),'01U')  : {'ch' : [family_data['ch']['index'][24]]},
            join_name(system, subsystem, element.upper(),'03U')  : {'ch' : [family_data['ch']['index'][0]]},
            join_name(system, subsystem, element.upper(),'05U')  : {'ch' : [family_data['ch']['index'][1]]},
            join_name(system, subsystem, element.upper(),'07U')  : {'ch' : [family_data['ch']['index'][2]]},
            join_name(system, subsystem, element.upper(),'09U')  : {'ch' : [family_data['ch']['index'][3]]},
            join_name(system, subsystem, element.upper(),'11U')  : {'ch' : [family_data['ch']['index'][4]]},
            join_name(system, subsystem, element.upper(),'13U')  : {'ch' : [family_data['ch']['index'][5]]},
            join_name(system, subsystem, element.upper(),'15U')  : {'ch' : [family_data['ch']['index'][6]]},
            join_name(system, subsystem, element.upper(),'17U')  : {'ch' : [family_data['ch']['index'][7]]},
            join_name(system, subsystem, element.upper(),'19U')  : {'ch' : [family_data['ch']['index'][8]]},
            join_name(system, subsystem, element.upper(),'21U')  : {'ch' : [family_data['ch']['index'][9]]},
            join_name(system, subsystem, element.upper(),'23U')  : {'ch' : [family_data['ch']['index'][10]]},
            join_name(system, subsystem, element.upper(),'25U')  : {'ch' : [family_data['ch']['index'][11]]},
            join_name(system, subsystem, element.upper(),'27U')  : {'ch' : [family_data['ch']['index'][12]]},
            join_name(system, subsystem, element.upper(),'29U')  : {'ch' : [family_data['ch']['index'][13]]},
            join_name(system, subsystem, element.upper(),'31U')  : {'ch' : [family_data['ch']['index'][14]]},
            join_name(system, subsystem, element.upper(),'33U')  : {'ch' : [family_data['ch']['index'][15]]},
            join_name(system, subsystem, element.upper(),'35U')  : {'ch' : [family_data['ch']['index'][16]]},
            join_name(system, subsystem, element.upper(),'37U')  : {'ch' : [family_data['ch']['index'][17]]},
            join_name(system, subsystem, element.upper(),'39U')  : {'ch' : [family_data['ch']['index'][18]]},
            join_name(system, subsystem, element.upper(),'41U')  : {'ch' : [family_data['ch']['index'][19]]},
            join_name(system, subsystem, element.upper(),'43U')  : {'ch' : [family_data['ch']['index'][20]]},
            join_name(system, subsystem, element.upper(),'45U')  : {'ch' : [family_data['ch']['index'][21]]},
            join_name(system, subsystem, element.upper(),'47U')  : {'ch' : [family_data['ch']['index'][22]]},
            join_name(system, subsystem, element.upper(),'49D')  : {'ch' : [family_data['ch']['index'][23]]},
        }
        return _dict

    if element.lower() == 'qd':
        _dict = {
            join_name(system, subsystem, element.upper(),'02D')  : {'qd' : [family_data['qd']['index'][0]]},
            join_name(system, subsystem, element.upper(),'04D')  : {'qd' : [family_data['qd']['index'][1]]},
            join_name(system, subsystem, element.upper(),'06D')  : {'qd' : [family_data['qd']['index'][2]]},
            join_name(system, subsystem, element.upper(),'08D')  : {'qd' : [family_data['qd']['index'][3]]},
            join_name(system, subsystem, element.upper(),'10D')  : {'qd' : [family_data['qd']['index'][4]]},
            join_name(system, subsystem, element.upper(),'12D')  : {'qd' : [family_data['qd']['index'][5]]},
            join_name(system, subsystem, element.upper(),'14D')  : {'qd' : [family_data['qd']['index'][6]]},
            join_name(system, subsystem, element.upper(),'16D')  : {'qd' : [family_data['qd']['index'][7]]},
            join_name(system, subsystem, element.upper(),'18D')  : {'qd' : [family_data['qd']['index'][8]]},
            join_name(system, subsystem, element.upper(),'20D')  : {'qd' : [family_data['qd']['index'][9]]},
            join_name(system, subsystem, element.upper(),'22D')  : {'qd' : [family_data['qd']['index'][10]]},
            join_name(system, subsystem, element.upper(),'24D')  : {'qd' : [family_data['qd']['index'][11]]},
            join_name(system, subsystem, element.upper(),'26D')  : {'qd' : [family_data['qd']['index'][12]]},
            join_name(system, subsystem, element.upper(),'28D')  : {'qd' : [family_data['qd']['index'][13]]},
            join_name(system, subsystem, element.upper(),'30D')  : {'qd' : [family_data['qd']['index'][14]]},
            join_name(system, subsystem, element.upper(),'32D')  : {'qd' : [family_data['qd']['index'][15]]},
            join_name(system, subsystem, element.upper(),'34D')  : {'qd' : [family_data['qd']['index'][16]]},
            join_name(system, subsystem, element.upper(),'36D')  : {'qd' : [family_data['qd']['index'][17]]},
            join_name(system, subsystem, element.upper(),'38D')  : {'qd' : [family_data['qd']['index'][18]]},
            join_name(system, subsystem, element.upper(),'40D')  : {'qd' : [family_data['qd']['index'][19]]},
            join_name(system, subsystem, element.upper(),'42D')  : {'qd' : [family_data['qd']['index'][20]]},
            join_name(system, subsystem, element.upper(),'44D')  : {'qd' : [family_data['qd']['index'][21]]},
            join_name(system, subsystem, element.upper(),'46D')  : {'qd' : [family_data['qd']['index'][22]]},
            join_name(system, subsystem, element.upper(),'48D')  : {'qd' : [family_data['qd']['index'][23]]},
            join_name(system, subsystem, element.upper(),'50D')  : {'qd' : [family_data['qd']['index'][24]]},
        }
        return _dict

    if element.lower() == 'qf':
        _dict = {
            join_name(system, subsystem, element.upper(),'01')  : {'qf' : [family_data['qf']['index'][0]]},
            join_name(system, subsystem, element.upper(),'02')  : {'qf' : [family_data['qf']['index'][1]]},
            join_name(system, subsystem, element.upper(),'03')  : {'qf' : [family_data['qf']['index'][2]]},
            join_name(system, subsystem, element.upper(),'04')  : {'qf' : [family_data['qf']['index'][3]]},
            join_name(system, subsystem, element.upper(),'05')  : {'qf' : [family_data['qf']['index'][4]]},
            join_name(system, subsystem, element.upper(),'06')  : {'qf' : [family_data['qf']['index'][5]]},
            join_name(system, subsystem, element.upper(),'07')  : {'qf' : [family_data['qf']['index'][6]]},
            join_name(system, subsystem, element.upper(),'08')  : {'qf' : [family_data['qf']['index'][7]]},
            join_name(system, subsystem, element.upper(),'09')  : {'qf' : [family_data['qf']['index'][8]]},
            join_name(system, subsystem, element.upper(),'10')  : {'qf' : [family_data['qf']['index'][9]]},
            join_name(system, subsystem, element.upper(),'11')  : {'qf' : [family_data['qf']['index'][10]]},
            join_name(system, subsystem, element.upper(),'12')  : {'qf' : [family_data['qf']['index'][11]]},
            join_name(system, subsystem, element.upper(),'13')  : {'qf' : [family_data['qf']['index'][12]]},
            join_name(system, subsystem, element.upper(),'14')  : {'qf' : [family_data['qf']['index'][13]]},
            join_name(system, subsystem, element.upper(),'15')  : {'qf' : [family_data['qf']['index'][14]]},
            join_name(system, subsystem, element.upper(),'16')  : {'qf' : [family_data['qf']['index'][15]]},
            join_name(system, subsystem, element.upper(),'17')  : {'qf' : [family_data['qf']['index'][16]]},
            join_name(system, subsystem, element.upper(),'18')  : {'qf' : [family_data['qf']['index'][17]]},
            join_name(system, subsystem, element.upper(),'19')  : {'qf' : [family_data['qf']['index'][18]]},
            join_name(system, subsystem, element.upper(),'20')  : {'qf' : [family_data['qf']['index'][19]]},
            join_name(system, subsystem, element.upper(),'21')  : {'qf' : [family_data['qf']['index'][20]]},
            join_name(system, subsystem, element.upper(),'22')  : {'qf' : [family_data['qf']['index'][21]]},
            join_name(system, subsystem, element.upper(),'23')  : {'qf' : [family_data['qf']['index'][22]]},
            join_name(system, subsystem, element.upper(),'24')  : {'qf' : [family_data['qf']['index'][23]]},
            join_name(system, subsystem, element.upper(),'25')  : {'qf' : [family_data['qf']['index'][24]]},
            join_name(system, subsystem, element.upper(),'26')  : {'qf' : [family_data['qf']['index'][25]]},
            join_name(system, subsystem, element.upper(),'27')  : {'qf' : [family_data['qf']['index'][26]]},
            join_name(system, subsystem, element.upper(),'28')  : {'qf' : [family_data['qf']['index'][27]]},
            join_name(system, subsystem, element.upper(),'29')  : {'qf' : [family_data['qf']['index'][28]]},
            join_name(system, subsystem, element.upper(),'30')  : {'qf' : [family_data['qf']['index'][29]]},
            join_name(system, subsystem, element.upper(),'31')  : {'qf' : [family_data['qf']['index'][30]]},
            join_name(system, subsystem, element.upper(),'32')  : {'qf' : [family_data['qf']['index'][31]]},
            join_name(system, subsystem, element.upper(),'33')  : {'qf' : [family_data['qf']['index'][32]]},
            join_name(system, subsystem, element.upper(),'34')  : {'qf' : [family_data['qf']['index'][33]]},
            join_name(system, subsystem, element.upper(),'35')  : {'qf' : [family_data['qf']['index'][34]]},
            join_name(system, subsystem, element.upper(),'36')  : {'qf' : [family_data['qf']['index'][35]]},
            join_name(system, subsystem, element.upper(),'37')  : {'qf' : [family_data['qf']['index'][36]]},
            join_name(system, subsystem, element.upper(),'38')  : {'qf' : [family_data['qf']['index'][37]]},
            join_name(system, subsystem, element.upper(),'39')  : {'qf' : [family_data['qf']['index'][38]]},
            join_name(system, subsystem, element.upper(),'40')  : {'qf' : [family_data['qf']['index'][39]]},
            join_name(system, subsystem, element.upper(),'41')  : {'qf' : [family_data['qf']['index'][40]]},
            join_name(system, subsystem, element.upper(),'42')  : {'qf' : [family_data['qf']['index'][41]]},
            join_name(system, subsystem, element.upper(),'43')  : {'qf' : [family_data['qf']['index'][42]]},
            join_name(system, subsystem, element.upper(),'44')  : {'qf' : [family_data['qf']['index'][43]]},
            join_name(system, subsystem, element.upper(),'45')  : {'qf' : [family_data['qf']['index'][44]]},
            join_name(system, subsystem, element.upper(),'46')  : {'qf' : [family_data['qf']['index'][45]]},
            join_name(system, subsystem, element.upper(),'47')  : {'qf' : [family_data['qf']['index'][46]]},
            join_name(system, subsystem, element.upper(),'48')  : {'qf' : [family_data['qf']['index'][47]]},
            join_name(system, subsystem, element.upper(),'49')  : {'qf' : [family_data['qf']['index'][48]]},
            join_name(system, subsystem, element.upper(),'50')  : {'qf' : [family_data['qf']['index'][49]]},
        }
        return _dict

    if element.lower() == 'sd':
        _dict = {
            join_name(system, subsystem, element.upper(),'03U')  : {'sd' : [family_data['sd']['index'][0]]},
            join_name(system, subsystem, element.upper(),'08U')  : {'sd' : [family_data['sd']['index'][1]]},
            join_name(system, subsystem, element.upper(),'13U')  : {'sd' : [family_data['sd']['index'][2]]},
            join_name(system, subsystem, element.upper(),'18U')  : {'sd' : [family_data['sd']['index'][3]]},
            join_name(system, subsystem, element.upper(),'23U')  : {'sd' : [family_data['sd']['index'][4]]},
            join_name(system, subsystem, element.upper(),'28U')  : {'sd' : [family_data['sd']['index'][5]]},
            join_name(system, subsystem, element.upper(),'33U')  : {'sd' : [family_data['sd']['index'][6]]},
            join_name(system, subsystem, element.upper(),'38U')  : {'sd' : [family_data['sd']['index'][7]]},
            join_name(system, subsystem, element.upper(),'43U')  : {'sd' : [family_data['sd']['index'][8]]},
            join_name(system, subsystem, element.upper(),'48U')  : {'sd' : [family_data['sd']['index'][9]]},
        }
        return _dict

    if element.lower() == 'sf':
        _dict = {
            join_name(system, subsystem, element.upper(),'02U')  : {'sf' : [family_data['sf']['index'][0]]},
            join_name(system, subsystem, element.upper(),'04U')  : {'sf' : [family_data['sf']['index'][1]]},
            join_name(system, subsystem, element.upper(),'06U')  : {'sf' : [family_data['sf']['index'][2]]},
            join_name(system, subsystem, element.upper(),'08U')  : {'sf' : [family_data['sf']['index'][3]]},
            join_name(system, subsystem, element.upper(),'10U')  : {'sf' : [family_data['sf']['index'][4]]},
            join_name(system, subsystem, element.upper(),'12U')  : {'sf' : [family_data['sf']['index'][5]]},
            join_name(system, subsystem, element.upper(),'14U')  : {'sf' : [family_data['sf']['index'][6]]},
            join_name(system, subsystem, element.upper(),'16U')  : {'sf' : [family_data['sf']['index'][7]]},
            join_name(system, subsystem, element.upper(),'18U')  : {'sf' : [family_data['sf']['index'][8]]},
            join_name(system, subsystem, element.upper(),'20U')  : {'sf' : [family_data['sf']['index'][9]]},
            join_name(system, subsystem, element.upper(),'22U')  : {'sf' : [family_data['sf']['index'][10]]},
            join_name(system, subsystem, element.upper(),'24U')  : {'sf' : [family_data['sf']['index'][11]]},
            join_name(system, subsystem, element.upper(),'26U')  : {'sf' : [family_data['sf']['index'][12]]},
            join_name(system, subsystem, element.upper(),'28U')  : {'sf' : [family_data['sf']['index'][13]]},
            join_name(system, subsystem, element.upper(),'30U')  : {'sf' : [family_data['sf']['index'][14]]},
            join_name(system, subsystem, element.upper(),'32U')  : {'sf' : [family_data['sf']['index'][15]]},
            join_name(system, subsystem, element.upper(),'34U')  : {'sf' : [family_data['sf']['index'][16]]},
            join_name(system, subsystem, element.upper(),'36U')  : {'sf' : [family_data['sf']['index'][17]]},
            join_name(system, subsystem, element.upper(),'38U')  : {'sf' : [family_data['sf']['index'][18]]},
            join_name(system, subsystem, element.upper(),'40U')  : {'sf' : [family_data['sf']['index'][19]]},
            join_name(system, subsystem, element.upper(),'42U')  : {'sf' : [family_data['sf']['index'][20]]},
            join_name(system, subsystem, element.upper(),'44U')  : {'sf' : [family_data['sf']['index'][21]]},
            join_name(system, subsystem, element.upper(),'46U')  : {'sf' : [family_data['sf']['index'][22]]},
            join_name(system, subsystem, element.upper(),'48U')  : {'sf' : [family_data['sf']['index'][23]]},
            join_name(system, subsystem, element.upper(),'50U')  : {'sf' : [family_data['sf']['index'][24]]},
        }
        return _dict

    if element.lower() == 'kick_in':
        _dict = {join_name(system, subsystem, 'KICKERINJ','01D')  : {'kick_in' : family_data['kick_in']['index']}}
        return _dict

    if element.lower() == 'kick_ex':
        _dict = {
            join_name(system, subsystem, 'KICKEREXT', '48D', '1')  : {'kick_ex' : [family_data['kick_ex']['index'][0]]},
            join_name(system, subsystem, 'KICKEREXT', '48D', '2')  : {'kick_ex' : [family_data['kick_ex']['index'][1]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    _dict = get_device_names(accelerator, 'ma')
    _dict.update(get_device_names(accelerator, 'pm'))
    return _dict
