
import sirius

def get_record_names(family_name = None):

    if family_name == None:
        families = ['ti']

        record_names_dict = {}
        for i in range(len(families)):
            record_names_dict.update(get_record_names(families[i]))
        return record_names_dict

    if family_name.lower() == 'ti':
        _dict = {
                'TI-CYCLE':{},               # when set starts entire injection cycle
                #'TI-BO-KICKIN-ON':{},
                #'TI-BO-KICKIN-DELAY':{},
                #'TI-BO-KICKEX-ON':{},
                #'TI-BO-KICKEX-DELAY':{},     
                'TI-DELAY-BO2SI':{},         # current time delay of ring relative to booster [s]
                'TI-DELAY-BO2SI-DELTA':{},   # delta time: should be set to inverse of RF frequency
                'TI-DELAY-BO2SI-INC':{}      # when set DELAY-BO2SI-DELTA is added to DELAY-BO2SI
        }
        return _dict

    else:
        raise Exception('Family name %s not found'%family_name)
