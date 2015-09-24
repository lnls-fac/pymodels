
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
        subsystems = ['sipa', 'sidi', 'sirf', 'sips', 'siti']
        record_names_dict = {}
        for subsystem in subsystems:
            record_names_dict.update(get_record_names(family_data, subsystem))
        return record_names_dict

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
        }
        return _dict

    if subsystem.lower() == 'sidi':
        prefix = 'SIDI-'

        _dict = {
                'SIDI-TUNEH':{},
                'SIDI-TUNEV':{},
                'SIDI-TUNES':{},
                'SIDI-CURRENT':{},
                'SIDI-BCURRENT':{},
        }
        bpm_dict = get_element_names(family_data, element = 'bpm', prefix = prefix)
        _dict.update(bpm_dict)
        bpm_fam_dict = get_family_names(family_data, family = 'bpm', prefix = prefix)
        _dict.update(bpm_fam_dict)
        return _dict

    if subsystem.lower() == 'sips':
        prefix = 'SIPS-'

        element_dict = {}
        element_dict.update(get_element_names(family_data, element = 'quad', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'sext', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'ch', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'cv', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'qs', prefix = prefix))

        family_dict = {}
        family_dict.update(get_family_names(family_data, family = 'bend', prefix = prefix))
        family_dict.update(get_family_names(family_data, family = 'quad', prefix = prefix))
        family_dict.update(get_family_names(family_data, family = 'sext', prefix = prefix))

        _dict = {}
        _dict.update(element_dict)
        _dict.update(family_dict)
        return _dict

    if subsystem.lower() == 'sima':
        prefix = 'SIMA-'

        element_dict = {}
        element_dict.update(get_element_names(family_data, element = 'bend', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'quad', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'sext', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'ch', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'cv', prefix = prefix))
        element_dict.update(get_element_names(family_data, element = 'qs', prefix = prefix))

        return element_dict

    if subsystem.lower() == 'siti':
        _dict = {
                'SITI-KICKINJ-ENABLED':{},
                'SITI-KICKINJ-DELAY':{},
                'SITI-PMM-ENABLED':{},
                'SITI-PMM-DELAY':{},
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

        family_names = []
        family_names += _families.families_dipoles()
        family_names += _families.families_quadrupoles()
        family_names += _families.families_sextupoles()
        family_names += ['bpm']

        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix = prefix))
        return _dict

    if family.lower() == 'bend':
        _dict = { prefix + 'BEND-FAM' :
            {'b1' : family_data['b1']['index'],
             'b2' : family_data['b2']['index'],
             'b3' : family_data['b3']['index'],
             'bc' : family_data['bc']['index'],
            }
        }
        return _dict

    if family.lower() == 'quad':
        family_names = _families.families_quadrupoles()
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix = prefix))
        return _dict

    if family.lower() == 'sext':
        family_names = _families.families_sextupoles()
        _dict = {}
        for family in family_names:
            _dict.update(get_family_names(family_data, family, prefix = prefix))
        return _dict

    if family.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {prefix + 'BPM-FAM-X': {'bpm': indices},
                 prefix + 'BPM-FAM-Y': {'bpm': indices},
                }
        return _dict

    if family.lower() == 'qfa':
        indices = family_data['qfa']['index']
        _dict = {prefix + 'QFA-FAM': {'qfa': indices}}
        return _dict

    if family.lower() == 'qda':
        indices = family_data['qda']['index']
        _dict = {prefix + 'QDA-FAM': {'qda': indices}}
        return _dict

    if family.lower() == 'qfb':
        indices = family_data['qfb']['index']
        _dict = {prefix + 'QFB-FAM': {'qfb': indices}}
        return _dict

    if family.lower() == 'qdb1':
        indices = family_data['qdb1']['index']
        _dict = {prefix + 'QDB1-FAM': {'qdb1': indices}}
        return _dict

    if family.lower() == 'qdb2':
        indices = family_data['qdb2']['index']
        _dict = {prefix + 'QDB2-FAM': {'qdb2': indices}}
        return _dict

    if family.lower() == 'qf1':
        indices = family_data['qf1']['index']
        _dict = {prefix + 'QF1-FAM': {'qf1': indices}}
        return _dict

    if family.lower() == 'qf2':
        indices = family_data['qf2']['index']
        _dict = {prefix + 'QF2-FAM': {'qf2': indices}}
        return _dict

    if family.lower() == 'qf3':
        indices = family_data['qf3']['index']
        _dict = {prefix + 'QF3-FAM': {'qf3': indices}}
        return _dict

    if family.lower() == 'qf4':
        indices = family_data['qf4']['index']
        _dict = {prefix + 'QF4-FAM': {'qf4': indices}}
        return _dict

    if family.lower() == 'sfa':
        indices = family_data['sfa']['index']
        _dict = {prefix + 'SFA-FAM': {'sfa': indices}}
        return _dict

    if family.lower() == 'sda':
        indices = family_data['sda']['index']
        _dict = {prefix + 'SDA-FAM': {'sda': indices}}
        return _dict

    if family.lower() == 'sd1':
        indices = family_data['sd1']['index']
        _dict = {prefix + 'SD1-FAM': {'sd1': indices}}
        return _dict

    if family.lower() == 'sf1':
        indices = family_data['sf1']['index']
        _dict = {prefix + 'SF1-FAM': {'sf1': indices}}
        return _dict

    if family.lower() == 'sd2':
        indices = family_data['sd2']['index']
        _dict = {prefix + 'SD2-FAM': {'sd2': indices}}
        return _dict

    if family.lower() == 'sd3':
        indices = family_data['sd3']['index']
        _dict = {prefix + 'SD3-FAM': {'sd3': indices}}
        return _dict

    if family.lower() == 'sf2':
        indices = family_data['sf2']['index']
        _dict = {prefix + 'SF2-FAM': {'sf2': indices}}
        return _dict

    if family.lower() == 'sf3':
        indices = family_data['sf3']['index']
        _dict = {prefix + 'SF3-FAM': {'sf3': indices}}
        return _dict

    if family.lower() == 'sd4':
        indices = family_data['sd4']['index']
        _dict = {prefix + 'SD4-FAM': {'sd4': indices}}
        return _dict

    if family.lower() == 'sd5':
        indices = family_data['sd5']['index']
        _dict = {prefix + 'SD5-FAM': {'sd5': indices}}
        return _dict

    if family.lower() == 'sf4':
        indices = family_data['sf4']['index']
        _dict = {prefix + 'SF4-FAM': {'sf4': indices}}
        return _dict

    if family.lower() == 'sd6':
        indices = family_data['sd6']['index']
        _dict = {prefix + 'SD6-FAM': {'sd6': indices}}
        return _dict

    if family.lower() == 'sdb':
        indices = family_data['sdb']['index']
        _dict = {prefix + 'SDB-FAM': {'sdb': indices}}
        return _dict

    if family.lower() == 'sfb':
        indices = family_data['sfb']['index']
        _dict = {prefix + 'SFB-FAM': {'sfb': indices}}
        return _dict

    else:
        raise Exception('Family %s not found'%family)


