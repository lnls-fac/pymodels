
from . import families as _families

def get_record_names(family_name = None):

    family_data = _families._family_data

    if family_name == None:
        families = ['ch', 'cv', 'qf-fam', 'qd-fam', 'sd-fam', 'sf-fam', 'bend-fam', 'bopa', 'bodi', 'bpm-fam']
        record_names_dict = {}
        for i in range(len(families)):
            record_names_dict.update(get_record_names(families[i]))
        return record_names_dict

    if family_name.lower() == 'bopa':
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

    if family_name.lower() == 'bodi':
        _dict = {
                'BODI-TUNEH':{},
                'BODI-TUNEV':{},
                'BODI-TUNES':{},
                'BODI-CURRENT':{},
                'BODI-BCURRENT':{},
        }
        bpm_dict = get_record_names(family_name = 'bpm')
        _dict.update(bpm_dict)
        return _dict

    if family_name.lower() == 'bpm-fam':
        indices = family_data['bpm']['index']
        _dict = {'BODI-BPM-FAM-X': {'bpm': indices},
                 'BODI-BPM-FAM-Y': {'bpm': indices}
                }
        return _dict

    if family_name.lower() == 'bpm':
        prefix = 'BODI-BPM-'
        bpm_dict = {
            prefix + '01A' : {'bpm' : [family_data['bpm']['index'][49]]},
            prefix + '02A' : {'bpm' : [family_data['bpm']['index'][0]]},
            prefix + '03A' : {'bpm' : [family_data['bpm']['index'][1]]},
            prefix + '04A' : {'bpm' : [family_data['bpm']['index'][2]]},
            prefix + '05A' : {'bpm' : [family_data['bpm']['index'][3]]},
            prefix + '06A' : {'bpm' : [family_data['bpm']['index'][4]]},
            prefix + '07A' : {'bpm' : [family_data['bpm']['index'][5]]},
            prefix + '08A' : {'bpm' : [family_data['bpm']['index'][6]]},
            prefix + '09A' : {'bpm' : [family_data['bpm']['index'][7]]},
            prefix + '10A' : {'bpm' : [family_data['bpm']['index'][8]]},
            prefix + '11A' : {'bpm' : [family_data['bpm']['index'][9]]},
            prefix + '12A' : {'bpm' : [family_data['bpm']['index'][10]]},
            prefix + '13A' : {'bpm' : [family_data['bpm']['index'][11]]},
            prefix + '14A' : {'bpm' : [family_data['bpm']['index'][12]]},
            prefix + '15A' : {'bpm' : [family_data['bpm']['index'][13]]},
            prefix + '16A' : {'bpm' : [family_data['bpm']['index'][14]]},
            prefix + '17A' : {'bpm' : [family_data['bpm']['index'][15]]},
            prefix + '18A' : {'bpm' : [family_data['bpm']['index'][16]]},
            prefix + '19A' : {'bpm' : [family_data['bpm']['index'][17]]},
            prefix + '20A' : {'bpm' : [family_data['bpm']['index'][18]]},
            prefix + '21A' : {'bpm' : [family_data['bpm']['index'][19]]},
            prefix + '22A' : {'bpm' : [family_data['bpm']['index'][20]]},
            prefix + '23A' : {'bpm' : [family_data['bpm']['index'][21]]},
            prefix + '24A' : {'bpm' : [family_data['bpm']['index'][22]]},
            prefix + '25A' : {'bpm' : [family_data['bpm']['index'][23]]},
            prefix + '26A' : {'bpm' : [family_data['bpm']['index'][24]]},
            prefix + '27A' : {'bpm' : [family_data['bpm']['index'][25]]},
            prefix + '28A' : {'bpm' : [family_data['bpm']['index'][26]]},
            prefix + '29A' : {'bpm' : [family_data['bpm']['index'][27]]},
            prefix + '30A' : {'bpm' : [family_data['bpm']['index'][28]]},
            prefix + '31A' : {'bpm' : [family_data['bpm']['index'][29]]},
            prefix + '32A' : {'bpm' : [family_data['bpm']['index'][30]]},
            prefix + '33A' : {'bpm' : [family_data['bpm']['index'][31]]},
            prefix + '34A' : {'bpm' : [family_data['bpm']['index'][32]]},
            prefix + '35A' : {'bpm' : [family_data['bpm']['index'][33]]},
            prefix + '36A' : {'bpm' : [family_data['bpm']['index'][34]]},
            prefix + '37A' : {'bpm' : [family_data['bpm']['index'][35]]},
            prefix + '38A' : {'bpm' : [family_data['bpm']['index'][36]]},
            prefix + '39A' : {'bpm' : [family_data['bpm']['index'][37]]},
            prefix + '40A' : {'bpm' : [family_data['bpm']['index'][38]]},
            prefix + '41A' : {'bpm' : [family_data['bpm']['index'][39]]},
            prefix + '42A' : {'bpm' : [family_data['bpm']['index'][40]]},
            prefix + '43A' : {'bpm' : [family_data['bpm']['index'][41]]},
            prefix + '44A' : {'bpm' : [family_data['bpm']['index'][42]]},
            prefix + '45A' : {'bpm' : [family_data['bpm']['index'][43]]},
            prefix + '46A' : {'bpm' : [family_data['bpm']['index'][44]]},
            prefix + '47A' : {'bpm' : [family_data['bpm']['index'][45]]},
            prefix + '48A' : {'bpm' : [family_data['bpm']['index'][46]]},
            prefix + '49A' : {'bpm' : [family_data['bpm']['index'][47]]},
            prefix + '50A' : {'bpm' : [family_data['bpm']['index'][48]]},
        }
        return bpm_dict

    if family_name.lower() == 'ch':
        prefix = 'BOPS-CH-'
        ch_dict ={
            prefix + '01A' : {'ch' : [family_data['ch']['index'][24]]},
            prefix + '03B' : {'ch' : [family_data['ch']['index'][0]]},
            prefix + '05A' : {'ch' : [family_data['ch']['index'][1]]},
            prefix + '07A' : {'ch' : [family_data['ch']['index'][2]]},
            prefix + '09A' : {'ch' : [family_data['ch']['index'][3]]},
            prefix + '11A' : {'ch' : [family_data['ch']['index'][4]]},
            prefix + '13A' : {'ch' : [family_data['ch']['index'][5]]},
            prefix + '15A' : {'ch' : [family_data['ch']['index'][6]]},
            prefix + '17A' : {'ch' : [family_data['ch']['index'][7]]},
            prefix + '19A' : {'ch' : [family_data['ch']['index'][8]]},
            prefix + '21A' : {'ch' : [family_data['ch']['index'][9]]},
            prefix + '23A' : {'ch' : [family_data['ch']['index'][10]]},
            prefix + '25A' : {'ch' : [family_data['ch']['index'][11]]},
            prefix + '27A' : {'ch' : [family_data['ch']['index'][12]]},
            prefix + '29A' : {'ch' : [family_data['ch']['index'][13]]},
            prefix + '31A' : {'ch' : [family_data['ch']['index'][14]]},
            prefix + '33A' : {'ch' : [family_data['ch']['index'][15]]},
            prefix + '35A' : {'ch' : [family_data['ch']['index'][16]]},
            prefix + '37A' : {'ch' : [family_data['ch']['index'][17]]},
            prefix + '39A' : {'ch' : [family_data['ch']['index'][18]]},
            prefix + '41A' : {'ch' : [family_data['ch']['index'][19]]},
            prefix + '43A' : {'ch' : [family_data['ch']['index'][20]]},
            prefix + '45A' : {'ch' : [family_data['ch']['index'][21]]},
            prefix + '47A' : {'ch' : [family_data['ch']['index'][22]]},
            prefix + '49A' : {'ch' : [family_data['ch']['index'][23]]},
        }
        return ch_dict

    if family_name.lower() == 'cv':
        prefix = 'BOPS-CV-'
        cv_dict ={
            prefix + '01A' : {'cv' : [family_data['cv']['index'][24]]},
            prefix + '03A' : {'cv' : [family_data['cv']['index'][0]]},
            prefix + '05A' : {'cv' : [family_data['cv']['index'][1]]},
            prefix + '07A' : {'cv' : [family_data['cv']['index'][2]]},
            prefix + '09A' : {'cv' : [family_data['cv']['index'][3]]},
            prefix + '11A' : {'cv' : [family_data['cv']['index'][4]]},
            prefix + '13A' : {'cv' : [family_data['cv']['index'][5]]},
            prefix + '15A' : {'cv' : [family_data['cv']['index'][6]]},
            prefix + '17A' : {'cv' : [family_data['cv']['index'][7]]},
            prefix + '19A' : {'cv' : [family_data['cv']['index'][8]]},
            prefix + '21A' : {'cv' : [family_data['cv']['index'][9]]},
            prefix + '23A' : {'cv' : [family_data['cv']['index'][10]]},
            prefix + '25A' : {'cv' : [family_data['cv']['index'][11]]},
            prefix + '27A' : {'cv' : [family_data['cv']['index'][12]]},
            prefix + '29A' : {'cv' : [family_data['cv']['index'][13]]},
            prefix + '31A' : {'cv' : [family_data['cv']['index'][14]]},
            prefix + '33A' : {'cv' : [family_data['cv']['index'][15]]},
            prefix + '35A' : {'cv' : [family_data['cv']['index'][16]]},
            prefix + '37A' : {'cv' : [family_data['cv']['index'][17]]},
            prefix + '39A' : {'cv' : [family_data['cv']['index'][18]]},
            prefix + '41A' : {'cv' : [family_data['cv']['index'][19]]},
            prefix + '43A' : {'cv' : [family_data['cv']['index'][20]]},
            prefix + '45A' : {'cv' : [family_data['cv']['index'][21]]},
            prefix + '47A' : {'cv' : [family_data['cv']['index'][22]]},
            prefix + '49A' : {'cv' : [family_data['cv']['index'][23]]},
        }
        return cv_dict

    if family_name.lower() == 'qf-fam':
        qf_dict = { 'BOPS-QF-FAM' : {'qf' : family_data['qf']['index']}}
        return qf_dict

    if family_name.lower() == 'qd-fam':
        qd_dict = { 'BOPS-QD-FAM' : {'qd' : family_data['qd']['index']}}
        return qd_dict

    if family_name.lower() == 'sd-fam':
        sd_dict = { 'BOPS-SD-FAM' : {'sd' : family_data['sd']['index']}}
        return sd_dict

    if family_name.lower() == 'sf-fam':
        sf_dict = { 'BOPS-SF-FAM' : {'sf' : family_data['sf']['index']}}
        return sf_dict

    if family_name.lower() == 'b-fam' or family_name.lower() == 'bend-fam':
        b_dict = { 'BOPS-BEND-FAM-A' : {'bend' : family_data['b']['index']},
                   'BOPS-BEND-FAM-B' : {'bend' : family_data['b']['index']}}
        return b_dict

    else:
        raise Exception('Family name %s not found'%family_name)
