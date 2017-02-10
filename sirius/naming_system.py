
_pvnaming_rule = 2 # 1 : PV Naming Proposal#1; 2 : PV Naming Proposal#2
def join_name(section, discipline, device, subsection, instance = None):

    if _pvnaming_rule == 1:       # Proposal 1
        name = section.upper() + '-' + discipline.upper() + ':' + device + '-' + subsection
    elif _pvnaming_rule == 2:     # Proposal 2
        name = section.upper() + '-' + subsection + ':' + discipline.upper() + '-' + device
    else:
        raise Exception('Device name specification not implemented.')

    name += ('-' + instance) if instance else ""
    return name

def split_name(name):
    name_list = [s.split(':') for s in name.split('-')]
    name_list = [y for x in name_list for y in x]
    name_dict = {}

    # Proposal 1
    if _pvnaming_rule == 1:
        name_dict['section']    = name_list[0]
        name_dict['discipline'] = name_list[1]
        name_dict['device']     = name_list[2]
        name_dict['subsection'] = name_list[3]
        name_dict['instance']   = name_list[4] if len(name_list) >= 5 else ''
        return name_dict

    # Proposal 2
    elif _pvnaming_rule == 2:
        name_dict['section']    = name_list[0]
        name_dict['subsection'] = name_list[1]
        name_dict['discipline'] = name_list[2]
        name_dict['device']     = name_list[3]
        name_dict['instance']   = name_list[4] if len(name_list) >= 5 else ''
        return name_dict

    else:
        raise Exception('Device name specification not implemented.')