def get_element_names(accelerator, element = None, prefix = ''):

    if not isinstance(accelerator, dict):
        family_data = _families.get_family_data(accelerator)
    else:
        family_data = accelerator

    if element == None:
        elements = []
        elements += _families.families_dipoles()
        elements += _families.families_quadrupoles()
        elements += _families.families_sextupoles()
        elements += _families.families_horizontal_correctors()
        elements += _families.families_vertical_correctors()
        elements += _families.families_skew_correctors()
        elements += ['bpm']

        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'bend':
        _dict = {}
        _dict.update(get_element_names(family_data, 'b1', prefix = prefix))
        _dict.update(get_element_names(family_data, 'b2', prefix = prefix))
        _dict.update(get_element_names(family_data, 'b3', prefix = prefix))
        _dict.update(get_element_names(family_data, 'bc', prefix = prefix))
        return _dict

    if element.lower() == 'quad':
        elements = _families.families_quadrupoles()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'sext':
        elements = _families.families_sextupoles()
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

    if element.lower() == 'ch':
        elements = _families.families_horizontal_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'cv':
        elements = _families.families_vertical_correctors()
        _dict = {}
        for element in elements:
            _dict.update(get_element_names(family_data, element, prefix = prefix))
        return _dict

    if element.lower() == 'bpm':
        prefix = prefix + 'BPM-'
        _dict = {

            #Sector 01
            prefix + '01M1'   : {'bpm' : [family_data['bpm']['index'][179]]},
            prefix + '01M2'   : {'bpm' : [family_data['bpm']['index'][0]]},
            prefix + '01C1-A' : {'bpm' : [family_data['bpm']['index'][1]]},
            prefix + '01C1-B' : {'bpm' : [family_data['bpm']['index'][2]]},
            prefix + '01C2-A' : {'bpm' : [family_data['bpm']['index'][3]]},
            prefix + '01C2-B' : {'bpm' : [family_data['bpm']['index'][4]]},
            prefix + '01C4'   : {'bpm' : [family_data['bpm']['index'][5]]},
            prefix + '01C5-A' : {'bpm' : [family_data['bpm']['index'][6]]},
            prefix + '01C5-B' : {'bpm' : [family_data['bpm']['index'][7]]},

            #Sector 02
            prefix + '02M1'   : {'bpm' : [family_data['bpm']['index'][8]]},
            prefix + '02M2'   : {'bpm' : [family_data['bpm']['index'][9]]},
            prefix + '02C1-A' : {'bpm' : [family_data['bpm']['index'][10]]},
            prefix + '02C1-B' : {'bpm' : [family_data['bpm']['index'][11]]},
            prefix + '02C2-A' : {'bpm' : [family_data['bpm']['index'][12]]},
            prefix + '02C2-B' : {'bpm' : [family_data['bpm']['index'][13]]},
            prefix + '02C4'   : {'bpm' : [family_data['bpm']['index'][14]]},
            prefix + '02C5-A' : {'bpm' : [family_data['bpm']['index'][15]]},
            prefix + '02C5-B' : {'bpm' : [family_data['bpm']['index'][16]]},

            #Sector 03
            prefix + '03M1'   : {'bpm' : [family_data['bpm']['index'][17]]},
            prefix + '03M2'   : {'bpm' : [family_data['bpm']['index'][18]]},
            prefix + '03C1-A' : {'bpm' : [family_data['bpm']['index'][19]]},
            prefix + '03C1-B' : {'bpm' : [family_data['bpm']['index'][20]]},
            prefix + '03C2-A' : {'bpm' : [family_data['bpm']['index'][21]]},
            prefix + '03C2-B' : {'bpm' : [family_data['bpm']['index'][22]]},
            prefix + '03C4'   : {'bpm' : [family_data['bpm']['index'][23]]},
            prefix + '03C5-A' : {'bpm' : [family_data['bpm']['index'][24]]},
            prefix + '03C5-B' : {'bpm' : [family_data['bpm']['index'][25]]},

            #Sector 04
            prefix + '04M1'   : {'bpm' : [family_data['bpm']['index'][26]]},
            prefix + '04M2'   : {'bpm' : [family_data['bpm']['index'][27]]},
            prefix + '04C1-A' : {'bpm' : [family_data['bpm']['index'][28]]},
            prefix + '04C1-B' : {'bpm' : [family_data['bpm']['index'][29]]},
            prefix + '04C2-A' : {'bpm' : [family_data['bpm']['index'][30]]},
            prefix + '04C2-B' : {'bpm' : [family_data['bpm']['index'][31]]},
            prefix + '04C4'   : {'bpm' : [family_data['bpm']['index'][32]]},
            prefix + '04C5-A' : {'bpm' : [family_data['bpm']['index'][33]]},
            prefix + '04C5-B' : {'bpm' : [family_data['bpm']['index'][34]]},

            #Sector 05
            prefix + '05M1'   : {'bpm' : [family_data['bpm']['index'][35]]},
            prefix + '05M2'   : {'bpm' : [family_data['bpm']['index'][36]]},
            prefix + '05C1-A' : {'bpm' : [family_data['bpm']['index'][37]]},
            prefix + '05C1-B' : {'bpm' : [family_data['bpm']['index'][38]]},
            prefix + '05C2-A' : {'bpm' : [family_data['bpm']['index'][39]]},
            prefix + '05C2-B' : {'bpm' : [family_data['bpm']['index'][40]]},
            prefix + '05C4'   : {'bpm' : [family_data['bpm']['index'][41]]},
            prefix + '05C5-A' : {'bpm' : [family_data['bpm']['index'][42]]},
            prefix + '05C5-B' : {'bpm' : [family_data['bpm']['index'][43]]},

            #Sector 06
            prefix + '06M1'   : {'bpm' : [family_data['bpm']['index'][44]]},
            prefix + '06M2'   : {'bpm' : [family_data['bpm']['index'][45]]},
            prefix + '06C1-A' : {'bpm' : [family_data['bpm']['index'][46]]},
            prefix + '06C1-B' : {'bpm' : [family_data['bpm']['index'][47]]},
            prefix + '06C2-A' : {'bpm' : [family_data['bpm']['index'][48]]},
            prefix + '06C2-B' : {'bpm' : [family_data['bpm']['index'][49]]},
            prefix + '06C4'   : {'bpm' : [family_data['bpm']['index'][50]]},
            prefix + '06C5-A' : {'bpm' : [family_data['bpm']['index'][51]]},
            prefix + '06C5-B' : {'bpm' : [family_data['bpm']['index'][52]]},

            #Sector 07
            prefix + '07M1'   : {'bpm' : [family_data['bpm']['index'][53]]},
            prefix + '07M2'   : {'bpm' : [family_data['bpm']['index'][54]]},
            prefix + '07C1-A' : {'bpm' : [family_data['bpm']['index'][55]]},
            prefix + '07C1-B' : {'bpm' : [family_data['bpm']['index'][56]]},
            prefix + '07C2-A' : {'bpm' : [family_data['bpm']['index'][57]]},
            prefix + '07C2-B' : {'bpm' : [family_data['bpm']['index'][58]]},
            prefix + '07C4'   : {'bpm' : [family_data['bpm']['index'][59]]},
            prefix + '07C5-A' : {'bpm' : [family_data['bpm']['index'][60]]},
            prefix + '07C5-B' : {'bpm' : [family_data['bpm']['index'][61]]},

            #Sector 08
            prefix + '08M1'   : {'bpm' : [family_data['bpm']['index'][62]]},
            prefix + '08M2'   : {'bpm' : [family_data['bpm']['index'][63]]},
            prefix + '08C1-A' : {'bpm' : [family_data['bpm']['index'][64]]},
            prefix + '08C1-B' : {'bpm' : [family_data['bpm']['index'][65]]},
            prefix + '08C2-A' : {'bpm' : [family_data['bpm']['index'][66]]},
            prefix + '08C2-B' : {'bpm' : [family_data['bpm']['index'][67]]},
            prefix + '08C4'   : {'bpm' : [family_data['bpm']['index'][68]]},
            prefix + '08C5-A' : {'bpm' : [family_data['bpm']['index'][69]]},
            prefix + '08C5-B' : {'bpm' : [family_data['bpm']['index'][70]]},

            #Sector 09
            prefix + '09M1'   : {'bpm' : [family_data['bpm']['index'][71]]},
            prefix + '09M2'   : {'bpm' : [family_data['bpm']['index'][72]]},
            prefix + '09C1-A' : {'bpm' : [family_data['bpm']['index'][73]]},
            prefix + '09C1-B' : {'bpm' : [family_data['bpm']['index'][74]]},
            prefix + '09C2-A' : {'bpm' : [family_data['bpm']['index'][75]]},
            prefix + '09C2-B' : {'bpm' : [family_data['bpm']['index'][76]]},
            prefix + '09C4'   : {'bpm' : [family_data['bpm']['index'][77]]},
            prefix + '09C5-A' : {'bpm' : [family_data['bpm']['index'][78]]},
            prefix + '09C5-B' : {'bpm' : [family_data['bpm']['index'][79]]},

            #Sector 10
            prefix + '10M1'   : {'bpm' : [family_data['bpm']['index'][80]]},
            prefix + '10M2'   : {'bpm' : [family_data['bpm']['index'][81]]},
            prefix + '10C1-A' : {'bpm' : [family_data['bpm']['index'][82]]},
            prefix + '10C1-B' : {'bpm' : [family_data['bpm']['index'][83]]},
            prefix + '10C2-A' : {'bpm' : [family_data['bpm']['index'][84]]},
            prefix + '10C2-B' : {'bpm' : [family_data['bpm']['index'][85]]},
            prefix + '10C4'   : {'bpm' : [family_data['bpm']['index'][86]]},
            prefix + '10C5-A' : {'bpm' : [family_data['bpm']['index'][87]]},
            prefix + '10C5-B' : {'bpm' : [family_data['bpm']['index'][88]]},

            #Sector 11
            prefix + '11M1'   : {'bpm' : [family_data['bpm']['index'][89]]},
            prefix + '11M2'   : {'bpm' : [family_data['bpm']['index'][90]]},
            prefix + '11C1-A' : {'bpm' : [family_data['bpm']['index'][91]]},
            prefix + '11C1-B' : {'bpm' : [family_data['bpm']['index'][92]]},
            prefix + '11C2-A' : {'bpm' : [family_data['bpm']['index'][93]]},
            prefix + '11C2-B' : {'bpm' : [family_data['bpm']['index'][94]]},
            prefix + '11C4'   : {'bpm' : [family_data['bpm']['index'][95]]},
            prefix + '11C5-A' : {'bpm' : [family_data['bpm']['index'][96]]},
            prefix + '11C5-B' : {'bpm' : [family_data['bpm']['index'][97]]},

            #Sector 12
            prefix + '12M1'   : {'bpm' : [family_data['bpm']['index'][98]]},
            prefix + '12M2'   : {'bpm' : [family_data['bpm']['index'][99]]},
            prefix + '12C1-A' : {'bpm' : [family_data['bpm']['index'][100]]},
            prefix + '12C1-B' : {'bpm' : [family_data['bpm']['index'][101]]},
            prefix + '12C2-A' : {'bpm' : [family_data['bpm']['index'][102]]},
            prefix + '12C2-B' : {'bpm' : [family_data['bpm']['index'][103]]},
            prefix + '12C4'   : {'bpm' : [family_data['bpm']['index'][104]]},
            prefix + '12C5-A' : {'bpm' : [family_data['bpm']['index'][105]]},
            prefix + '12C5-B' : {'bpm' : [family_data['bpm']['index'][106]]},

            #Sector 13
            prefix + '13M1'   : {'bpm' : [family_data['bpm']['index'][107]]},
            prefix + '13M2'   : {'bpm' : [family_data['bpm']['index'][108]]},
            prefix + '13C1-A' : {'bpm' : [family_data['bpm']['index'][109]]},
            prefix + '13C1-B' : {'bpm' : [family_data['bpm']['index'][110]]},
            prefix + '13C2-A' : {'bpm' : [family_data['bpm']['index'][111]]},
            prefix + '13C2-B' : {'bpm' : [family_data['bpm']['index'][112]]},
            prefix + '13C4'   : {'bpm' : [family_data['bpm']['index'][113]]},
            prefix + '13C5-A' : {'bpm' : [family_data['bpm']['index'][114]]},
            prefix + '13C5-B' : {'bpm' : [family_data['bpm']['index'][115]]},

            #Sector 14
            prefix + '14M1'   : {'bpm' : [family_data['bpm']['index'][116]]},
            prefix + '14M2'   : {'bpm' : [family_data['bpm']['index'][117]]},
            prefix + '14C1-A' : {'bpm' : [family_data['bpm']['index'][118]]},
            prefix + '14C1-B' : {'bpm' : [family_data['bpm']['index'][119]]},
            prefix + '14C2-A' : {'bpm' : [family_data['bpm']['index'][120]]},
            prefix + '14C2-B' : {'bpm' : [family_data['bpm']['index'][121]]},
            prefix + '14C4'   : {'bpm' : [family_data['bpm']['index'][122]]},
            prefix + '14C5-A' : {'bpm' : [family_data['bpm']['index'][123]]},
            prefix + '14C5-B' : {'bpm' : [family_data['bpm']['index'][124]]},

            #Sector 15
            prefix + '15M1'   : {'bpm' : [family_data['bpm']['index'][125]]},
            prefix + '15M2'   : {'bpm' : [family_data['bpm']['index'][126]]},
            prefix + '15C1-A' : {'bpm' : [family_data['bpm']['index'][127]]},
            prefix + '15C1-B' : {'bpm' : [family_data['bpm']['index'][128]]},
            prefix + '15C2-A' : {'bpm' : [family_data['bpm']['index'][129]]},
            prefix + '15C2-B' : {'bpm' : [family_data['bpm']['index'][130]]},
            prefix + '15C4'   : {'bpm' : [family_data['bpm']['index'][131]]},
            prefix + '15C5-A' : {'bpm' : [family_data['bpm']['index'][132]]},
            prefix + '15C5-B' : {'bpm' : [family_data['bpm']['index'][133]]},

            #Sector 16
            prefix + '16M1'   : {'bpm' : [family_data['bpm']['index'][134]]},
            prefix + '16M2'   : {'bpm' : [family_data['bpm']['index'][135]]},
            prefix + '16C1-A' : {'bpm' : [family_data['bpm']['index'][136]]},
            prefix + '16C1-B' : {'bpm' : [family_data['bpm']['index'][137]]},
            prefix + '16C2-A' : {'bpm' : [family_data['bpm']['index'][138]]},
            prefix + '16C2-B' : {'bpm' : [family_data['bpm']['index'][139]]},
            prefix + '16C4'   : {'bpm' : [family_data['bpm']['index'][140]]},
            prefix + '16C5-A' : {'bpm' : [family_data['bpm']['index'][141]]},
            prefix + '16C5-B' : {'bpm' : [family_data['bpm']['index'][142]]},

            #Sector 17
            prefix + '17M1'   : {'bpm' : [family_data['bpm']['index'][143]]},
            prefix + '17M2'   : {'bpm' : [family_data['bpm']['index'][144]]},
            prefix + '17C1-A' : {'bpm' : [family_data['bpm']['index'][145]]},
            prefix + '17C1-B' : {'bpm' : [family_data['bpm']['index'][146]]},
            prefix + '17C2-A' : {'bpm' : [family_data['bpm']['index'][147]]},
            prefix + '17C2-B' : {'bpm' : [family_data['bpm']['index'][148]]},
            prefix + '17C4'   : {'bpm' : [family_data['bpm']['index'][149]]},
            prefix + '17C5-A' : {'bpm' : [family_data['bpm']['index'][150]]},
            prefix + '17C5-B' : {'bpm' : [family_data['bpm']['index'][151]]},

            #Sector 18
            prefix + '18M1'   : {'bpm' : [family_data['bpm']['index'][152]]},
            prefix + '18M2'   : {'bpm' : [family_data['bpm']['index'][153]]},
            prefix + '18C1-A' : {'bpm' : [family_data['bpm']['index'][154]]},
            prefix + '18C1-B' : {'bpm' : [family_data['bpm']['index'][155]]},
            prefix + '18C2-A' : {'bpm' : [family_data['bpm']['index'][156]]},
            prefix + '18C2-B' : {'bpm' : [family_data['bpm']['index'][157]]},
            prefix + '18C4'   : {'bpm' : [family_data['bpm']['index'][158]]},
            prefix + '18C5-A' : {'bpm' : [family_data['bpm']['index'][159]]},
            prefix + '18C5-B' : {'bpm' : [family_data['bpm']['index'][160]]},

            #Sector 19
            prefix + '19M1'   : {'bpm' : [family_data['bpm']['index'][161]]},
            prefix + '19M2'   : {'bpm' : [family_data['bpm']['index'][162]]},
            prefix + '19C1-A' : {'bpm' : [family_data['bpm']['index'][163]]},
            prefix + '19C1-B' : {'bpm' : [family_data['bpm']['index'][164]]},
            prefix + '19C2-A' : {'bpm' : [family_data['bpm']['index'][165]]},
            prefix + '19C2-B' : {'bpm' : [family_data['bpm']['index'][166]]},
            prefix + '19C4'   : {'bpm' : [family_data['bpm']['index'][167]]},
            prefix + '19C5-A' : {'bpm' : [family_data['bpm']['index'][168]]},
            prefix + '19C5-B' : {'bpm' : [family_data['bpm']['index'][169]]},

            #Sector 20
            prefix + '20M1'   : {'bpm' : [family_data['bpm']['index'][170]]},
            prefix + '20M2'   : {'bpm' : [family_data['bpm']['index'][171]]},
            prefix + '20C1-A' : {'bpm' : [family_data['bpm']['index'][172]]},
            prefix + '20C1-B' : {'bpm' : [family_data['bpm']['index'][173]]},
            prefix + '20C2-A' : {'bpm' : [family_data['bpm']['index'][174]]},
            prefix + '20C2-B' : {'bpm' : [family_data['bpm']['index'][175]]},
            prefix + '20C4'   : {'bpm' : [family_data['bpm']['index'][176]]},
            prefix + '20C5-A' : {'bpm' : [family_data['bpm']['index'][177]]},
            prefix + '20C5-B' : {'bpm' : [family_data['bpm']['index'][178]]},

        }
        return _dict

    if element.lower() == 'qs':
        prefix = prefix + 'QS-'
        _dict = {
            #Sector 1
            prefix + '01M1'   : {'qs' : [family_data['qs']['index'][79]]},
            prefix + '01M2'   : {'qs' : [family_data['qs']['index'][0]]},
            prefix + '01C1'   : {'qs' : [family_data['qs']['index'][1]]},
            prefix + '01C5'   : {'qs' : [family_data['qs']['index'][2]]},

            #Sector 2
            prefix + '02M1'   : {'qs' : [family_data['qs']['index'][3]]},
            prefix + '02M2'   : {'qs' : [family_data['qs']['index'][4]]},
            prefix + '02C1'   : {'qs' : [family_data['qs']['index'][5]]},
            prefix + '02C5'   : {'qs' : [family_data['qs']['index'][6]]},

            #Sector 3
            prefix + '03M1'   : {'qs' : [family_data['qs']['index'][7]]},
            prefix + '03M2'   : {'qs' : [family_data['qs']['index'][8]]},
            prefix + '03C1'   : {'qs' : [family_data['qs']['index'][9]]},
            prefix + '03C5'   : {'qs' : [family_data['qs']['index'][10]]},

            #Sector 4
            prefix + '04M1'   : {'qs' : [family_data['qs']['index'][11]]},
            prefix + '04M2'   : {'qs' : [family_data['qs']['index'][12]]},
            prefix + '04C1'   : {'qs' : [family_data['qs']['index'][13]]},
            prefix + '04C5'   : {'qs' : [family_data['qs']['index'][14]]},

            #Sector 5
            prefix + '05M1'   : {'qs' : [family_data['qs']['index'][15]]},
            prefix + '05M2'   : {'qs' : [family_data['qs']['index'][16]]},
            prefix + '05C1'   : {'qs' : [family_data['qs']['index'][17]]},
            prefix + '05C5'   : {'qs' : [family_data['qs']['index'][18]]},

            #Sector 6
            prefix + '06M1'   : {'qs' : [family_data['qs']['index'][19]]},
            prefix + '06M2'   : {'qs' : [family_data['qs']['index'][20]]},
            prefix + '06C1'   : {'qs' : [family_data['qs']['index'][21]]},
            prefix + '06C5'   : {'qs' : [family_data['qs']['index'][22]]},

            #Sector 7
            prefix + '07M1'   : {'qs' : [family_data['qs']['index'][23]]},
            prefix + '07M2'   : {'qs' : [family_data['qs']['index'][24]]},
            prefix + '07C1'   : {'qs' : [family_data['qs']['index'][25]]},
            prefix + '07C5'   : {'qs' : [family_data['qs']['index'][26]]},

            #Sector 8
            prefix + '08M1'   : {'qs' : [family_data['qs']['index'][27]]},
            prefix + '08M2'   : {'qs' : [family_data['qs']['index'][28]]},
            prefix + '08C1'   : {'qs' : [family_data['qs']['index'][29]]},
            prefix + '08C5'   : {'qs' : [family_data['qs']['index'][30]]},

            #Sector 9
            prefix + '09M1'   : {'qs' : [family_data['qs']['index'][31]]},
            prefix + '09M2'   : {'qs' : [family_data['qs']['index'][32]]},
            prefix + '09C1'   : {'qs' : [family_data['qs']['index'][33]]},
            prefix + '09C5'   : {'qs' : [family_data['qs']['index'][34]]},

            #Sector 10
            prefix + '10M1'   : {'qs' : [family_data['qs']['index'][35]]},
            prefix + '10M2'   : {'qs' : [family_data['qs']['index'][36]]},
            prefix + '10C1'   : {'qs' : [family_data['qs']['index'][37]]},
            prefix + '10C5'   : {'qs' : [family_data['qs']['index'][38]]},

            #Sector 11
            prefix + '11M1'   : {'qs' : [family_data['qs']['index'][39]]},
            prefix + '11M2'   : {'qs' : [family_data['qs']['index'][40]]},
            prefix + '11C1'   : {'qs' : [family_data['qs']['index'][41]]},
            prefix + '11C5'   : {'qs' : [family_data['qs']['index'][42]]},

            #Sector 12
            prefix + '12M1'   : {'qs' : [family_data['qs']['index'][43]]},
            prefix + '12M2'   : {'qs' : [family_data['qs']['index'][44]]},
            prefix + '12C1'   : {'qs' : [family_data['qs']['index'][45]]},
            prefix + '12C5'   : {'qs' : [family_data['qs']['index'][46]]},

            #Sector 13
            prefix + '13M1'   : {'qs' : [family_data['qs']['index'][47]]},
            prefix + '13M2'   : {'qs' : [family_data['qs']['index'][48]]},
            prefix + '13C1'   : {'qs' : [family_data['qs']['index'][49]]},
            prefix + '13C5'   : {'qs' : [family_data['qs']['index'][50]]},

            #Sector 14
            prefix + '14M1'   : {'qs' : [family_data['qs']['index'][51]]},
            prefix + '14M2'   : {'qs' : [family_data['qs']['index'][52]]},
            prefix + '14C1'   : {'qs' : [family_data['qs']['index'][53]]},
            prefix + '14C5'   : {'qs' : [family_data['qs']['index'][54]]},

            #Sector 15
            prefix + '15M1'   : {'qs' : [family_data['qs']['index'][55]]},
            prefix + '15M2'   : {'qs' : [family_data['qs']['index'][56]]},
            prefix + '15C1'   : {'qs' : [family_data['qs']['index'][57]]},
            prefix + '15C5'   : {'qs' : [family_data['qs']['index'][58]]},

            #Sector 16
            prefix + '16M1'   : {'qs' : [family_data['qs']['index'][59]]},
            prefix + '16M2'   : {'qs' : [family_data['qs']['index'][60]]},
            prefix + '16C1'   : {'qs' : [family_data['qs']['index'][61]]},
            prefix + '16C5'   : {'qs' : [family_data['qs']['index'][62]]},

            #Sector 17
            prefix + '17M1'   : {'qs' : [family_data['qs']['index'][63]]},
            prefix + '17M2'   : {'qs' : [family_data['qs']['index'][64]]},
            prefix + '17C1'   : {'qs' : [family_data['qs']['index'][65]]},
            prefix + '17C5'   : {'qs' : [family_data['qs']['index'][66]]},

            #Sector 18
            prefix + '18M1'   : {'qs' : [family_data['qs']['index'][67]]},
            prefix + '18M2'   : {'qs' : [family_data['qs']['index'][68]]},
            prefix + '18C1'   : {'qs' : [family_data['qs']['index'][69]]},
            prefix + '18C5'   : {'qs' : [family_data['qs']['index'][70]]},

            #Sector 19
            prefix + '19M1'   : {'qs' : [family_data['qs']['index'][71]]},
            prefix + '19M2'   : {'qs' : [family_data['qs']['index'][72]]},
            prefix + '19C1'   : {'qs' : [family_data['qs']['index'][73]]},
            prefix + '19C5'   : {'qs' : [family_data['qs']['index'][74]]},

            #Sector 20
            prefix + '20M1'   : {'qs' : [family_data['qs']['index'][75]]},
            prefix + '20M2'   : {'qs' : [family_data['qs']['index'][76]]},
            prefix + '20C1'   : {'qs' : [family_data['qs']['index'][77]]},
            prefix + '20C5'   : {'qs' : [family_data['qs']['index'][78]]},
        }
        return _dict

    if element.lower() == 'b1':
        prefix = prefix + 'B1-'
        _dict = {
            prefix + '01-A'   : {'b1' : [family_data['b1']['index'][0]]},
            prefix + '01-B'   : {'b1' : [family_data['b1']['index'][1]]},
            prefix + '02-A'   : {'b1' : [family_data['b1']['index'][2]]},
            prefix + '02-B'   : {'b1' : [family_data['b1']['index'][3]]},
            prefix + '03-A'   : {'b1' : [family_data['b1']['index'][4]]},
            prefix + '03-B'   : {'b1' : [family_data['b1']['index'][5]]},
            prefix + '04-A'   : {'b1' : [family_data['b1']['index'][6]]},
            prefix + '04-B'   : {'b1' : [family_data['b1']['index'][7]]},
            prefix + '05-A'   : {'b1' : [family_data['b1']['index'][8]]},
            prefix + '05-B'   : {'b1' : [family_data['b1']['index'][9]]},
            prefix + '06-A'   : {'b1' : [family_data['b1']['index'][10]]},
            prefix + '06-B'   : {'b1' : [family_data['b1']['index'][11]]},
            prefix + '07-A'   : {'b1' : [family_data['b1']['index'][12]]},
            prefix + '07-B'   : {'b1' : [family_data['b1']['index'][13]]},
            prefix + '08-A'   : {'b1' : [family_data['b1']['index'][14]]},
            prefix + '08-B'   : {'b1' : [family_data['b1']['index'][15]]},
            prefix + '09-A'   : {'b1' : [family_data['b1']['index'][16]]},
            prefix + '09-B'   : {'b1' : [family_data['b1']['index'][17]]},
            prefix + '10-A'   : {'b1' : [family_data['b1']['index'][18]]},
            prefix + '10-B'   : {'b1' : [family_data['b1']['index'][19]]},
            prefix + '11-A'   : {'b1' : [family_data['b1']['index'][20]]},
            prefix + '11-B'   : {'b1' : [family_data['b1']['index'][21]]},
            prefix + '12-A'   : {'b1' : [family_data['b1']['index'][22]]},
            prefix + '12-B'   : {'b1' : [family_data['b1']['index'][23]]},
            prefix + '13-A'   : {'b1' : [family_data['b1']['index'][24]]},
            prefix + '13-B'   : {'b1' : [family_data['b1']['index'][25]]},
            prefix + '14-A'   : {'b1' : [family_data['b1']['index'][26]]},
            prefix + '14-B'   : {'b1' : [family_data['b1']['index'][27]]},
            prefix + '15-A'   : {'b1' : [family_data['b1']['index'][28]]},
            prefix + '15-B'   : {'b1' : [family_data['b1']['index'][29]]},
            prefix + '16-A'   : {'b1' : [family_data['b1']['index'][30]]},
            prefix + '16-B'   : {'b1' : [family_data['b1']['index'][31]]},
            prefix + '17-A'   : {'b1' : [family_data['b1']['index'][32]]},
            prefix + '17-B'   : {'b1' : [family_data['b1']['index'][33]]},
            prefix + '18-A'   : {'b1' : [family_data['b1']['index'][34]]},
            prefix + '18-B'   : {'b1' : [family_data['b1']['index'][35]]},
            prefix + '19-A'   : {'b1' : [family_data['b1']['index'][36]]},
            prefix + '19-B'   : {'b1' : [family_data['b1']['index'][37]]},
            prefix + '20-A'   : {'b1' : [family_data['b1']['index'][38]]},
            prefix + '20-B'   : {'b1' : [family_data['b1']['index'][39]]},
        }
        return _dict

    if element.lower() == 'b2':
        prefix = prefix + 'B2-'
        _dict = {
            prefix + '01-A'   : {'b2' : [family_data['b2']['index'][0]]},
            prefix + '01-B'   : {'b2' : [family_data['b2']['index'][1]]},
            prefix + '02-A'   : {'b2' : [family_data['b2']['index'][2]]},
            prefix + '02-B'   : {'b2' : [family_data['b2']['index'][3]]},
            prefix + '03-A'   : {'b2' : [family_data['b2']['index'][4]]},
            prefix + '03-B'   : {'b2' : [family_data['b2']['index'][5]]},
            prefix + '04-A'   : {'b2' : [family_data['b2']['index'][6]]},
            prefix + '04-B'   : {'b2' : [family_data['b2']['index'][7]]},
            prefix + '05-A'   : {'b2' : [family_data['b2']['index'][8]]},
            prefix + '05-B'   : {'b2' : [family_data['b2']['index'][9]]},
            prefix + '06-A'   : {'b2' : [family_data['b2']['index'][10]]},
            prefix + '06-B'   : {'b2' : [family_data['b2']['index'][11]]},
            prefix + '07-A'   : {'b2' : [family_data['b2']['index'][12]]},
            prefix + '07-B'   : {'b2' : [family_data['b2']['index'][13]]},
            prefix + '08-A'   : {'b2' : [family_data['b2']['index'][14]]},
            prefix + '08-B'   : {'b2' : [family_data['b2']['index'][15]]},
            prefix + '09-A'   : {'b2' : [family_data['b2']['index'][16]]},
            prefix + '09-B'   : {'b2' : [family_data['b2']['index'][17]]},
            prefix + '10-A'   : {'b2' : [family_data['b2']['index'][18]]},
            prefix + '10-B'   : {'b2' : [family_data['b2']['index'][19]]},
            prefix + '11-A'   : {'b2' : [family_data['b2']['index'][20]]},
            prefix + '11-B'   : {'b2' : [family_data['b2']['index'][21]]},
            prefix + '12-A'   : {'b2' : [family_data['b2']['index'][22]]},
            prefix + '12-B'   : {'b2' : [family_data['b2']['index'][23]]},
            prefix + '13-A'   : {'b2' : [family_data['b2']['index'][24]]},
            prefix + '13-B'   : {'b2' : [family_data['b2']['index'][25]]},
            prefix + '14-A'   : {'b2' : [family_data['b2']['index'][26]]},
            prefix + '14-B'   : {'b2' : [family_data['b2']['index'][27]]},
            prefix + '15-A'   : {'b2' : [family_data['b2']['index'][28]]},
            prefix + '15-B'   : {'b2' : [family_data['b2']['index'][29]]},
            prefix + '16-A'   : {'b2' : [family_data['b2']['index'][30]]},
            prefix + '16-B'   : {'b2' : [family_data['b2']['index'][31]]},
            prefix + '17-A'   : {'b2' : [family_data['b2']['index'][32]]},
            prefix + '17-B'   : {'b2' : [family_data['b2']['index'][33]]},
            prefix + '18-A'   : {'b2' : [family_data['b2']['index'][34]]},
            prefix + '18-B'   : {'b2' : [family_data['b2']['index'][35]]},
            prefix + '19-A'   : {'b2' : [family_data['b2']['index'][36]]},
            prefix + '19-B'   : {'b2' : [family_data['b2']['index'][37]]},
            prefix + '20-A'   : {'b2' : [family_data['b2']['index'][38]]},
            prefix + '20-B'   : {'b2' : [family_data['b2']['index'][39]]},
        }
        return _dict

    if element.lower() == 'b3':
        prefix = prefix + 'B3-'
        _dict = {
            prefix + '01-A'   : {'b3' : [family_data['b3']['index'][0]]},
            prefix + '01-B'   : {'b3' : [family_data['b3']['index'][1]]},
            prefix + '02-A'   : {'b3' : [family_data['b3']['index'][2]]},
            prefix + '02-B'   : {'b3' : [family_data['b3']['index'][3]]},
            prefix + '03-A'   : {'b3' : [family_data['b3']['index'][4]]},
            prefix + '03-B'   : {'b3' : [family_data['b3']['index'][5]]},
            prefix + '04-A'   : {'b3' : [family_data['b3']['index'][6]]},
            prefix + '04-B'   : {'b3' : [family_data['b3']['index'][7]]},
            prefix + '05-A'   : {'b3' : [family_data['b3']['index'][8]]},
            prefix + '05-B'   : {'b3' : [family_data['b3']['index'][9]]},
            prefix + '06-A'   : {'b3' : [family_data['b3']['index'][10]]},
            prefix + '06-B'   : {'b3' : [family_data['b3']['index'][11]]},
            prefix + '07-A'   : {'b3' : [family_data['b3']['index'][12]]},
            prefix + '07-B'   : {'b3' : [family_data['b3']['index'][13]]},
            prefix + '08-A'   : {'b3' : [family_data['b3']['index'][14]]},
            prefix + '08-B'   : {'b3' : [family_data['b3']['index'][15]]},
            prefix + '09-A'   : {'b3' : [family_data['b3']['index'][16]]},
            prefix + '09-B'   : {'b3' : [family_data['b3']['index'][17]]},
            prefix + '10-A'   : {'b3' : [family_data['b3']['index'][18]]},
            prefix + '10-B'   : {'b3' : [family_data['b3']['index'][19]]},
            prefix + '11-A'   : {'b3' : [family_data['b3']['index'][20]]},
            prefix + '11-B'   : {'b3' : [family_data['b3']['index'][21]]},
            prefix + '12-A'   : {'b3' : [family_data['b3']['index'][22]]},
            prefix + '12-B'   : {'b3' : [family_data['b3']['index'][23]]},
            prefix + '13-A'   : {'b3' : [family_data['b3']['index'][24]]},
            prefix + '13-B'   : {'b3' : [family_data['b3']['index'][25]]},
            prefix + '14-A'   : {'b3' : [family_data['b3']['index'][26]]},
            prefix + '14-B'   : {'b3' : [family_data['b3']['index'][27]]},
            prefix + '15-A'   : {'b3' : [family_data['b3']['index'][28]]},
            prefix + '15-B'   : {'b3' : [family_data['b3']['index'][29]]},
            prefix + '16-A'   : {'b3' : [family_data['b3']['index'][30]]},
            prefix + '16-B'   : {'b3' : [family_data['b3']['index'][31]]},
            prefix + '17-A'   : {'b3' : [family_data['b3']['index'][32]]},
            prefix + '17-B'   : {'b3' : [family_data['b3']['index'][33]]},
            prefix + '18-A'   : {'b3' : [family_data['b3']['index'][34]]},
            prefix + '18-B'   : {'b3' : [family_data['b3']['index'][35]]},
            prefix + '19-A'   : {'b3' : [family_data['b3']['index'][36]]},
            prefix + '19-B'   : {'b3' : [family_data['b3']['index'][37]]},
            prefix + '20-A'   : {'b3' : [family_data['b3']['index'][38]]},
            prefix + '20-B'   : {'b3' : [family_data['b3']['index'][39]]},
        }
        return _dict

    if element.lower() == 'bc':
        prefix = prefix + 'BC-'
        _dict = {
            prefix + '01'   : {'bc' : [family_data['bc']['index'][0]]},
            prefix + '02'   : {'bc' : [family_data['bc']['index'][1]]},
            prefix + '03'   : {'bc' : [family_data['bc']['index'][2]]},
            prefix + '04'   : {'bc' : [family_data['bc']['index'][3]]},
            prefix + '05'   : {'bc' : [family_data['bc']['index'][4]]},
            prefix + '06'   : {'bc' : [family_data['bc']['index'][5]]},
            prefix + '07'   : {'bc' : [family_data['bc']['index'][6]]},
            prefix + '08'   : {'bc' : [family_data['bc']['index'][7]]},
            prefix + '09'   : {'bc' : [family_data['bc']['index'][8]]},
            prefix + '10'   : {'bc' : [family_data['bc']['index'][9]]},
            prefix + '11'   : {'bc' : [family_data['bc']['index'][10]]},
            prefix + '12'   : {'bc' : [family_data['bc']['index'][11]]},
            prefix + '13'   : {'bc' : [family_data['bc']['index'][12]]},
            prefix + '14'   : {'bc' : [family_data['bc']['index'][13]]},
            prefix + '15'   : {'bc' : [family_data['bc']['index'][14]]},
            prefix + '16'   : {'bc' : [family_data['bc']['index'][15]]},
            prefix + '17'   : {'bc' : [family_data['bc']['index'][16]]},
            prefix + '18'   : {'bc' : [family_data['bc']['index'][17]]},
            prefix + '19'   : {'bc' : [family_data['bc']['index'][18]]},
            prefix + '20'   : {'bc' : [family_data['bc']['index'][19]]},
        }
        return _dict

    if element.lower() == 'chs':
        prefix = prefix + 'CHS-'
        _dict = {
            #Sector 1
            prefix + '01M1'   : {'chs' : [family_data['chs']['index'][159]]},
            prefix + '01M2'   : {'chs' : [family_data['chs']['index'][0]]},
            prefix + '01C1-A' : {'chs' : [family_data['chs']['index'][1]]},
            prefix + '01C1-B' : {'chs' : [family_data['chs']['index'][2]]},
            prefix + '01C2'   : {'chs' : [family_data['chs']['index'][3]]},
            prefix + '01C4'   : {'chs' : [family_data['chs']['index'][4]]},
            prefix + '01C5-A' : {'chs' : [family_data['chs']['index'][5]]},
            prefix + '01C5-B' : {'chs' : [family_data['chs']['index'][6]]},

            #Sector 2
            prefix + '02M1'   : {'chs' : [family_data['chs']['index'][7]]},
            prefix + '02M2'   : {'chs' : [family_data['chs']['index'][8]]},
            prefix + '02C1-A' : {'chs' : [family_data['chs']['index'][9]]},
            prefix + '02C1-B' : {'chs' : [family_data['chs']['index'][10]]},
            prefix + '02C2'   : {'chs' : [family_data['chs']['index'][11]]},
            prefix + '02C4'   : {'chs' : [family_data['chs']['index'][12]]},
            prefix + '02C5-A' : {'chs' : [family_data['chs']['index'][13]]},
            prefix + '02C5-B' : {'chs' : [family_data['chs']['index'][14]]},

            #Sector 3
            prefix + '03M1'   : {'chs' : [family_data['chs']['index'][15]]},
            prefix + '03M2'   : {'chs' : [family_data['chs']['index'][16]]},
            prefix + '03C1-A' : {'chs' : [family_data['chs']['index'][17]]},
            prefix + '03C1-B' : {'chs' : [family_data['chs']['index'][18]]},
            prefix + '03C2'   : {'chs' : [family_data['chs']['index'][19]]},
            prefix + '03C4'   : {'chs' : [family_data['chs']['index'][20]]},
            prefix + '03C5-A' : {'chs' : [family_data['chs']['index'][21]]},
            prefix + '03C5-B' : {'chs' : [family_data['chs']['index'][22]]},

            #Sector 4
            prefix + '04M1'   : {'chs' : [family_data['chs']['index'][23]]},
            prefix + '04M2'   : {'chs' : [family_data['chs']['index'][24]]},
            prefix + '04C1-A' : {'chs' : [family_data['chs']['index'][25]]},
            prefix + '04C1-B' : {'chs' : [family_data['chs']['index'][26]]},
            prefix + '04C2'   : {'chs' : [family_data['chs']['index'][27]]},
            prefix + '04C4'   : {'chs' : [family_data['chs']['index'][28]]},
            prefix + '04C5-A' : {'chs' : [family_data['chs']['index'][29]]},
            prefix + '04C5-B' : {'chs' : [family_data['chs']['index'][30]]},

            #Sector 5
            prefix + '05M1'   : {'chs' : [family_data['chs']['index'][31]]},
            prefix + '05M2'   : {'chs' : [family_data['chs']['index'][32]]},
            prefix + '05C1-A' : {'chs' : [family_data['chs']['index'][33]]},
            prefix + '05C1-B' : {'chs' : [family_data['chs']['index'][34]]},
            prefix + '05C2'   : {'chs' : [family_data['chs']['index'][35]]},
            prefix + '05C4'   : {'chs' : [family_data['chs']['index'][36]]},
            prefix + '05C5-A' : {'chs' : [family_data['chs']['index'][37]]},
            prefix + '05C5-B' : {'chs' : [family_data['chs']['index'][38]]},

            #Sector 6
            prefix + '06M1'   : {'chs' : [family_data['chs']['index'][39]]},
            prefix + '06M2'   : {'chs' : [family_data['chs']['index'][40]]},
            prefix + '06C1-A' : {'chs' : [family_data['chs']['index'][41]]},
            prefix + '06C1-B' : {'chs' : [family_data['chs']['index'][42]]},
            prefix + '06C2'   : {'chs' : [family_data['chs']['index'][43]]},
            prefix + '06C4'   : {'chs' : [family_data['chs']['index'][44]]},
            prefix + '06C5-A' : {'chs' : [family_data['chs']['index'][45]]},
            prefix + '06C5-B' : {'chs' : [family_data['chs']['index'][46]]},

            #Sector 7
            prefix + '07M1'   : {'chs' : [family_data['chs']['index'][47]]},
            prefix + '07M2'   : {'chs' : [family_data['chs']['index'][48]]},
            prefix + '07C1-A' : {'chs' : [family_data['chs']['index'][49]]},
            prefix + '07C1-B' : {'chs' : [family_data['chs']['index'][50]]},
            prefix + '07C2'   : {'chs' : [family_data['chs']['index'][51]]},
            prefix + '07C4'   : {'chs' : [family_data['chs']['index'][52]]},
            prefix + '07C5-A' : {'chs' : [family_data['chs']['index'][53]]},
            prefix + '07C5-B' : {'chs' : [family_data['chs']['index'][54]]},

            #Sector 8
            prefix + '08M1'   : {'chs' : [family_data['chs']['index'][55]]},
            prefix + '08M2'   : {'chs' : [family_data['chs']['index'][56]]},
            prefix + '08C1-A' : {'chs' : [family_data['chs']['index'][57]]},
            prefix + '08C1-B' : {'chs' : [family_data['chs']['index'][58]]},
            prefix + '08C2'   : {'chs' : [family_data['chs']['index'][59]]},
            prefix + '08C4'   : {'chs' : [family_data['chs']['index'][60]]},
            prefix + '08C5-A' : {'chs' : [family_data['chs']['index'][61]]},
            prefix + '08C5-B' : {'chs' : [family_data['chs']['index'][62]]},

            #Sector 9
            prefix + '09M1'   : {'chs' : [family_data['chs']['index'][63]]},
            prefix + '09M2'   : {'chs' : [family_data['chs']['index'][64]]},
            prefix + '09C1-A' : {'chs' : [family_data['chs']['index'][65]]},
            prefix + '09C1-B' : {'chs' : [family_data['chs']['index'][66]]},
            prefix + '09C2'   : {'chs' : [family_data['chs']['index'][67]]},
            prefix + '09C4'   : {'chs' : [family_data['chs']['index'][68]]},
            prefix + '09C5-A' : {'chs' : [family_data['chs']['index'][69]]},
            prefix + '09C5-B' : {'chs' : [family_data['chs']['index'][70]]},

            #Sector 10
            prefix + '10M1'   : {'chs' : [family_data['chs']['index'][71]]},
            prefix + '10M2'   : {'chs' : [family_data['chs']['index'][72]]},
            prefix + '10C1-A' : {'chs' : [family_data['chs']['index'][73]]},
            prefix + '10C1-B' : {'chs' : [family_data['chs']['index'][74]]},
            prefix + '10C2'   : {'chs' : [family_data['chs']['index'][75]]},
            prefix + '10C4'   : {'chs' : [family_data['chs']['index'][76]]},
            prefix + '10C5-A' : {'chs' : [family_data['chs']['index'][77]]},
            prefix + '10C5-B' : {'chs' : [family_data['chs']['index'][78]]},

            #Sector 11
            prefix + '11M1'   : {'chs' : [family_data['chs']['index'][79]]},
            prefix + '11M2'   : {'chs' : [family_data['chs']['index'][80]]},
            prefix + '11C1-A' : {'chs' : [family_data['chs']['index'][81]]},
            prefix + '11C1-B' : {'chs' : [family_data['chs']['index'][82]]},
            prefix + '11C2'   : {'chs' : [family_data['chs']['index'][83]]},
            prefix + '11C4'   : {'chs' : [family_data['chs']['index'][84]]},
            prefix + '11C5-A' : {'chs' : [family_data['chs']['index'][85]]},
            prefix + '11C5-B' : {'chs' : [family_data['chs']['index'][86]]},

            #Sector 12
            prefix + '12M1'   : {'chs' : [family_data['chs']['index'][87]]},
            prefix + '12M2'   : {'chs' : [family_data['chs']['index'][88]]},
            prefix + '12C1-A' : {'chs' : [family_data['chs']['index'][89]]},
            prefix + '12C1-B' : {'chs' : [family_data['chs']['index'][90]]},
            prefix + '12C2'   : {'chs' : [family_data['chs']['index'][91]]},
            prefix + '12C4'   : {'chs' : [family_data['chs']['index'][92]]},
            prefix + '12C5-A' : {'chs' : [family_data['chs']['index'][93]]},
            prefix + '12C5-B' : {'chs' : [family_data['chs']['index'][94]]},

            #Sector 13
            prefix + '13M1'   : {'chs' : [family_data['chs']['index'][95]]},
            prefix + '13M2'   : {'chs' : [family_data['chs']['index'][96]]},
            prefix + '13C1-A' : {'chs' : [family_data['chs']['index'][97]]},
            prefix + '13C1-B' : {'chs' : [family_data['chs']['index'][98]]},
            prefix + '13C2'   : {'chs' : [family_data['chs']['index'][99]]},
            prefix + '13C4'   : {'chs' : [family_data['chs']['index'][100]]},
            prefix + '13C5-A' : {'chs' : [family_data['chs']['index'][101]]},
            prefix + '13C5-B' : {'chs' : [family_data['chs']['index'][102]]},

            #Sector 14
            prefix + '14M1'   : {'chs' : [family_data['chs']['index'][103]]},
            prefix + '14M2'   : {'chs' : [family_data['chs']['index'][104]]},
            prefix + '14C1-A' : {'chs' : [family_data['chs']['index'][105]]},
            prefix + '14C1-B' : {'chs' : [family_data['chs']['index'][106]]},
            prefix + '14C2'   : {'chs' : [family_data['chs']['index'][107]]},
            prefix + '14C4'   : {'chs' : [family_data['chs']['index'][108]]},
            prefix + '14C5-A' : {'chs' : [family_data['chs']['index'][109]]},
            prefix + '14C5-B' : {'chs' : [family_data['chs']['index'][110]]},

            #Sector 15
            prefix + '15M1'   : {'chs' : [family_data['chs']['index'][111]]},
            prefix + '15M2'   : {'chs' : [family_data['chs']['index'][112]]},
            prefix + '15C1-A' : {'chs' : [family_data['chs']['index'][113]]},
            prefix + '15C1-B' : {'chs' : [family_data['chs']['index'][114]]},
            prefix + '15C2'   : {'chs' : [family_data['chs']['index'][115]]},
            prefix + '15C4'   : {'chs' : [family_data['chs']['index'][116]]},
            prefix + '15C5-A' : {'chs' : [family_data['chs']['index'][117]]},
            prefix + '15C5-B' : {'chs' : [family_data['chs']['index'][118]]},

            #Sector 16
            prefix + '16M1'   : {'chs' : [family_data['chs']['index'][119]]},
            prefix + '16M2'   : {'chs' : [family_data['chs']['index'][120]]},
            prefix + '16C1-A' : {'chs' : [family_data['chs']['index'][121]]},
            prefix + '16C1-B' : {'chs' : [family_data['chs']['index'][122]]},
            prefix + '16C2'   : {'chs' : [family_data['chs']['index'][123]]},
            prefix + '16C4'   : {'chs' : [family_data['chs']['index'][124]]},
            prefix + '16C5-A' : {'chs' : [family_data['chs']['index'][125]]},
            prefix + '16C5-B' : {'chs' : [family_data['chs']['index'][126]]},

            #Sector 17
            prefix + '17M1'   : {'chs' : [family_data['chs']['index'][127]]},
            prefix + '17M2'   : {'chs' : [family_data['chs']['index'][128]]},
            prefix + '17C1-A' : {'chs' : [family_data['chs']['index'][129]]},
            prefix + '17C1-B' : {'chs' : [family_data['chs']['index'][130]]},
            prefix + '17C2'   : {'chs' : [family_data['chs']['index'][131]]},
            prefix + '17C4'   : {'chs' : [family_data['chs']['index'][132]]},
            prefix + '17C5-A' : {'chs' : [family_data['chs']['index'][133]]},
            prefix + '17C5-B' : {'chs' : [family_data['chs']['index'][134]]},

            #Sector 18
            prefix + '18M1'   : {'chs' : [family_data['chs']['index'][135]]},
            prefix + '18M2'   : {'chs' : [family_data['chs']['index'][136]]},
            prefix + '18C1-A' : {'chs' : [family_data['chs']['index'][137]]},
            prefix + '18C1-B' : {'chs' : [family_data['chs']['index'][138]]},
            prefix + '18C2'   : {'chs' : [family_data['chs']['index'][139]]},
            prefix + '18C4'   : {'chs' : [family_data['chs']['index'][140]]},
            prefix + '18C5-A' : {'chs' : [family_data['chs']['index'][141]]},
            prefix + '18C5-B' : {'chs' : [family_data['chs']['index'][142]]},

            #Sector 19
            prefix + '19M1'   : {'chs' : [family_data['chs']['index'][143]]},
            prefix + '19M2'   : {'chs' : [family_data['chs']['index'][144]]},
            prefix + '19C1-A' : {'chs' : [family_data['chs']['index'][145]]},
            prefix + '19C1-B' : {'chs' : [family_data['chs']['index'][146]]},
            prefix + '19C2'   : {'chs' : [family_data['chs']['index'][147]]},
            prefix + '19C4'   : {'chs' : [family_data['chs']['index'][148]]},
            prefix + '19C5-A' : {'chs' : [family_data['chs']['index'][149]]},
            prefix + '19C5-B' : {'chs' : [family_data['chs']['index'][150]]},

            #Sector 20
            prefix + '20M1'   : {'chs' : [family_data['chs']['index'][151]]},
            prefix + '20M2'   : {'chs' : [family_data['chs']['index'][152]]},
            prefix + '20C1-A' : {'chs' : [family_data['chs']['index'][153]]},
            prefix + '20C1-B' : {'chs' : [family_data['chs']['index'][154]]},
            prefix + '20C2'   : {'chs' : [family_data['chs']['index'][155]]},
            prefix + '20C4'   : {'chs' : [family_data['chs']['index'][156]]},
            prefix + '20C5-A' : {'chs' : [family_data['chs']['index'][157]]},
            prefix + '20C5-B' : {'chs' : [family_data['chs']['index'][158]]},
        }
        return _dict

    if element.lower() == 'cvs':
        prefix = prefix + 'CVS-'
        _dict = {
            #Sector 1
            prefix + '01M1'   : {'cvs' : [family_data['cvs']['index'][119]]},
            prefix + '01M2'   : {'cvs' : [family_data['cvs']['index'][0]]},
            prefix + '01C1'   : {'cvs' : [family_data['cvs']['index'][1]]},
            prefix + '01C2'   : {'cvs' : [family_data['cvs']['index'][2]]},
            prefix + '01C4'   : {'cvs' : [family_data['cvs']['index'][3]]},
            prefix + '01C5'   : {'cvs' : [family_data['cvs']['index'][4]]},

            #Sector 2
            prefix + '02M1'   : {'cvs' : [family_data['cvs']['index'][5]]},
            prefix + '02M2'   : {'cvs' : [family_data['cvs']['index'][6]]},
            prefix + '02C1'   : {'cvs' : [family_data['cvs']['index'][7]]},
            prefix + '02C2'   : {'cvs' : [family_data['cvs']['index'][8]]},
            prefix + '02C4'   : {'cvs' : [family_data['cvs']['index'][9]]},
            prefix + '02C5'   : {'cvs' : [family_data['cvs']['index'][10]]},

            #Sector 3
            prefix + '03M1'   : {'cvs' : [family_data['cvs']['index'][11]]},
            prefix + '03M2'   : {'cvs' : [family_data['cvs']['index'][12]]},
            prefix + '03C1'   : {'cvs' : [family_data['cvs']['index'][13]]},
            prefix + '03C2'   : {'cvs' : [family_data['cvs']['index'][14]]},
            prefix + '03C4'   : {'cvs' : [family_data['cvs']['index'][15]]},
            prefix + '03C5'   : {'cvs' : [family_data['cvs']['index'][16]]},

            #Sector 4
            prefix + '04M1'   : {'cvs' : [family_data['cvs']['index'][17]]},
            prefix + '04M2'   : {'cvs' : [family_data['cvs']['index'][18]]},
            prefix + '04C1'   : {'cvs' : [family_data['cvs']['index'][19]]},
            prefix + '04C2'   : {'cvs' : [family_data['cvs']['index'][20]]},
            prefix + '04C4'   : {'cvs' : [family_data['cvs']['index'][21]]},
            prefix + '04C5'   : {'cvs' : [family_data['cvs']['index'][22]]},

            #Sector 5
            prefix + '05M1'   : {'cvs' : [family_data['cvs']['index'][23]]},
            prefix + '05M2'   : {'cvs' : [family_data['cvs']['index'][24]]},
            prefix + '05C1'   : {'cvs' : [family_data['cvs']['index'][25]]},
            prefix + '05C2'   : {'cvs' : [family_data['cvs']['index'][26]]},
            prefix + '05C4'   : {'cvs' : [family_data['cvs']['index'][27]]},
            prefix + '05C5'   : {'cvs' : [family_data['cvs']['index'][28]]},

            #Sector 6
            prefix + '06M1'   : {'cvs' : [family_data['cvs']['index'][29]]},
            prefix + '06M2'   : {'cvs' : [family_data['cvs']['index'][30]]},
            prefix + '06C1'   : {'cvs' : [family_data['cvs']['index'][31]]},
            prefix + '06C2'   : {'cvs' : [family_data['cvs']['index'][32]]},
            prefix + '06C4'   : {'cvs' : [family_data['cvs']['index'][33]]},
            prefix + '06C5'   : {'cvs' : [family_data['cvs']['index'][34]]},

            #Sector 7
            prefix + '07M1'   : {'cvs' : [family_data['cvs']['index'][35]]},
            prefix + '07M2'   : {'cvs' : [family_data['cvs']['index'][36]]},
            prefix + '07C1'   : {'cvs' : [family_data['cvs']['index'][37]]},
            prefix + '07C2'   : {'cvs' : [family_data['cvs']['index'][38]]},
            prefix + '07C4'   : {'cvs' : [family_data['cvs']['index'][39]]},
            prefix + '07C5'   : {'cvs' : [family_data['cvs']['index'][40]]},

            #Sector 8
            prefix + '08M1'   : {'cvs' : [family_data['cvs']['index'][41]]},
            prefix + '08M2'   : {'cvs' : [family_data['cvs']['index'][42]]},
            prefix + '08C1'   : {'cvs' : [family_data['cvs']['index'][43]]},
            prefix + '08C2'   : {'cvs' : [family_data['cvs']['index'][44]]},
            prefix + '08C4'   : {'cvs' : [family_data['cvs']['index'][45]]},
            prefix + '08C5'   : {'cvs' : [family_data['cvs']['index'][46]]},

            #Sector 9
            prefix + '09M1'   : {'cvs' : [family_data['cvs']['index'][47]]},
            prefix + '09M2'   : {'cvs' : [family_data['cvs']['index'][48]]},
            prefix + '09C1'   : {'cvs' : [family_data['cvs']['index'][49]]},
            prefix + '09C2'   : {'cvs' : [family_data['cvs']['index'][50]]},
            prefix + '09C4'   : {'cvs' : [family_data['cvs']['index'][51]]},
            prefix + '09C5'   : {'cvs' : [family_data['cvs']['index'][52]]},

            #Sector 10
            prefix + '10M1'   : {'cvs' : [family_data['cvs']['index'][53]]},
            prefix + '10M2'   : {'cvs' : [family_data['cvs']['index'][54]]},
            prefix + '10C1'   : {'cvs' : [family_data['cvs']['index'][55]]},
            prefix + '10C2'   : {'cvs' : [family_data['cvs']['index'][56]]},
            prefix + '10C4'   : {'cvs' : [family_data['cvs']['index'][57]]},
            prefix + '10C5'   : {'cvs' : [family_data['cvs']['index'][58]]},

            #Sector 11
            prefix + '11M1'   : {'cvs' : [family_data['cvs']['index'][59]]},
            prefix + '11M2'   : {'cvs' : [family_data['cvs']['index'][60]]},
            prefix + '11C1'   : {'cvs' : [family_data['cvs']['index'][61]]},
            prefix + '11C2'   : {'cvs' : [family_data['cvs']['index'][62]]},
            prefix + '11C4'   : {'cvs' : [family_data['cvs']['index'][63]]},
            prefix + '11C5'   : {'cvs' : [family_data['cvs']['index'][64]]},

            #Sector 12
            prefix + '12M1'   : {'cvs' : [family_data['cvs']['index'][65]]},
            prefix + '12M2'   : {'cvs' : [family_data['cvs']['index'][66]]},
            prefix + '12C1'   : {'cvs' : [family_data['cvs']['index'][67]]},
            prefix + '12C2'   : {'cvs' : [family_data['cvs']['index'][68]]},
            prefix + '12C4'   : {'cvs' : [family_data['cvs']['index'][69]]},
            prefix + '12C5'   : {'cvs' : [family_data['cvs']['index'][70]]},

            #Sector 13
            prefix + '13M1'   : {'cvs' : [family_data['cvs']['index'][71]]},
            prefix + '13M2'   : {'cvs' : [family_data['cvs']['index'][72]]},
            prefix + '13C1'   : {'cvs' : [family_data['cvs']['index'][73]]},
            prefix + '13C2'   : {'cvs' : [family_data['cvs']['index'][74]]},
            prefix + '13C4'   : {'cvs' : [family_data['cvs']['index'][75]]},
            prefix + '13C5'   : {'cvs' : [family_data['cvs']['index'][76]]},

            #Sector 14
            prefix + '14M1'   : {'cvs' : [family_data['cvs']['index'][77]]},
            prefix + '14M2'   : {'cvs' : [family_data['cvs']['index'][78]]},
            prefix + '14C1'   : {'cvs' : [family_data['cvs']['index'][79]]},
            prefix + '14C2'   : {'cvs' : [family_data['cvs']['index'][80]]},
            prefix + '14C4'   : {'cvs' : [family_data['cvs']['index'][81]]},
            prefix + '14C5'   : {'cvs' : [family_data['cvs']['index'][82]]},

            #Sector 15
            prefix + '15M1'   : {'cvs' : [family_data['cvs']['index'][83]]},
            prefix + '15M2'   : {'cvs' : [family_data['cvs']['index'][84]]},
            prefix + '15C1'   : {'cvs' : [family_data['cvs']['index'][85]]},
            prefix + '15C2'   : {'cvs' : [family_data['cvs']['index'][86]]},
            prefix + '15C4'   : {'cvs' : [family_data['cvs']['index'][87]]},
            prefix + '15C5'   : {'cvs' : [family_data['cvs']['index'][88]]},

            #Sector 16
            prefix + '16M1'   : {'cvs' : [family_data['cvs']['index'][89]]},
            prefix + '16M2'   : {'cvs' : [family_data['cvs']['index'][90]]},
            prefix + '16C1'   : {'cvs' : [family_data['cvs']['index'][91]]},
            prefix + '16C2'   : {'cvs' : [family_data['cvs']['index'][92]]},
            prefix + '16C4'   : {'cvs' : [family_data['cvs']['index'][93]]},
            prefix + '16C5'   : {'cvs' : [family_data['cvs']['index'][94]]},

            #Sector 17
            prefix + '17M1'   : {'cvs' : [family_data['cvs']['index'][95]]},
            prefix + '17M2'   : {'cvs' : [family_data['cvs']['index'][96]]},
            prefix + '17C1'   : {'cvs' : [family_data['cvs']['index'][97]]},
            prefix + '17C2'   : {'cvs' : [family_data['cvs']['index'][98]]},
            prefix + '17C4'   : {'cvs' : [family_data['cvs']['index'][99]]},
            prefix + '17C5'   : {'cvs' : [family_data['cvs']['index'][100]]},

            #Sector 18
            prefix + '18M1'   : {'cvs' : [family_data['cvs']['index'][101]]},
            prefix + '18M2'   : {'cvs' : [family_data['cvs']['index'][102]]},
            prefix + '18C1'   : {'cvs' : [family_data['cvs']['index'][103]]},
            prefix + '18C2'   : {'cvs' : [family_data['cvs']['index'][104]]},
            prefix + '18C4'   : {'cvs' : [family_data['cvs']['index'][105]]},
            prefix + '18C5'   : {'cvs' : [family_data['cvs']['index'][106]]},

            #Sector 19
            prefix + '19M1'   : {'cvs' : [family_data['cvs']['index'][107]]},
            prefix + '19M2'   : {'cvs' : [family_data['cvs']['index'][108]]},
            prefix + '19C1'   : {'cvs' : [family_data['cvs']['index'][109]]},
            prefix + '19C2'   : {'cvs' : [family_data['cvs']['index'][110]]},
            prefix + '19C4'   : {'cvs' : [family_data['cvs']['index'][111]]},
            prefix + '19C5'   : {'cvs' : [family_data['cvs']['index'][112]]},

            #Sector 20
            prefix + '20M1'   : {'cvs' : [family_data['cvs']['index'][113]]},
            prefix + '20M2'   : {'cvs' : [family_data['cvs']['index'][114]]},
            prefix + '20C1'   : {'cvs' : [family_data['cvs']['index'][115]]},
            prefix + '20C2'   : {'cvs' : [family_data['cvs']['index'][116]]},
            prefix + '20C4'   : {'cvs' : [family_data['cvs']['index'][117]]},
            prefix + '20C5'   : {'cvs' : [family_data['cvs']['index'][118]]},
        }
        return _dict

    if element.lower() == 'chf':
        prefix = prefix + 'CHF-'
        _dict = {
            #Sector 1
            prefix + '01M1'   : {'chf' : [family_data['chf']['index'][79]]},
            prefix + '01M2'   : {'chf' : [family_data['chf']['index'][0]]},
            prefix + '01C2'   : {'chf' : [family_data['chf']['index'][1]]},
            prefix + '01C4'   : {'chf' : [family_data['chf']['index'][2]]},

            #Sector 2
            prefix + '02M1'   : {'chf' : [family_data['chf']['index'][3]]},
            prefix + '02M2'   : {'chf' : [family_data['chf']['index'][4]]},
            prefix + '02C2'   : {'chf' : [family_data['chf']['index'][5]]},
            prefix + '02C4'   : {'chf' : [family_data['chf']['index'][6]]},

            #Sector 3
            prefix + '03M1'   : {'chf' : [family_data['chf']['index'][7]]},
            prefix + '03M2'   : {'chf' : [family_data['chf']['index'][8]]},
            prefix + '03C2'   : {'chf' : [family_data['chf']['index'][9]]},
            prefix + '03C4'   : {'chf' : [family_data['chf']['index'][10]]},

            #Sector 4
            prefix + '04M1'   : {'chf' : [family_data['chf']['index'][11]]},
            prefix + '04M2'   : {'chf' : [family_data['chf']['index'][12]]},
            prefix + '04C2'   : {'chf' : [family_data['chf']['index'][13]]},
            prefix + '04C4'   : {'chf' : [family_data['chf']['index'][14]]},

            #Sector 5
            prefix + '05M1'   : {'chf' : [family_data['chf']['index'][15]]},
            prefix + '05M2'   : {'chf' : [family_data['chf']['index'][16]]},
            prefix + '05C2'   : {'chf' : [family_data['chf']['index'][17]]},
            prefix + '05C4'   : {'chf' : [family_data['chf']['index'][18]]},

            #Sector 6
            prefix + '06M1'   : {'chf' : [family_data['chf']['index'][19]]},
            prefix + '06M2'   : {'chf' : [family_data['chf']['index'][20]]},
            prefix + '06C2'   : {'chf' : [family_data['chf']['index'][21]]},
            prefix + '06C4'   : {'chf' : [family_data['chf']['index'][22]]},

            #Sector 7
            prefix + '07M1'   : {'chf' : [family_data['chf']['index'][23]]},
            prefix + '07M2'   : {'chf' : [family_data['chf']['index'][24]]},
            prefix + '07C2'   : {'chf' : [family_data['chf']['index'][25]]},
            prefix + '07C4'   : {'chf' : [family_data['chf']['index'][26]]},

            #Sector 8
            prefix + '08M1'   : {'chf' : [family_data['chf']['index'][27]]},
            prefix + '08M2'   : {'chf' : [family_data['chf']['index'][28]]},
            prefix + '08C2'   : {'chf' : [family_data['chf']['index'][29]]},
            prefix + '08C4'   : {'chf' : [family_data['chf']['index'][30]]},

            #Sector 9
            prefix + '09M1'   : {'chf' : [family_data['chf']['index'][31]]},
            prefix + '09M2'   : {'chf' : [family_data['chf']['index'][32]]},
            prefix + '09C2'   : {'chf' : [family_data['chf']['index'][33]]},
            prefix + '09C4'   : {'chf' : [family_data['chf']['index'][34]]},

            #Sector 10
            prefix + '10M1'   : {'chf' : [family_data['chf']['index'][35]]},
            prefix + '10M2'   : {'chf' : [family_data['chf']['index'][36]]},
            prefix + '10C2'   : {'chf' : [family_data['chf']['index'][37]]},
            prefix + '10C4'   : {'chf' : [family_data['chf']['index'][38]]},

            #Sector 11
            prefix + '11M1'   : {'chf' : [family_data['chf']['index'][39]]},
            prefix + '11M2'   : {'chf' : [family_data['chf']['index'][40]]},
            prefix + '11C2'   : {'chf' : [family_data['chf']['index'][41]]},
            prefix + '11C4'   : {'chf' : [family_data['chf']['index'][42]]},

            #Sector 12
            prefix + '12M1'   : {'chf' : [family_data['chf']['index'][43]]},
            prefix + '12M2'   : {'chf' : [family_data['chf']['index'][44]]},
            prefix + '12C2'   : {'chf' : [family_data['chf']['index'][45]]},
            prefix + '12C4'   : {'chf' : [family_data['chf']['index'][46]]},

            #Sector 13
            prefix + '13M1'   : {'chf' : [family_data['chf']['index'][47]]},
            prefix + '13M2'   : {'chf' : [family_data['chf']['index'][48]]},
            prefix + '13C2'   : {'chf' : [family_data['chf']['index'][49]]},
            prefix + '13C4'   : {'chf' : [family_data['chf']['index'][50]]},

            #Sector 14
            prefix + '14M1'   : {'chf' : [family_data['chf']['index'][51]]},
            prefix + '14M2'   : {'chf' : [family_data['chf']['index'][52]]},
            prefix + '14C2'   : {'chf' : [family_data['chf']['index'][53]]},
            prefix + '14C4'   : {'chf' : [family_data['chf']['index'][54]]},

            #Sector 15
            prefix + '15M1'   : {'chf' : [family_data['chf']['index'][55]]},
            prefix + '15M2'   : {'chf' : [family_data['chf']['index'][56]]},
            prefix + '15C2'   : {'chf' : [family_data['chf']['index'][57]]},
            prefix + '15C4'   : {'chf' : [family_data['chf']['index'][58]]},

            #Sector 16
            prefix + '16M1'   : {'chf' : [family_data['chf']['index'][59]]},
            prefix + '16M2'   : {'chf' : [family_data['chf']['index'][60]]},
            prefix + '16C2'   : {'chf' : [family_data['chf']['index'][61]]},
            prefix + '16C4'   : {'chf' : [family_data['chf']['index'][62]]},

            #Sector 17
            prefix + '17M1'   : {'chf' : [family_data['chf']['index'][63]]},
            prefix + '17M2'   : {'chf' : [family_data['chf']['index'][64]]},
            prefix + '17C2'   : {'chf' : [family_data['chf']['index'][65]]},
            prefix + '17C4'   : {'chf' : [family_data['chf']['index'][66]]},

            #Sector 18
            prefix + '18M1'   : {'chf' : [family_data['chf']['index'][67]]},
            prefix + '18M2'   : {'chf' : [family_data['chf']['index'][68]]},
            prefix + '18C2'   : {'chf' : [family_data['chf']['index'][69]]},
            prefix + '18C4'   : {'chf' : [family_data['chf']['index'][70]]},

            #Sector 19
            prefix + '19M1'   : {'chf' : [family_data['chf']['index'][71]]},
            prefix + '19M2'   : {'chf' : [family_data['chf']['index'][72]]},
            prefix + '19C2'   : {'chf' : [family_data['chf']['index'][73]]},
            prefix + '19C4'   : {'chf' : [family_data['chf']['index'][74]]},

            #Sector 20
            prefix + '20M1'   : {'chf' : [family_data['chf']['index'][75]]},
            prefix + '20M2'   : {'chf' : [family_data['chf']['index'][76]]},
            prefix + '20C2'   : {'chf' : [family_data['chf']['index'][77]]},
            prefix + '20C4'   : {'chf' : [family_data['chf']['index'][78]]},
        }
        return _dict

    if element.lower() == 'cvf':
        prefix = prefix + 'CVF-'
        _dict = {
            #Sector 1
            prefix + '01M1'   : {'cvf' : [family_data['cvf']['index'][79]]},
            prefix + '01M2'   : {'cvf' : [family_data['cvf']['index'][0]]},
            prefix + '01C2'   : {'cvf' : [family_data['cvf']['index'][1]]},
            prefix + '01C4'   : {'cvf' : [family_data['cvf']['index'][2]]},

            #Sector 2
            prefix + '02M1'   : {'cvf' : [family_data['cvf']['index'][3]]},
            prefix + '02M2'   : {'cvf' : [family_data['cvf']['index'][4]]},
            prefix + '02C2'   : {'cvf' : [family_data['cvf']['index'][5]]},
            prefix + '02C4'   : {'cvf' : [family_data['cvf']['index'][6]]},

            #Sector 3
            prefix + '03M1'   : {'cvf' : [family_data['cvf']['index'][7]]},
            prefix + '03M2'   : {'cvf' : [family_data['cvf']['index'][8]]},
            prefix + '03C2'   : {'cvf' : [family_data['cvf']['index'][9]]},
            prefix + '03C4'   : {'cvf' : [family_data['cvf']['index'][10]]},

            #Sector 4
            prefix + '04M1'   : {'cvf' : [family_data['cvf']['index'][11]]},
            prefix + '04M2'   : {'cvf' : [family_data['cvf']['index'][12]]},
            prefix + '04C2'   : {'cvf' : [family_data['cvf']['index'][13]]},
            prefix + '04C4'   : {'cvf' : [family_data['cvf']['index'][14]]},

            #Sector 5
            prefix + '05M1'   : {'cvf' : [family_data['cvf']['index'][15]]},
            prefix + '05M2'   : {'cvf' : [family_data['cvf']['index'][16]]},
            prefix + '05C2'   : {'cvf' : [family_data['cvf']['index'][17]]},
            prefix + '05C4'   : {'cvf' : [family_data['cvf']['index'][18]]},

            #Sector 6
            prefix + '06M1'   : {'cvf' : [family_data['cvf']['index'][19]]},
            prefix + '06M2'   : {'cvf' : [family_data['cvf']['index'][20]]},
            prefix + '06C2'   : {'cvf' : [family_data['cvf']['index'][21]]},
            prefix + '06C4'   : {'cvf' : [family_data['cvf']['index'][22]]},

            #Sector 7
            prefix + '07M1'   : {'cvf' : [family_data['cvf']['index'][23]]},
            prefix + '07M2'   : {'cvf' : [family_data['cvf']['index'][24]]},
            prefix + '07C2'   : {'cvf' : [family_data['cvf']['index'][25]]},
            prefix + '07C4'   : {'cvf' : [family_data['cvf']['index'][26]]},

            #Sector 8
            prefix + '08M1'   : {'cvf' : [family_data['cvf']['index'][27]]},
            prefix + '08M2'   : {'cvf' : [family_data['cvf']['index'][28]]},
            prefix + '08C2'   : {'cvf' : [family_data['cvf']['index'][29]]},
            prefix + '08C4'   : {'cvf' : [family_data['cvf']['index'][30]]},

            #Sector 9
            prefix + '09M1'   : {'cvf' : [family_data['cvf']['index'][31]]},
            prefix + '09M2'   : {'cvf' : [family_data['cvf']['index'][32]]},
            prefix + '09C2'   : {'cvf' : [family_data['cvf']['index'][33]]},
            prefix + '09C4'   : {'cvf' : [family_data['cvf']['index'][34]]},

            #Sector 10
            prefix + '10M1'   : {'cvf' : [family_data['cvf']['index'][35]]},
            prefix + '10M2'   : {'cvf' : [family_data['cvf']['index'][36]]},
            prefix + '10C2'   : {'cvf' : [family_data['cvf']['index'][37]]},
            prefix + '10C4'   : {'cvf' : [family_data['cvf']['index'][38]]},

            #Sector 11
            prefix + '11M1'   : {'cvf' : [family_data['cvf']['index'][39]]},
            prefix + '11M2'   : {'cvf' : [family_data['cvf']['index'][40]]},
            prefix + '11C2'   : {'cvf' : [family_data['cvf']['index'][41]]},
            prefix + '11C4'   : {'cvf' : [family_data['cvf']['index'][42]]},

            #Sector 12
            prefix + '12M1'   : {'cvf' : [family_data['cvf']['index'][43]]},
            prefix + '12M2'   : {'cvf' : [family_data['cvf']['index'][44]]},
            prefix + '12C2'   : {'cvf' : [family_data['cvf']['index'][45]]},
            prefix + '12C4'   : {'cvf' : [family_data['cvf']['index'][46]]},

            #Sector 13
            prefix + '13M1'   : {'cvf' : [family_data['cvf']['index'][47]]},
            prefix + '13M2'   : {'cvf' : [family_data['cvf']['index'][48]]},
            prefix + '13C2'   : {'cvf' : [family_data['cvf']['index'][49]]},
            prefix + '13C4'   : {'cvf' : [family_data['cvf']['index'][50]]},

            #Sector 14
            prefix + '14M1'   : {'cvf' : [family_data['cvf']['index'][51]]},
            prefix + '14M2'   : {'cvf' : [family_data['cvf']['index'][52]]},
            prefix + '14C2'   : {'cvf' : [family_data['cvf']['index'][53]]},
            prefix + '14C4'   : {'cvf' : [family_data['cvf']['index'][54]]},

            #Sector 15
            prefix + '15M1'   : {'cvf' : [family_data['cvf']['index'][55]]},
            prefix + '15M2'   : {'cvf' : [family_data['cvf']['index'][56]]},
            prefix + '15C2'   : {'cvf' : [family_data['cvf']['index'][57]]},
            prefix + '15C4'   : {'cvf' : [family_data['cvf']['index'][58]]},

            #Sector 16
            prefix + '16M1'   : {'cvf' : [family_data['cvf']['index'][59]]},
            prefix + '16M2'   : {'cvf' : [family_data['cvf']['index'][60]]},
            prefix + '16C2'   : {'cvf' : [family_data['cvf']['index'][61]]},
            prefix + '16C4'   : {'cvf' : [family_data['cvf']['index'][62]]},

            #Sector 17
            prefix + '17M1'   : {'cvf' : [family_data['cvf']['index'][63]]},
            prefix + '17M2'   : {'cvf' : [family_data['cvf']['index'][64]]},
            prefix + '17C2'   : {'cvf' : [family_data['cvf']['index'][65]]},
            prefix + '17C4'   : {'cvf' : [family_data['cvf']['index'][66]]},

            #Sector 18
            prefix + '18M1'   : {'cvf' : [family_data['cvf']['index'][67]]},
            prefix + '18M2'   : {'cvf' : [family_data['cvf']['index'][68]]},
            prefix + '18C2'   : {'cvf' : [family_data['cvf']['index'][69]]},
            prefix + '18C4'   : {'cvf' : [family_data['cvf']['index'][70]]},

            #Sector 19
            prefix + '19M1'   : {'cvf' : [family_data['cvf']['index'][71]]},
            prefix + '19M2'   : {'cvf' : [family_data['cvf']['index'][72]]},
            prefix + '19C2'   : {'cvf' : [family_data['cvf']['index'][73]]},
            prefix + '19C4'   : {'cvf' : [family_data['cvf']['index'][74]]},

            #Sector 20
            prefix + '20M1'   : {'cvf' : [family_data['cvf']['index'][75]]},
            prefix + '20M2'   : {'cvf' : [family_data['cvf']['index'][76]]},
            prefix + '20C2'   : {'cvf' : [family_data['cvf']['index'][77]]},
            prefix + '20C4'   : {'cvf' : [family_data['cvf']['index'][78]]},
        }
        return _dict

    if element.lower() == 'sfa':
        prefix = prefix + 'SFA-'
        _dict = {
            prefix + '01M2'   : {'sfa' : [family_data['sfa']['index'][19]]},
            prefix + '02M2'   : {'sfa' : [family_data['sfa']['index'][0]]},
            prefix + '03M2'   : {'sfa' : [family_data['sfa']['index'][1]]},
            prefix + '04M2'   : {'sfa' : [family_data['sfa']['index'][2]]},
            prefix + '05M2'   : {'sfa' : [family_data['sfa']['index'][3]]},
            prefix + '06M2'   : {'sfa' : [family_data['sfa']['index'][4]]},
            prefix + '07M2'   : {'sfa' : [family_data['sfa']['index'][5]]},
            prefix + '08M2'   : {'sfa' : [family_data['sfa']['index'][6]]},
            prefix + '09M2'   : {'sfa' : [family_data['sfa']['index'][7]]},
            prefix + '10M2'   : {'sfa' : [family_data['sfa']['index'][8]]},
            prefix + '11M2'   : {'sfa' : [family_data['sfa']['index'][9]]},
            prefix + '12M2'   : {'sfa' : [family_data['sfa']['index'][10]]},
            prefix + '13M2'   : {'sfa' : [family_data['sfa']['index'][11]]},
            prefix + '14M2'   : {'sfa' : [family_data['sfa']['index'][12]]},
            prefix + '15M2'   : {'sfa' : [family_data['sfa']['index'][13]]},
            prefix + '16M2'   : {'sfa' : [family_data['sfa']['index'][14]]},
            prefix + '17M2'   : {'sfa' : [family_data['sfa']['index'][15]]},
            prefix + '18M2'   : {'sfa' : [family_data['sfa']['index'][16]]},
            prefix + '19M2'   : {'sfa' : [family_data['sfa']['index'][17]]},
            prefix + '20M2'   : {'sfa' : [family_data['sfa']['index'][18]]},
        }
        return _dict

    if element.lower() == 'qfa':
        prefix = prefix + 'QFA-'
        _dict = {
            prefix + '01M2'   : {'qfa' : [family_data['qfa']['index'][19]]},
            prefix + '02M2'   : {'qfa' : [family_data['qfa']['index'][0]]},
            prefix + '03M2'   : {'qfa' : [family_data['qfa']['index'][1]]},
            prefix + '04M2'   : {'qfa' : [family_data['qfa']['index'][2]]},
            prefix + '05M2'   : {'qfa' : [family_data['qfa']['index'][3]]},
            prefix + '06M2'   : {'qfa' : [family_data['qfa']['index'][4]]},
            prefix + '07M2'   : {'qfa' : [family_data['qfa']['index'][5]]},
            prefix + '08M2'   : {'qfa' : [family_data['qfa']['index'][6]]},
            prefix + '09M2'   : {'qfa' : [family_data['qfa']['index'][7]]},
            prefix + '10M2'   : {'qfa' : [family_data['qfa']['index'][8]]},
            prefix + '11M2'   : {'qfa' : [family_data['qfa']['index'][9]]},
            prefix + '12M2'   : {'qfa' : [family_data['qfa']['index'][10]]},
            prefix + '13M2'   : {'qfa' : [family_data['qfa']['index'][11]]},
            prefix + '14M2'   : {'qfa' : [family_data['qfa']['index'][12]]},
            prefix + '15M2'   : {'qfa' : [family_data['qfa']['index'][13]]},
            prefix + '16M2'   : {'qfa' : [family_data['qfa']['index'][14]]},
            prefix + '17M2'   : {'qfa' : [family_data['qfa']['index'][15]]},
            prefix + '18M2'   : {'qfa' : [family_data['qfa']['index'][16]]},
            prefix + '19M2'   : {'qfa' : [family_data['qfa']['index'][17]]},
            prefix + '20M2'   : {'qfa' : [family_data['qfa']['index'][18]]},
        }
        return _dict

    if element.lower() == 'qda':
        prefix = prefix + 'QDA-'
        _dict = {
            prefix + '01M2'   : {'qda' : [family_data['qda']['index'][19]]},
            prefix + '02M2'   : {'qda' : [family_data['qda']['index'][0]]},
            prefix + '03M2'   : {'qda' : [family_data['qda']['index'][1]]},
            prefix + '04M2'   : {'qda' : [family_data['qda']['index'][2]]},
            prefix + '05M2'   : {'qda' : [family_data['qda']['index'][3]]},
            prefix + '06M2'   : {'qda' : [family_data['qda']['index'][4]]},
            prefix + '07M2'   : {'qda' : [family_data['qda']['index'][5]]},
            prefix + '08M2'   : {'qda' : [family_data['qda']['index'][6]]},
            prefix + '09M2'   : {'qda' : [family_data['qda']['index'][7]]},
            prefix + '10M2'   : {'qda' : [family_data['qda']['index'][8]]},
            prefix + '11M2'   : {'qda' : [family_data['qda']['index'][9]]},
            prefix + '12M2'   : {'qda' : [family_data['qda']['index'][10]]},
            prefix + '13M2'   : {'qda' : [family_data['qda']['index'][11]]},
            prefix + '14M2'   : {'qda' : [family_data['qda']['index'][12]]},
            prefix + '15M2'   : {'qda' : [family_data['qda']['index'][13]]},
            prefix + '16M2'   : {'qda' : [family_data['qda']['index'][14]]},
            prefix + '17M2'   : {'qda' : [family_data['qda']['index'][15]]},
            prefix + '18M2'   : {'qda' : [family_data['qda']['index'][16]]},
            prefix + '19M2'   : {'qda' : [family_data['qda']['index'][17]]},
            prefix + '20M2'   : {'qda' : [family_data['qda']['index'][18]]},
        }
        return _dict

    if element.lower() == 'sda':
        prefix = prefix + 'SDA-'
        _dict = {
            prefix + '01M2'   : {'sda' : [family_data['sda']['index'][19]]},
            prefix + '02M2'   : {'sda' : [family_data['sda']['index'][0]]},
            prefix + '03M2'   : {'sda' : [family_data['sda']['index'][1]]},
            prefix + '04M2'   : {'sda' : [family_data['sda']['index'][2]]},
            prefix + '05M2'   : {'sda' : [family_data['sda']['index'][3]]},
            prefix + '06M2'   : {'sda' : [family_data['sda']['index'][4]]},
            prefix + '07M2'   : {'sda' : [family_data['sda']['index'][5]]},
            prefix + '08M2'   : {'sda' : [family_data['sda']['index'][6]]},
            prefix + '09M2'   : {'sda' : [family_data['sda']['index'][7]]},
            prefix + '10M2'   : {'sda' : [family_data['sda']['index'][8]]},
            prefix + '11M2'   : {'sda' : [family_data['sda']['index'][9]]},
            prefix + '12M2'   : {'sda' : [family_data['sda']['index'][10]]},
            prefix + '13M2'   : {'sda' : [family_data['sda']['index'][11]]},
            prefix + '14M2'   : {'sda' : [family_data['sda']['index'][12]]},
            prefix + '15M2'   : {'sda' : [family_data['sda']['index'][13]]},
            prefix + '16M2'   : {'sda' : [family_data['sda']['index'][14]]},
            prefix + '17M2'   : {'sda' : [family_data['sda']['index'][15]]},
            prefix + '18M2'   : {'sda' : [family_data['sda']['index'][16]]},
            prefix + '19M2'   : {'sda' : [family_data['sda']['index'][17]]},
            prefix + '20M2'   : {'sda' : [family_data['sda']['index'][18]]},
        }
        return _dict

    if element.lower() == 'sd1':
        prefix = prefix + 'SD1-'
        _dict = {
            prefix + '01C1'   : {'sd1' : [family_data['sd1']['index'][0]]},
            prefix + '02C1'   : {'sd1' : [family_data['sd1']['index'][1]]},
            prefix + '03C1'   : {'sd1' : [family_data['sd1']['index'][2]]},
            prefix + '04C1'   : {'sd1' : [family_data['sd1']['index'][3]]},
            prefix + '05C1'   : {'sd1' : [family_data['sd1']['index'][4]]},
            prefix + '06C1'   : {'sd1' : [family_data['sd1']['index'][5]]},
            prefix + '07C1'   : {'sd1' : [family_data['sd1']['index'][6]]},
            prefix + '08C1'   : {'sd1' : [family_data['sd1']['index'][7]]},
            prefix + '09C1'   : {'sd1' : [family_data['sd1']['index'][8]]},
            prefix + '10C1'   : {'sd1' : [family_data['sd1']['index'][9]]},
            prefix + '11C1'   : {'sd1' : [family_data['sd1']['index'][10]]},
            prefix + '12C1'   : {'sd1' : [family_data['sd1']['index'][11]]},
            prefix + '13C1'   : {'sd1' : [family_data['sd1']['index'][12]]},
            prefix + '14C1'   : {'sd1' : [family_data['sd1']['index'][13]]},
            prefix + '15C1'   : {'sd1' : [family_data['sd1']['index'][14]]},
            prefix + '16C1'   : {'sd1' : [family_data['sd1']['index'][15]]},
            prefix + '17C1'   : {'sd1' : [family_data['sd1']['index'][16]]},
            prefix + '18C1'   : {'sd1' : [family_data['sd1']['index'][17]]},
            prefix + '19C1'   : {'sd1' : [family_data['sd1']['index'][18]]},
            prefix + '20C1'   : {'sd1' : [family_data['sd1']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qf1':
        prefix = prefix + 'QF1-'
        _dict = {
            prefix + '01C1'   : {'qf1' : [family_data['qf1']['index'][0]]},
            prefix + '01C5'   : {'qf1' : [family_data['qf1']['index'][1]]},
            prefix + '02C1'   : {'qf1' : [family_data['qf1']['index'][2]]},
            prefix + '02C5'   : {'qf1' : [family_data['qf1']['index'][3]]},
            prefix + '03C1'   : {'qf1' : [family_data['qf1']['index'][4]]},
            prefix + '03C5'   : {'qf1' : [family_data['qf1']['index'][5]]},
            prefix + '04C1'   : {'qf1' : [family_data['qf1']['index'][6]]},
            prefix + '04C5'   : {'qf1' : [family_data['qf1']['index'][7]]},
            prefix + '05C1'   : {'qf1' : [family_data['qf1']['index'][8]]},
            prefix + '05C5'   : {'qf1' : [family_data['qf1']['index'][9]]},
            prefix + '06C1'   : {'qf1' : [family_data['qf1']['index'][10]]},
            prefix + '06C5'   : {'qf1' : [family_data['qf1']['index'][11]]},
            prefix + '07C1'   : {'qf1' : [family_data['qf1']['index'][12]]},
            prefix + '07C5'   : {'qf1' : [family_data['qf1']['index'][13]]},
            prefix + '08C1'   : {'qf1' : [family_data['qf1']['index'][14]]},
            prefix + '08C5'   : {'qf1' : [family_data['qf1']['index'][15]]},
            prefix + '09C1'   : {'qf1' : [family_data['qf1']['index'][16]]},
            prefix + '09C5'   : {'qf1' : [family_data['qf1']['index'][17]]},
            prefix + '10C1'   : {'qf1' : [family_data['qf1']['index'][18]]},
            prefix + '10C5'   : {'qf1' : [family_data['qf1']['index'][19]]},
            prefix + '11C1'   : {'qf1' : [family_data['qf1']['index'][20]]},
            prefix + '11C5'   : {'qf1' : [family_data['qf1']['index'][21]]},
            prefix + '12C1'   : {'qf1' : [family_data['qf1']['index'][22]]},
            prefix + '12C5'   : {'qf1' : [family_data['qf1']['index'][23]]},
            prefix + '13C1'   : {'qf1' : [family_data['qf1']['index'][24]]},
            prefix + '13C5'   : {'qf1' : [family_data['qf1']['index'][25]]},
            prefix + '14C1'   : {'qf1' : [family_data['qf1']['index'][26]]},
            prefix + '14C5'   : {'qf1' : [family_data['qf1']['index'][27]]},
            prefix + '15C1'   : {'qf1' : [family_data['qf1']['index'][28]]},
            prefix + '15C5'   : {'qf1' : [family_data['qf1']['index'][29]]},
            prefix + '16C1'   : {'qf1' : [family_data['qf1']['index'][30]]},
            prefix + '16C5'   : {'qf1' : [family_data['qf1']['index'][31]]},
            prefix + '17C1'   : {'qf1' : [family_data['qf1']['index'][32]]},
            prefix + '17C5'   : {'qf1' : [family_data['qf1']['index'][33]]},
            prefix + '18C1'   : {'qf1' : [family_data['qf1']['index'][34]]},
            prefix + '18C5'   : {'qf1' : [family_data['qf1']['index'][35]]},
            prefix + '19C1'   : {'qf1' : [family_data['qf1']['index'][36]]},
            prefix + '19C5'   : {'qf1' : [family_data['qf1']['index'][37]]},
            prefix + '20C1'   : {'qf1' : [family_data['qf1']['index'][38]]},
            prefix + '20C5'   : {'qf1' : [family_data['qf1']['index'][39]]},
        }
        return _dict

    if element.lower() == 'sf1':
        prefix = prefix + 'SF1-'
        _dict = {
            prefix + '01C1'   : {'sf1' : [family_data['sf1']['index'][0]]},
            prefix + '02C1'   : {'sf1' : [family_data['sf1']['index'][1]]},
            prefix + '03C1'   : {'sf1' : [family_data['sf1']['index'][2]]},
            prefix + '04C1'   : {'sf1' : [family_data['sf1']['index'][3]]},
            prefix + '05C1'   : {'sf1' : [family_data['sf1']['index'][4]]},
            prefix + '06C1'   : {'sf1' : [family_data['sf1']['index'][5]]},
            prefix + '07C1'   : {'sf1' : [family_data['sf1']['index'][6]]},
            prefix + '08C1'   : {'sf1' : [family_data['sf1']['index'][7]]},
            prefix + '09C1'   : {'sf1' : [family_data['sf1']['index'][8]]},
            prefix + '10C1'   : {'sf1' : [family_data['sf1']['index'][9]]},
            prefix + '11C1'   : {'sf1' : [family_data['sf1']['index'][10]]},
            prefix + '12C1'   : {'sf1' : [family_data['sf1']['index'][11]]},
            prefix + '13C1'   : {'sf1' : [family_data['sf1']['index'][12]]},
            prefix + '14C1'   : {'sf1' : [family_data['sf1']['index'][13]]},
            prefix + '15C1'   : {'sf1' : [family_data['sf1']['index'][14]]},
            prefix + '16C1'   : {'sf1' : [family_data['sf1']['index'][15]]},
            prefix + '17C1'   : {'sf1' : [family_data['sf1']['index'][16]]},
            prefix + '18C1'   : {'sf1' : [family_data['sf1']['index'][17]]},
            prefix + '19C1'   : {'sf1' : [family_data['sf1']['index'][18]]},
            prefix + '20C1'   : {'sf1' : [family_data['sf1']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qf2':
        prefix = prefix + 'QF2-'
        _dict = {
            prefix + '01C1'   : {'qf2' : [family_data['qf2']['index'][0]]},
            prefix + '01C5'   : {'qf2' : [family_data['qf2']['index'][1]]},
            prefix + '02C1'   : {'qf2' : [family_data['qf2']['index'][2]]},
            prefix + '02C5'   : {'qf2' : [family_data['qf2']['index'][3]]},
            prefix + '03C1'   : {'qf2' : [family_data['qf2']['index'][4]]},
            prefix + '03C5'   : {'qf2' : [family_data['qf2']['index'][5]]},
            prefix + '04C1'   : {'qf2' : [family_data['qf2']['index'][6]]},
            prefix + '04C5'   : {'qf2' : [family_data['qf2']['index'][7]]},
            prefix + '05C1'   : {'qf2' : [family_data['qf2']['index'][8]]},
            prefix + '05C5'   : {'qf2' : [family_data['qf2']['index'][9]]},
            prefix + '06C1'   : {'qf2' : [family_data['qf2']['index'][10]]},
            prefix + '06C5'   : {'qf2' : [family_data['qf2']['index'][11]]},
            prefix + '07C1'   : {'qf2' : [family_data['qf2']['index'][12]]},
            prefix + '07C5'   : {'qf2' : [family_data['qf2']['index'][13]]},
            prefix + '08C1'   : {'qf2' : [family_data['qf2']['index'][14]]},
            prefix + '08C5'   : {'qf2' : [family_data['qf2']['index'][15]]},
            prefix + '09C1'   : {'qf2' : [family_data['qf2']['index'][16]]},
            prefix + '09C5'   : {'qf2' : [family_data['qf2']['index'][17]]},
            prefix + '10C1'   : {'qf2' : [family_data['qf2']['index'][18]]},
            prefix + '10C5'   : {'qf2' : [family_data['qf2']['index'][19]]},
            prefix + '11C1'   : {'qf2' : [family_data['qf2']['index'][20]]},
            prefix + '11C5'   : {'qf2' : [family_data['qf2']['index'][21]]},
            prefix + '12C1'   : {'qf2' : [family_data['qf2']['index'][22]]},
            prefix + '12C5'   : {'qf2' : [family_data['qf2']['index'][23]]},
            prefix + '13C1'   : {'qf2' : [family_data['qf2']['index'][24]]},
            prefix + '13C5'   : {'qf2' : [family_data['qf2']['index'][25]]},
            prefix + '14C1'   : {'qf2' : [family_data['qf2']['index'][26]]},
            prefix + '14C5'   : {'qf2' : [family_data['qf2']['index'][27]]},
            prefix + '15C1'   : {'qf2' : [family_data['qf2']['index'][28]]},
            prefix + '15C5'   : {'qf2' : [family_data['qf2']['index'][29]]},
            prefix + '16C1'   : {'qf2' : [family_data['qf2']['index'][30]]},
            prefix + '16C5'   : {'qf2' : [family_data['qf2']['index'][31]]},
            prefix + '17C1'   : {'qf2' : [family_data['qf2']['index'][32]]},
            prefix + '17C5'   : {'qf2' : [family_data['qf2']['index'][33]]},
            prefix + '18C1'   : {'qf2' : [family_data['qf2']['index'][34]]},
            prefix + '18C5'   : {'qf2' : [family_data['qf2']['index'][35]]},
            prefix + '19C1'   : {'qf2' : [family_data['qf2']['index'][36]]},
            prefix + '19C5'   : {'qf2' : [family_data['qf2']['index'][37]]},
            prefix + '20C1'   : {'qf2' : [family_data['qf2']['index'][38]]},
            prefix + '20C5'   : {'qf2' : [family_data['qf2']['index'][39]]},
        }
        return _dict

    if element.lower() == 'sd2':
        prefix = prefix + 'SD2-'
        _dict = {
            prefix + '01C1'   : {'sd2' : [family_data['sd2']['index'][0]]},
            prefix + '02C1'   : {'sd2' : [family_data['sd2']['index'][1]]},
            prefix + '03C1'   : {'sd2' : [family_data['sd2']['index'][2]]},
            prefix + '04C1'   : {'sd2' : [family_data['sd2']['index'][3]]},
            prefix + '05C1'   : {'sd2' : [family_data['sd2']['index'][4]]},
            prefix + '06C1'   : {'sd2' : [family_data['sd2']['index'][5]]},
            prefix + '07C1'   : {'sd2' : [family_data['sd2']['index'][6]]},
            prefix + '08C1'   : {'sd2' : [family_data['sd2']['index'][7]]},
            prefix + '09C1'   : {'sd2' : [family_data['sd2']['index'][8]]},
            prefix + '10C1'   : {'sd2' : [family_data['sd2']['index'][9]]},
            prefix + '11C1'   : {'sd2' : [family_data['sd2']['index'][10]]},
            prefix + '12C1'   : {'sd2' : [family_data['sd2']['index'][11]]},
            prefix + '13C1'   : {'sd2' : [family_data['sd2']['index'][12]]},
            prefix + '14C1'   : {'sd2' : [family_data['sd2']['index'][13]]},
            prefix + '15C1'   : {'sd2' : [family_data['sd2']['index'][14]]},
            prefix + '16C1'   : {'sd2' : [family_data['sd2']['index'][15]]},
            prefix + '17C1'   : {'sd2' : [family_data['sd2']['index'][16]]},
            prefix + '18C1'   : {'sd2' : [family_data['sd2']['index'][17]]},
            prefix + '19C1'   : {'sd2' : [family_data['sd2']['index'][18]]},
            prefix + '20C1'   : {'sd2' : [family_data['sd2']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sd3':
        prefix = prefix + 'SD3-'
        _dict = {
            prefix + '01C2'   : {'sd3' : [family_data['sd3']['index'][0]]},
            prefix + '02C2'   : {'sd3' : [family_data['sd3']['index'][1]]},
            prefix + '03C2'   : {'sd3' : [family_data['sd3']['index'][2]]},
            prefix + '04C2'   : {'sd3' : [family_data['sd3']['index'][3]]},
            prefix + '05C2'   : {'sd3' : [family_data['sd3']['index'][4]]},
            prefix + '06C2'   : {'sd3' : [family_data['sd3']['index'][5]]},
            prefix + '07C2'   : {'sd3' : [family_data['sd3']['index'][6]]},
            prefix + '08C2'   : {'sd3' : [family_data['sd3']['index'][7]]},
            prefix + '09C2'   : {'sd3' : [family_data['sd3']['index'][8]]},
            prefix + '10C2'   : {'sd3' : [family_data['sd3']['index'][9]]},
            prefix + '11C2'   : {'sd3' : [family_data['sd3']['index'][10]]},
            prefix + '12C2'   : {'sd3' : [family_data['sd3']['index'][11]]},
            prefix + '13C2'   : {'sd3' : [family_data['sd3']['index'][12]]},
            prefix + '14C2'   : {'sd3' : [family_data['sd3']['index'][13]]},
            prefix + '15C2'   : {'sd3' : [family_data['sd3']['index'][14]]},
            prefix + '16C2'   : {'sd3' : [family_data['sd3']['index'][15]]},
            prefix + '17C2'   : {'sd3' : [family_data['sd3']['index'][16]]},
            prefix + '18C2'   : {'sd3' : [family_data['sd3']['index'][17]]},
            prefix + '19C2'   : {'sd3' : [family_data['sd3']['index'][18]]},
            prefix + '20C2'   : {'sd3' : [family_data['sd3']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qf3':
        prefix = prefix + 'QF3-'
        _dict = {
            prefix + '01C2'   : {'qf3' : [family_data['qf3']['index'][0]]},
            prefix + '01C4'   : {'qf3' : [family_data['qf3']['index'][1]]},
            prefix + '02C2'   : {'qf3' : [family_data['qf3']['index'][2]]},
            prefix + '02C4'   : {'qf3' : [family_data['qf3']['index'][3]]},
            prefix + '03C2'   : {'qf3' : [family_data['qf3']['index'][4]]},
            prefix + '03C4'   : {'qf3' : [family_data['qf3']['index'][5]]},
            prefix + '04C2'   : {'qf3' : [family_data['qf3']['index'][6]]},
            prefix + '04C4'   : {'qf3' : [family_data['qf3']['index'][7]]},
            prefix + '05C2'   : {'qf3' : [family_data['qf3']['index'][8]]},
            prefix + '05C4'   : {'qf3' : [family_data['qf3']['index'][9]]},
            prefix + '06C2'   : {'qf3' : [family_data['qf3']['index'][10]]},
            prefix + '06C4'   : {'qf3' : [family_data['qf3']['index'][11]]},
            prefix + '07C2'   : {'qf3' : [family_data['qf3']['index'][12]]},
            prefix + '07C4'   : {'qf3' : [family_data['qf3']['index'][13]]},
            prefix + '08C2'   : {'qf3' : [family_data['qf3']['index'][14]]},
            prefix + '08C4'   : {'qf3' : [family_data['qf3']['index'][15]]},
            prefix + '09C2'   : {'qf3' : [family_data['qf3']['index'][16]]},
            prefix + '09C4'   : {'qf3' : [family_data['qf3']['index'][17]]},
            prefix + '10C2'   : {'qf3' : [family_data['qf3']['index'][18]]},
            prefix + '10C4'   : {'qf3' : [family_data['qf3']['index'][19]]},
            prefix + '11C2'   : {'qf3' : [family_data['qf3']['index'][20]]},
            prefix + '11C4'   : {'qf3' : [family_data['qf3']['index'][21]]},
            prefix + '12C2'   : {'qf3' : [family_data['qf3']['index'][22]]},
            prefix + '12C4'   : {'qf3' : [family_data['qf3']['index'][23]]},
            prefix + '13C2'   : {'qf3' : [family_data['qf3']['index'][24]]},
            prefix + '13C4'   : {'qf3' : [family_data['qf3']['index'][25]]},
            prefix + '14C2'   : {'qf3' : [family_data['qf3']['index'][26]]},
            prefix + '14C4'   : {'qf3' : [family_data['qf3']['index'][27]]},
            prefix + '15C2'   : {'qf3' : [family_data['qf3']['index'][28]]},
            prefix + '15C4'   : {'qf3' : [family_data['qf3']['index'][29]]},
            prefix + '16C2'   : {'qf3' : [family_data['qf3']['index'][30]]},
            prefix + '16C4'   : {'qf3' : [family_data['qf3']['index'][31]]},
            prefix + '17C2'   : {'qf3' : [family_data['qf3']['index'][32]]},
            prefix + '17C4'   : {'qf3' : [family_data['qf3']['index'][33]]},
            prefix + '18C2'   : {'qf3' : [family_data['qf3']['index'][34]]},
            prefix + '18C4'   : {'qf3' : [family_data['qf3']['index'][35]]},
            prefix + '19C2'   : {'qf3' : [family_data['qf3']['index'][36]]},
            prefix + '19C4'   : {'qf3' : [family_data['qf3']['index'][37]]},
            prefix + '20C2'   : {'qf3' : [family_data['qf3']['index'][38]]},
            prefix + '20C4'   : {'qf3' : [family_data['qf3']['index'][39]]},
        }
        return _dict

    if element.lower() == 'sf2':
        prefix = prefix + 'SF2-'
        _dict = {
            prefix + '01C2'   : {'sf2' : [family_data['sf2']['index'][0]]},
            prefix + '02C2'   : {'sf2' : [family_data['sf2']['index'][1]]},
            prefix + '03C2'   : {'sf2' : [family_data['sf2']['index'][2]]},
            prefix + '04C2'   : {'sf2' : [family_data['sf2']['index'][3]]},
            prefix + '05C2'   : {'sf2' : [family_data['sf2']['index'][4]]},
            prefix + '06C2'   : {'sf2' : [family_data['sf2']['index'][5]]},
            prefix + '07C2'   : {'sf2' : [family_data['sf2']['index'][6]]},
            prefix + '08C2'   : {'sf2' : [family_data['sf2']['index'][7]]},
            prefix + '09C2'   : {'sf2' : [family_data['sf2']['index'][8]]},
            prefix + '10C2'   : {'sf2' : [family_data['sf2']['index'][9]]},
            prefix + '11C2'   : {'sf2' : [family_data['sf2']['index'][10]]},
            prefix + '12C2'   : {'sf2' : [family_data['sf2']['index'][11]]},
            prefix + '13C2'   : {'sf2' : [family_data['sf2']['index'][12]]},
            prefix + '14C2'   : {'sf2' : [family_data['sf2']['index'][13]]},
            prefix + '15C2'   : {'sf2' : [family_data['sf2']['index'][14]]},
            prefix + '16C2'   : {'sf2' : [family_data['sf2']['index'][15]]},
            prefix + '17C2'   : {'sf2' : [family_data['sf2']['index'][16]]},
            prefix + '18C2'   : {'sf2' : [family_data['sf2']['index'][17]]},
            prefix + '19C2'   : {'sf2' : [family_data['sf2']['index'][18]]},
            prefix + '20C2'   : {'sf2' : [family_data['sf2']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qf4':
        prefix = prefix + 'QF4-'
        _dict = {
            prefix + '01C2'   : {'qf4' : [family_data['qf4']['index'][0]]},
            prefix + '01C4'   : {'qf4' : [family_data['qf4']['index'][1]]},
            prefix + '02C2'   : {'qf4' : [family_data['qf4']['index'][2]]},
            prefix + '02C4'   : {'qf4' : [family_data['qf4']['index'][3]]},
            prefix + '03C2'   : {'qf4' : [family_data['qf4']['index'][4]]},
            prefix + '03C4'   : {'qf4' : [family_data['qf4']['index'][5]]},
            prefix + '04C2'   : {'qf4' : [family_data['qf4']['index'][6]]},
            prefix + '04C4'   : {'qf4' : [family_data['qf4']['index'][7]]},
            prefix + '05C2'   : {'qf4' : [family_data['qf4']['index'][8]]},
            prefix + '05C4'   : {'qf4' : [family_data['qf4']['index'][9]]},
            prefix + '06C2'   : {'qf4' : [family_data['qf4']['index'][10]]},
            prefix + '06C4'   : {'qf4' : [family_data['qf4']['index'][11]]},
            prefix + '07C2'   : {'qf4' : [family_data['qf4']['index'][12]]},
            prefix + '07C4'   : {'qf4' : [family_data['qf4']['index'][13]]},
            prefix + '08C2'   : {'qf4' : [family_data['qf4']['index'][14]]},
            prefix + '08C4'   : {'qf4' : [family_data['qf4']['index'][15]]},
            prefix + '09C2'   : {'qf4' : [family_data['qf4']['index'][16]]},
            prefix + '09C4'   : {'qf4' : [family_data['qf4']['index'][17]]},
            prefix + '10C2'   : {'qf4' : [family_data['qf4']['index'][18]]},
            prefix + '10C4'   : {'qf4' : [family_data['qf4']['index'][19]]},
            prefix + '11C2'   : {'qf4' : [family_data['qf4']['index'][20]]},
            prefix + '11C4'   : {'qf4' : [family_data['qf4']['index'][21]]},
            prefix + '12C2'   : {'qf4' : [family_data['qf4']['index'][22]]},
            prefix + '12C4'   : {'qf4' : [family_data['qf4']['index'][23]]},
            prefix + '13C2'   : {'qf4' : [family_data['qf4']['index'][24]]},
            prefix + '13C4'   : {'qf4' : [family_data['qf4']['index'][25]]},
            prefix + '14C2'   : {'qf4' : [family_data['qf4']['index'][26]]},
            prefix + '14C4'   : {'qf4' : [family_data['qf4']['index'][27]]},
            prefix + '15C2'   : {'qf4' : [family_data['qf4']['index'][28]]},
            prefix + '15C4'   : {'qf4' : [family_data['qf4']['index'][29]]},
            prefix + '16C2'   : {'qf4' : [family_data['qf4']['index'][30]]},
            prefix + '16C4'   : {'qf4' : [family_data['qf4']['index'][31]]},
            prefix + '17C2'   : {'qf4' : [family_data['qf4']['index'][32]]},
            prefix + '17C4'   : {'qf4' : [family_data['qf4']['index'][33]]},
            prefix + '18C2'   : {'qf4' : [family_data['qf4']['index'][34]]},
            prefix + '18C4'   : {'qf4' : [family_data['qf4']['index'][35]]},
            prefix + '19C2'   : {'qf4' : [family_data['qf4']['index'][36]]},
            prefix + '19C4'   : {'qf4' : [family_data['qf4']['index'][37]]},
            prefix + '20C2'   : {'qf4' : [family_data['qf4']['index'][38]]},
            prefix + '20C4'   : {'qf4' : [family_data['qf4']['index'][39]]},
        }
        return _dict

    if element.lower() == 'sf3':
        prefix = prefix + 'SF3-'
        _dict = {
            prefix + '01C4'   : {'sf3' : [family_data['sf3']['index'][0]]},
            prefix + '02C4'   : {'sf3' : [family_data['sf3']['index'][1]]},
            prefix + '03C4'   : {'sf3' : [family_data['sf3']['index'][2]]},
            prefix + '04C4'   : {'sf3' : [family_data['sf3']['index'][3]]},
            prefix + '05C4'   : {'sf3' : [family_data['sf3']['index'][4]]},
            prefix + '06C4'   : {'sf3' : [family_data['sf3']['index'][5]]},
            prefix + '07C4'   : {'sf3' : [family_data['sf3']['index'][6]]},
            prefix + '08C4'   : {'sf3' : [family_data['sf3']['index'][7]]},
            prefix + '09C4'   : {'sf3' : [family_data['sf3']['index'][8]]},
            prefix + '10C4'   : {'sf3' : [family_data['sf3']['index'][9]]},
            prefix + '11C4'   : {'sf3' : [family_data['sf3']['index'][10]]},
            prefix + '12C4'   : {'sf3' : [family_data['sf3']['index'][11]]},
            prefix + '13C4'   : {'sf3' : [family_data['sf3']['index'][12]]},
            prefix + '14C4'   : {'sf3' : [family_data['sf3']['index'][13]]},
            prefix + '15C4'   : {'sf3' : [family_data['sf3']['index'][14]]},
            prefix + '16C4'   : {'sf3' : [family_data['sf3']['index'][15]]},
            prefix + '17C4'   : {'sf3' : [family_data['sf3']['index'][16]]},
            prefix + '18C4'   : {'sf3' : [family_data['sf3']['index'][17]]},
            prefix + '19C4'   : {'sf3' : [family_data['sf3']['index'][18]]},
            prefix + '20C4'   : {'sf3' : [family_data['sf3']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sd4':
        prefix = prefix + 'SD4-'
        _dict = {
            prefix + '01C4'   : {'sd4' : [family_data['sd4']['index'][0]]},
            prefix + '02C4'   : {'sd4' : [family_data['sd4']['index'][1]]},
            prefix + '03C4'   : {'sd4' : [family_data['sd4']['index'][2]]},
            prefix + '04C4'   : {'sd4' : [family_data['sd4']['index'][3]]},
            prefix + '05C4'   : {'sd4' : [family_data['sd4']['index'][4]]},
            prefix + '06C4'   : {'sd4' : [family_data['sd4']['index'][5]]},
            prefix + '07C4'   : {'sd4' : [family_data['sd4']['index'][6]]},
            prefix + '08C4'   : {'sd4' : [family_data['sd4']['index'][7]]},
            prefix + '09C4'   : {'sd4' : [family_data['sd4']['index'][8]]},
            prefix + '10C4'   : {'sd4' : [family_data['sd4']['index'][9]]},
            prefix + '11C4'   : {'sd4' : [family_data['sd4']['index'][10]]},
            prefix + '12C4'   : {'sd4' : [family_data['sd4']['index'][11]]},
            prefix + '13C4'   : {'sd4' : [family_data['sd4']['index'][12]]},
            prefix + '14C4'   : {'sd4' : [family_data['sd4']['index'][13]]},
            prefix + '15C4'   : {'sd4' : [family_data['sd4']['index'][14]]},
            prefix + '16C4'   : {'sd4' : [family_data['sd4']['index'][15]]},
            prefix + '17C4'   : {'sd4' : [family_data['sd4']['index'][16]]},
            prefix + '18C4'   : {'sd4' : [family_data['sd4']['index'][17]]},
            prefix + '19C4'   : {'sd4' : [family_data['sd4']['index'][18]]},
            prefix + '20C4'   : {'sd4' : [family_data['sd4']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sd5':
        prefix = prefix + 'SD5-'
        _dict = {
            prefix + '01C5'   : {'sd5' : [family_data['sd5']['index'][0]]},
            prefix + '02C5'   : {'sd5' : [family_data['sd5']['index'][1]]},
            prefix + '03C5'   : {'sd5' : [family_data['sd5']['index'][2]]},
            prefix + '04C5'   : {'sd5' : [family_data['sd5']['index'][3]]},
            prefix + '05C5'   : {'sd5' : [family_data['sd5']['index'][4]]},
            prefix + '06C5'   : {'sd5' : [family_data['sd5']['index'][5]]},
            prefix + '07C5'   : {'sd5' : [family_data['sd5']['index'][6]]},
            prefix + '08C5'   : {'sd5' : [family_data['sd5']['index'][7]]},
            prefix + '09C5'   : {'sd5' : [family_data['sd5']['index'][8]]},
            prefix + '10C5'   : {'sd5' : [family_data['sd5']['index'][9]]},
            prefix + '11C5'   : {'sd5' : [family_data['sd5']['index'][10]]},
            prefix + '12C5'   : {'sd5' : [family_data['sd5']['index'][11]]},
            prefix + '13C5'   : {'sd5' : [family_data['sd5']['index'][12]]},
            prefix + '14C5'   : {'sd5' : [family_data['sd5']['index'][13]]},
            prefix + '15C5'   : {'sd5' : [family_data['sd5']['index'][14]]},
            prefix + '16C5'   : {'sd5' : [family_data['sd5']['index'][15]]},
            prefix + '17C5'   : {'sd5' : [family_data['sd5']['index'][16]]},
            prefix + '18C5'   : {'sd5' : [family_data['sd5']['index'][17]]},
            prefix + '19C5'   : {'sd5' : [family_data['sd5']['index'][18]]},
            prefix + '20C5'   : {'sd5' : [family_data['sd5']['index'][19]]},     }
        return _dict

    if element.lower() == 'sf4':
        prefix = prefix + 'SF4-'
        _dict = {
            prefix + '01C5'   : {'sf4' : [family_data['sf4']['index'][0]]},
            prefix + '02C5'   : {'sf4' : [family_data['sf4']['index'][1]]},
            prefix + '03C5'   : {'sf4' : [family_data['sf4']['index'][2]]},
            prefix + '04C5'   : {'sf4' : [family_data['sf4']['index'][3]]},
            prefix + '05C5'   : {'sf4' : [family_data['sf4']['index'][4]]},
            prefix + '06C5'   : {'sf4' : [family_data['sf4']['index'][5]]},
            prefix + '07C5'   : {'sf4' : [family_data['sf4']['index'][6]]},
            prefix + '08C5'   : {'sf4' : [family_data['sf4']['index'][7]]},
            prefix + '09C5'   : {'sf4' : [family_data['sf4']['index'][8]]},
            prefix + '10C5'   : {'sf4' : [family_data['sf4']['index'][9]]},
            prefix + '11C5'   : {'sf4' : [family_data['sf4']['index'][10]]},
            prefix + '12C5'   : {'sf4' : [family_data['sf4']['index'][11]]},
            prefix + '13C5'   : {'sf4' : [family_data['sf4']['index'][12]]},
            prefix + '14C5'   : {'sf4' : [family_data['sf4']['index'][13]]},
            prefix + '15C5'   : {'sf4' : [family_data['sf4']['index'][14]]},
            prefix + '16C5'   : {'sf4' : [family_data['sf4']['index'][15]]},
            prefix + '17C5'   : {'sf4' : [family_data['sf4']['index'][16]]},
            prefix + '18C5'   : {'sf4' : [family_data['sf4']['index'][17]]},
            prefix + '19C5'   : {'sf4' : [family_data['sf4']['index'][18]]},
            prefix + '20C5'   : {'sf4' : [family_data['sf4']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sd6':
        prefix = prefix + 'SD6-'
        _dict = {
            prefix + '01C5'   : {'sd6' : [family_data['sd6']['index'][0]]},
            prefix + '02C5'   : {'sd6' : [family_data['sd6']['index'][1]]},
            prefix + '03C5'   : {'sd6' : [family_data['sd6']['index'][2]]},
            prefix + '04C5'   : {'sd6' : [family_data['sd6']['index'][3]]},
            prefix + '05C5'   : {'sd6' : [family_data['sd6']['index'][4]]},
            prefix + '06C5'   : {'sd6' : [family_data['sd6']['index'][5]]},
            prefix + '07C5'   : {'sd6' : [family_data['sd6']['index'][6]]},
            prefix + '08C5'   : {'sd6' : [family_data['sd6']['index'][7]]},
            prefix + '09C5'   : {'sd6' : [family_data['sd6']['index'][8]]},
            prefix + '10C5'   : {'sd6' : [family_data['sd6']['index'][9]]},
            prefix + '11C5'   : {'sd6' : [family_data['sd6']['index'][10]]},
            prefix + '12C5'   : {'sd6' : [family_data['sd6']['index'][11]]},
            prefix + '13C5'   : {'sd6' : [family_data['sd6']['index'][12]]},
            prefix + '14C5'   : {'sd6' : [family_data['sd6']['index'][13]]},
            prefix + '15C5'   : {'sd6' : [family_data['sd6']['index'][14]]},
            prefix + '16C5'   : {'sd6' : [family_data['sd6']['index'][15]]},
            prefix + '17C5'   : {'sd6' : [family_data['sd6']['index'][16]]},
            prefix + '18C5'   : {'sd6' : [family_data['sd6']['index'][17]]},
            prefix + '19C5'   : {'sd6' : [family_data['sd6']['index'][18]]},
            prefix + '20C5'   : {'sd6' : [family_data['sd6']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sdb':
        prefix = prefix + 'SDB-'
        _dict = {
            prefix + '01M1'   : {'sdb' : [family_data['sdb']['index'][0]]},
            prefix + '02M1'   : {'sdb' : [family_data['sdb']['index'][1]]},
            prefix + '03M1'   : {'sdb' : [family_data['sdb']['index'][2]]},
            prefix + '04M1'   : {'sdb' : [family_data['sdb']['index'][3]]},
            prefix + '05M1'   : {'sdb' : [family_data['sdb']['index'][4]]},
            prefix + '06M1'   : {'sdb' : [family_data['sdb']['index'][5]]},
            prefix + '07M1'   : {'sdb' : [family_data['sdb']['index'][6]]},
            prefix + '08M1'   : {'sdb' : [family_data['sdb']['index'][7]]},
            prefix + '09M1'   : {'sdb' : [family_data['sdb']['index'][8]]},
            prefix + '10M1'   : {'sdb' : [family_data['sdb']['index'][9]]},
            prefix + '11M1'   : {'sdb' : [family_data['sdb']['index'][10]]},
            prefix + '12M1'   : {'sdb' : [family_data['sdb']['index'][11]]},
            prefix + '13M1'   : {'sdb' : [family_data['sdb']['index'][12]]},
            prefix + '14M1'   : {'sdb' : [family_data['sdb']['index'][13]]},
            prefix + '15M1'   : {'sdb' : [family_data['sdb']['index'][14]]},
            prefix + '16M1'   : {'sdb' : [family_data['sdb']['index'][15]]},
            prefix + '17M1'   : {'sdb' : [family_data['sdb']['index'][16]]},
            prefix + '18M1'   : {'sdb' : [family_data['sdb']['index'][17]]},
            prefix + '19M1'   : {'sdb' : [family_data['sdb']['index'][18]]},
            prefix + '20M1'   : {'sdb' : [family_data['sdb']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qdb1':
        prefix = prefix + 'QDB1-'
        _dict = {
            prefix + '01M1'   : {'qdb1' : [family_data['qdb1']['index'][0]]},
            prefix + '02M1'   : {'qdb1' : [family_data['qdb1']['index'][1]]},
            prefix + '03M1'   : {'qdb1' : [family_data['qdb1']['index'][2]]},
            prefix + '04M1'   : {'qdb1' : [family_data['qdb1']['index'][3]]},
            prefix + '05M1'   : {'qdb1' : [family_data['qdb1']['index'][4]]},
            prefix + '06M1'   : {'qdb1' : [family_data['qdb1']['index'][5]]},
            prefix + '07M1'   : {'qdb1' : [family_data['qdb1']['index'][6]]},
            prefix + '08M1'   : {'qdb1' : [family_data['qdb1']['index'][7]]},
            prefix + '09M1'   : {'qdb1' : [family_data['qdb1']['index'][8]]},
            prefix + '10M1'   : {'qdb1' : [family_data['qdb1']['index'][9]]},
            prefix + '11M1'   : {'qdb1' : [family_data['qdb1']['index'][10]]},
            prefix + '12M1'   : {'qdb1' : [family_data['qdb1']['index'][11]]},
            prefix + '13M1'   : {'qdb1' : [family_data['qdb1']['index'][12]]},
            prefix + '14M1'   : {'qdb1' : [family_data['qdb1']['index'][13]]},
            prefix + '15M1'   : {'qdb1' : [family_data['qdb1']['index'][14]]},
            prefix + '16M1'   : {'qdb1' : [family_data['qdb1']['index'][15]]},
            prefix + '17M1'   : {'qdb1' : [family_data['qdb1']['index'][16]]},
            prefix + '18M1'   : {'qdb1' : [family_data['qdb1']['index'][17]]},
            prefix + '19M1'   : {'qdb1' : [family_data['qdb1']['index'][18]]},
            prefix + '20M1'   : {'qdb1' : [family_data['qdb1']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qfb':
        prefix = prefix + 'QFB-'
        _dict = {
            prefix + '01M1'   : {'qfb' : [family_data['qfb']['index'][0]]},
            prefix + '02M1'   : {'qfb' : [family_data['qfb']['index'][1]]},
            prefix + '03M1'   : {'qfb' : [family_data['qfb']['index'][2]]},
            prefix + '04M1'   : {'qfb' : [family_data['qfb']['index'][3]]},
            prefix + '05M1'   : {'qfb' : [family_data['qfb']['index'][4]]},
            prefix + '06M1'   : {'qfb' : [family_data['qfb']['index'][5]]},
            prefix + '07M1'   : {'qfb' : [family_data['qfb']['index'][6]]},
            prefix + '08M1'   : {'qfb' : [family_data['qfb']['index'][7]]},
            prefix + '09M1'   : {'qfb' : [family_data['qfb']['index'][8]]},
            prefix + '10M1'   : {'qfb' : [family_data['qfb']['index'][9]]},
            prefix + '11M1'   : {'qfb' : [family_data['qfb']['index'][10]]},
            prefix + '12M1'   : {'qfb' : [family_data['qfb']['index'][11]]},
            prefix + '13M1'   : {'qfb' : [family_data['qfb']['index'][12]]},
            prefix + '14M1'   : {'qfb' : [family_data['qfb']['index'][13]]},
            prefix + '15M1'   : {'qfb' : [family_data['qfb']['index'][14]]},
            prefix + '16M1'   : {'qfb' : [family_data['qfb']['index'][15]]},
            prefix + '17M1'   : {'qfb' : [family_data['qfb']['index'][16]]},
            prefix + '18M1'   : {'qfb' : [family_data['qfb']['index'][17]]},
            prefix + '19M1'   : {'qfb' : [family_data['qfb']['index'][18]]},
            prefix + '20M1'   : {'qfb' : [family_data['qfb']['index'][19]]},
        }
        return _dict

    if element.lower() == 'sfb':
        prefix = prefix + 'SFB-'
        _dict = {
            prefix + '01M1'   : {'sfb' : [family_data['sfb']['index'][0]]},
            prefix + '02M1'   : {'sfb' : [family_data['sfb']['index'][1]]},
            prefix + '03M1'   : {'sfb' : [family_data['sfb']['index'][2]]},
            prefix + '04M1'   : {'sfb' : [family_data['sfb']['index'][3]]},
            prefix + '05M1'   : {'sfb' : [family_data['sfb']['index'][4]]},
            prefix + '06M1'   : {'sfb' : [family_data['sfb']['index'][5]]},
            prefix + '07M1'   : {'sfb' : [family_data['sfb']['index'][6]]},
            prefix + '08M1'   : {'sfb' : [family_data['sfb']['index'][7]]},
            prefix + '09M1'   : {'sfb' : [family_data['sfb']['index'][8]]},
            prefix + '10M1'   : {'sfb' : [family_data['sfb']['index'][9]]},
            prefix + '11M1'   : {'sfb' : [family_data['sfb']['index'][10]]},
            prefix + '12M1'   : {'sfb' : [family_data['sfb']['index'][11]]},
            prefix + '13M1'   : {'sfb' : [family_data['sfb']['index'][12]]},
            prefix + '14M1'   : {'sfb' : [family_data['sfb']['index'][13]]},
            prefix + '15M1'   : {'sfb' : [family_data['sfb']['index'][14]]},
            prefix + '16M1'   : {'sfb' : [family_data['sfb']['index'][15]]},
            prefix + '17M1'   : {'sfb' : [family_data['sfb']['index'][16]]},
            prefix + '18M1'   : {'sfb' : [family_data['sfb']['index'][17]]},
            prefix + '19M1'   : {'sfb' : [family_data['sfb']['index'][18]]},
            prefix + '20M1'   : {'sfb' : [family_data['sfb']['index'][19]]},
        }
        return _dict

    if element.lower() == 'qdb2':
        prefix = prefix + 'QDB2-'
        _dict = {
            prefix + '01M1'   : {'qdb2' : [family_data['qdb2']['index'][0]]},
            prefix + '02M1'   : {'qdb2' : [family_data['qdb2']['index'][1]]},
            prefix + '03M1'   : {'qdb2' : [family_data['qdb2']['index'][2]]},
            prefix + '04M1'   : {'qdb2' : [family_data['qdb2']['index'][3]]},
            prefix + '05M1'   : {'qdb2' : [family_data['qdb2']['index'][4]]},
            prefix + '06M1'   : {'qdb2' : [family_data['qdb2']['index'][5]]},
            prefix + '07M1'   : {'qdb2' : [family_data['qdb2']['index'][6]]},
            prefix + '08M1'   : {'qdb2' : [family_data['qdb2']['index'][7]]},
            prefix + '09M1'   : {'qdb2' : [family_data['qdb2']['index'][8]]},
            prefix + '10M1'   : {'qdb2' : [family_data['qdb2']['index'][9]]},
            prefix + '11M1'   : {'qdb2' : [family_data['qdb2']['index'][10]]},
            prefix + '12M1'   : {'qdb2' : [family_data['qdb2']['index'][11]]},
            prefix + '13M1'   : {'qdb2' : [family_data['qdb2']['index'][12]]},
            prefix + '14M1'   : {'qdb2' : [family_data['qdb2']['index'][13]]},
            prefix + '15M1'   : {'qdb2' : [family_data['qdb2']['index'][14]]},
            prefix + '16M1'   : {'qdb2' : [family_data['qdb2']['index'][15]]},
            prefix + '17M1'   : {'qdb2' : [family_data['qdb2']['index'][16]]},
            prefix + '18M1'   : {'qdb2' : [family_data['qdb2']['index'][17]]},
            prefix + '19M1'   : {'qdb2' : [family_data['qdb2']['index'][18]]},
            prefix + '20M1'   : {'qdb2' : [family_data['qdb2']['index'][19]]},
        }
        return _dict

    else:
        raise Exception('Element %s not found'%element)


def get_magnet_names(accelerator):
    return get_record_names(accelerator, 'sima')
