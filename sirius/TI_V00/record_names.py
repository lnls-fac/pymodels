
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
                'TI-BO-KICKIN-ON':{},        # whether to pulse BO injection kicker
                'TI-BO-KICKIN-DELAY':{},     # when to pulse BO injection kickes
                'TI-BO-KICKEX-ON':{},        # whether to pulse BO extraction kicker
                'TI-BO-KICKEX-DELAY':{},     # when to pulse BO extraction kicker
                'TI-SI-KICKIN-ON':{} ,       # whether to pulse SI injection kicker
                'TI-SI-KICKIN-DELAY':{},     # when to pulse SI injection kicker
                'TI-SI-KICKIN-INC':{},       # increment to SI injection kicker delay
        }
        return _dict

    else:
        raise Exception('Family name %s not found'%family_name)