class DeviceNames:
    pvnaming_glob = 'Glob'
    pvnaming_fam  = 'Fam'

    @staticmethod
    def join_name(section, discipline, device, subsection, instance = None):

        if _pvnaming_rule == 1:       # Proposal 1
            name = section.upper() + '-' + discipline.upper() + ':' + device + '-' + subsection
        elif _pvnaming_rule == 2:     # Proposal 2
            name = section.upper() + '-' + subsection + ':' + discipline.upper() + '-' + device
        else:
            raise Exception('Device name specification not implemented.')

        name += ('-' + instance) if instance else ""
        return name

    @staticmethod
    def split_name(name):
        name_list = [s.split(':') for s in name.split('-')]
        name_list = [y for x in name_list for y in x]
        name_dict = {}

        # Proposal 1
        if _pvnaming_rule == 1:
            name_dict['section']    = name_list[0]
            name_dict['discipline'] = name_list[1]
            name_dict['device']     = name_list[2]
            name_dict['subsection'] = name_list[3]
            name_dict['instance']   = name_list[4] if len(name_list) >= 5 else ''
            return name_dict

        # Proposal 2
        elif _pvnaming_rule == 2:
            name_dict['section']    = name_list[0]
            name_dict['subsection'] = name_list[1]
            name_dict['discipline'] = name_list[2]
            name_dict['device']     = name_list[3]
            name_dict['instance']   = name_list[4] if len(name_list) >= 5 else ''
            return name_dict

        else:
            raise Exception('Device name specification not implemented.')

    ### Must be implemented in classes that derive from this one ####
    def __init__(self):
        self.section = ''
        self.el_names = dict() # All these Family names must be defined in family_data dictionary
        self.fam_names = dict() # All these Family names must be defined in family_data dictionary
        self.glob_names = dict()# These Family names can be any name
        self.disciplines = sorted( self.el_names.keys() | self.fam_names.keys() | self.glob_names.keys())

        ##### Pulsed Magnets #######
        self.pulse_curve_mapping = dict()

        ##### Family Data Function ######
        self.get_family_data = lambda x: x

        return NotImplemented

    ##### Device Names ######
    def get_device_names(self, accelerator, discipline = None):
        """Return a dictionary of device names for given discipline
        each entry is another dictionary of model families whose
        values are the indices in the pyaccel model of the magnets
        that belong to the family. The magnet models can be segmented,
        in which case the value is a python list of lists."""
        family_data = accelerator
        if not isinstance(accelerator, dict):
            family_data = self.get_family_data(accelerator)

        if discipline == None:
            discipline = self.disciplines
        if not isinstance(discipline,(list,tuple)):
            discipline = [discipline.upper()]
        else:
            discipline = [s.upper() for s in discipline]

        _dict = {}
        for dis in discipline:
            names = self.el_names.get(dis) or []
            for el in names:
                subsec = family_data[el]['subsection']
                num    = family_data[el]['instance']
                idx    = family_data[el]['index']
                for i in range(len(subsec)):
                    device_name = self.join_name(self.section, dis, el, subsec[i], num[i])
                    _dict.update({ device_name:{el:idx[i]} })

            fams = self.fam_names.get(dis) or []
            for fam in fams:
                idx = family_data[fam]['index']
                device_name = self.join_name(self.section, dis, fam, self.pvnaming_fam)
                _dict.update({ device_name:{fam:idx} })

            globs = self.glob_names.get(dis) or []
            for glob in globs:
                device_name = join_name(self.section, dis, glob, self.pvnaming_glob)
                _dict.update({ device_name:{} })

        return _dict

    def get_magnet_names(self,accelerator):
        _dict = self.get_device_names(accelerator, 'ma')
        _dict.update(self.get_device_names(accelerator, 'pm'))
        return _dict


    ####### Power Supplies ########
    def get_magnet2power_supply_mapping(self, accelerator):
        """Get mapping from power supply to magnet names and inverse mapping

        Returns mapping, inverse_mapping.
        """
        mapping = dict()
        for power, mag in zip(['ma','pm'],['ps','pu']):
            # create a mapping of index in the lattice and magnet name
            mag_ind_dict = dict()
            for mag_name, mag_prop in self.get_device_names(accelerator,power).items():
                if self.pvnaming_fam in mag_name: continue
                idx = list(mag_prop.values())[0][0]
                mag_ind_dict[idx] = mag_name

            #Use this mapping to see if the power supply is attached to the same element
            for ps_name, ps_prop in self.get_device_names(accelerator,mag).items():
                idx = list(ps_prop.values())[0]
                idx = [idx[0]] if self.pvnaming_fam not in ps_name else [i[0] for i in idx] # if Fam then indices are list of lists
                for i in idx:
                    mag_name = mag_ind_dict[i]
                    if mapping.get(mag_name) is None:
                        mapping[mag_name]  = {ps_name}
                    else:
                        mapping[mag_name] |= {ps_name}

        # Finally find the inverse map
        inverse_mapping = dict()
        for key, value in mapping.items():
            for v in value:
                if inverse_mapping.get(v) is None:
                    inverse_mapping[v] = {key}
                else:
                    inverse_mapping[v].add(key)

        return mapping, inverse_mapping


    ####### Pulsed Magnets #########
    def _get_pulsed_magnet_mapping(self, accelerator,delay_or_enbl):
        mapping = {}
        tis_dev = set(self.get_device_names(accelerator, 'TI').keys())
        pms_dev = set(self.get_device_names(accelerator, 'PM').keys())
        for pm in pms_dev:
            dev = split_name(pm)['device']
            ti = [i for i in tis_dev if dev in i][0]
            mapping[pm] = ti + delay_or_enbl

        inverse_mapping = dict()
        for key, value in mapping.items():
            inverse_mapping[value] = key

        return mapping, inverse_mapping

    def get_magnet_delay_mapping(self, accelerator):
        """Get mapping from pulsed magnet to timing delay

        Returns dict.
        """
        return self._get_pulsed_magnet_mapping(accelerator,':Delay')

    def get_magnet_enabled_mapping(self, accelerator):
        """Get mapping from pulsed magnet to timing enabled

        Returns dict.
        """
        return self._get_pulsed_magnet_mapping(accelerator,':Enbl')

    def get_pulse_curve_mapping(self, accelerator):
        """Get mapping from pulsed magnet to pulse curve file names

        Returns dict.
        """
        mapping = {}
        pms_dev = set(self.get_device_names(accelerator, 'PM').keys())
        for pm in _pms_dev:
            dev = split_name(pm)['device']
            mapping[pm] = self.pulse_curve_mapping[dev]

        return mapping


    ####### Excitation Curves #########
    def get_excitation_curve_mapping(accelerator):  return NotImplemented
