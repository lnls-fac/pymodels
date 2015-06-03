import sirius

def get_record_names(family_name = None):

    family_data = sirius.TS_V400.lattice._family_data

    if family_name == None:
        families = ['bend', 'sidi', 'qf',
                    'qd', 'ch', 'cv', 'sep']
        record_names_dict = {}
        for family in families:
            record_names_dict.update(get_record_names(family))
        return record_names_dict

    if family_name.lower() == 'bend':
        _dict = {
            'TSPS-BEND-01' : {'bf ' :  family_data['bf']['index']},
            'TSPS-BEND-02' : {'bd ' : [family_data['bd']['index'][0]]},
            'TSPS-BEND-03' : {'bd ' : [family_data['bd']['index'][1]]},
        }
        return _dict

    if family_name.lower() == 'sidi':
        _dict = {}
        bpm_dict = get_record_names(family_name = 'bpm')
        _dict.update(bpm_dict)
        return _dict

    if family_name.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            'TSDI-BPM-01'   : {'bpm' : [indices[0]]},
            'TSDI-BPM-02'   : {'bpm' : [indices[1]]},
            'TSDI-BPM-03'   : {'bpm' : [indices[2]]},
            'TSDI-BPM-04-A' : {'bpm' : [indices[3]]},
            'TSDI-BPM-04-B' : {'bpm' : [indices[4]]},
        }
        return _dict

    if family_name.lower() == 'qf':
        indices = family_data['qf']['index']
        _dict = {
            'TSPS-QF-01'   : {'qf' : [indices[0]]},
            'TSPS-QF-03-A' : {'qf' : [indices[1]]},
            'TSPS-QF-03-B' : {'qf' : [indices[2]]},
            'TSPS-QF-04-A' : {'qf' : [indices[3]]},
            'TSPS-QF-04-B' : {'qf' : [indices[4]]},
        }
        return _dict

    if family_name.lower() == 'qd':
        indices = family_data['qd']['index']
        _dict = {
            'TSPS-QD-01'   : {'qd' : [indices[0]]},
            'TSPS-QD-02'   : {'qd' : [indices[1]]},
            'TSPS-QD-04-A' : {'qd' : [indices[2]]},
            'TSPS-QD-04-B' : {'qd' : [indices[3]]},
        }
        return _dict

    if family_name.lower() == 'ch':
        indices = family_data['ch']['index']
        _dict = {
            'TSPS-CH-01'   : {'ch' : [indices[0]]},
            'TSPS-CH-02'   : {'ch' : [indices[1]]},
            'TSPS-CH-03'   : {'ch' : [indices[2]]},
            'TSPS-CH-04'   : {'ch' : [indices[3]]},
        }
        return _dict

    if family_name.lower() == 'cv':
        indices = family_data['cv']['index']
        _dict = {
            'TSPS-CV-01-A' : {'cv' : [indices[0]]},
            'TSPS-CV-01-B' : {'cv' : [indices[1]]},
            'TSPS-CV-02'   : {'cv' : [indices[2]]},
            'TSPS-CV-03'   : {'cv' : [indices[3]]},
            'TSPS-CV-04-A' : {'cv' : [indices[4]]},
            'TSPS-CV-04-B' : {'cv' : [indices[5]]},
        }
        return _dict

    if family_name.lower() == 'sep':
        _dict ={
            'TSPU-SEPEX-01'   : {'seb' :  family_data['seb']['index']},
            'TSPU-SEPINTK-04' : {'seg' : [family_data['seg']['index'][0]]},
            'TSPU-SEPINTN-04' : {'sef' : [family_data['sef']['index'][0]]},
        }
        return _dict

    else:
        raise Exception('Family name %s not found'%family_name)
