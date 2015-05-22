
import sirius

def get_record_names(family_name = None):

    family_data = sirius.LI_V00._lattice._family_data

    if family_name == None:
        families = ['li']
        record_names_dict = {}
        for i in range(len(families)):
            record_names_dict.update(get_record_names(families[i]))
        return record_names_dict

    if family_name.lower() == 'li':
        _dict = {
                #'BOPA-SIGY':{},
                #'BOPA-SIGS':{},
        }
        return _dict
    else:
        raise Exception('Family name %s not found'%family_name)
