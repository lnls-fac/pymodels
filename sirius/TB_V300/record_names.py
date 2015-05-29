import sirius

def get_record_names(family_name = None):

    family_data = sirius.TB_V300.lattice._family_data

    if family_name == None:
        families = ['bend', 'sidi', 'qf',
                    'qd', 'ch', 'cv', 'sep']
        record_names_dict = {}
        for family in families:
            record_names_dict.update(get_record_names(family))
        return record_names_dict

    if family_name.lower() == 'bend':
        _dict = {
            'TBPS-BEND-01' : {'bspec' :  family_data['bspec']['index']},
            'TBPS-BEND-02' : {'bn '   :  family_data['bn']['index']},
            'TBPS-BEND-03' : {'bp '   : [family_data['bp']['index'][0]]},
            'TBPS-BEND-04' : {'bp '   : [family_data['bp']['index'][1]]},
        }
        return _dict

    if family_name.lower() == 'sidi':
        _dict = {
            'TBDI-CURRENT':{},
        }
        bpm_dict = get_record_names(family_name = 'bpm')
        _dict.update(bpm_dict)
        return _dict

    if family_name.lower() == 'bpm':
        indices = family_data['bpm']['index']
        _dict = {
            'TBDI-BPM-02'   : {'bpm' : [indices[0]]},
            'TBDI-BPM-03-A' : {'bpm' : [indices[1]]},
            'TBDI-BPM-03-B' : {'bpm' : [indices[2]]},
            'TBDI-BPM-04'   : {'bpm' : [indices[3]]},
            'TBDI-BPM-05'   : {'bpm' : [indices[4]]},
        }
        return _dict

    if family_name.lower() == 'qf':
        indices = family_data['qf']['index']
        _dict = {
            'TBPS-QF-01-A' : {'qf' : [indices[0]]},
            'TBPS-QF-01-B' : {'qf' : [indices[1]]},
            'TBPS-QF-02'   : {'qf' : [indices[2]]},
            'TBPS-QF-03-A' : {'qf' : [indices[3]]},
            'TBPS-QF-03-B' : {'qf' : [indices[4]]},
            'TBPS-QF-04'   : {'qf' : [indices[5]]},
            'TBPS-QF-05'   : {'qf' : [indices[6]]},
        }
        return _dict

    if family_name.lower() == 'qd':
        indices = family_data['qd']['index']
        _dict = {
            'TBPS-QD-01'   : {'qd' : [indices[0],indices[1]]},
            'TBPS-QD-02'   : {'qd' : [indices[2]]},
            'TBPS-QD-03'   : {'qd' : [indices[3]]},
            'TBPS-QD-04'   : {'qd' : [indices[4]]},
            'TBPS-QD-05'   : {'qd' : [indices[5]]},
        }
        return _dict

    if family_name.lower() == 'ch':
        _dict = { 'TBPS-CH-03':
            {'ch' : [family_data['ch']['index'][0]]},
        }
        return _dict

    if family_name.lower() == 'cv':
        indices = family_data['cv']['index']
        _dict = {
            'TBPS-CV-02-A' : {'cv' : [indices[0]]},
            'TBPS-CV-02-B' : {'cv' : [indices[1]]},
            'TBPS-CV-03-A' : {'cv' : [indices[2]]},
            'TBPS-CV-03-B' : {'cv' : [indices[3]]},
            'TBPS-CV-05-A' : {'cv' : [indices[4]]},
            'TBPS-CV-05-B' : {'cv' : [indices[5]]},
        }
        return _dict

    if family_name.lower() == 'sep':
        _dict ={
            'TBPU-SEPIN-05' : {'sep' : family_data['sep']['index']},
        }
        return _dict

    else:
        raise Exception('Family name %s not found'%family_name)
