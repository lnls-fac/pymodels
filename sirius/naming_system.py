
_pvnaming_rule = 2 # 1 : PV Naming Proposal#1; 2 : PV Naming Proposal#2

pvnaming_glob = 'Glob'
pvnaming_fam  = 'Fam'

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
        raise Exception('Device name specification not implemented.')

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
        raise Exception('Device name specification not implemented.')
