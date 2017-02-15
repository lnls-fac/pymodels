def join_name(section, discipline, device, subsection,
              instance=None, proper=None, field=None):

    name = section.upper() + '-' + subsection + ':' + discipline.upper() + '-' + device
    name += ('-' + instance) if instance else ""
    name += (':' + proper)   if proper   else ""
    name += ('.' + field)   if field   else ""
    return name

def split_name(name):
    name_dict = {}
    name_list = name.split(':')
    name_dict['area_name'] = name_list[0]
    name_dict['device_name'] = name_list[0] + ':' + name_list[1]

    name_sublist = name_list[0].split('-')
    name_dict['section']    = name_sublist[0]
    name_dict['subsection'] = name_sublist[1]

    name_sublist = name_list[1].split('-')
    name_dict['discipline'] = name_sublist[0]
    name_dict['device']     = name_sublist[1]
    name_dict['instance']   = name_sublist[2] if len(name_sublist) >= 3 else ''

    if len(name_list) >= 3:
        name_sublist = name_list[2].split('.')
        name_dict['property'] = name_sublist[0]
        name_dict['field'] = name_sublist[1] if len(name_sublist) >= 2 else ''
    else:
        name_dict['property'] = ''
        name_dict['field'] = ''

    return name_dict


class DeviceNames:
    pvnaming_glob = 'Glob'
    pvnaming_fam  = 'Fam'

    def split_name(self,name):
        return split_name(name)

    def join_name(self, discipline, device, subsection,
                  instance=None, proper=None, field=None):
        return join_name(self.section, discipline, device, subsection,
                        instance, proper, field)

    ### Must be implemented in classes that derive from this one ####
    def __init__(self):
        self.section = ''
        self.el_names = dict() # All these Family names must be defined in family_data dictionary
        self.fam_names = dict() # All these Family names must be defined in family_data dictionary
        self.glob_names = dict()# These Family names can be any name
        self.disciplines = sorted( self.el_names.keys() | self.fam_names.keys() | self.glob_names.keys())

        ##### Excitation Curves #######
        self.excitation_curves_mapping = dict()

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
                    device_name = self.join_name(dis, el, subsec[i], num[i])
                    _dict.update({ device_name:{el:idx[i]} })

            fams = self.fam_names.get(dis) or []
            for fam in fams:
                idx = family_data[fam]['index']
                device_name = self.join_name(dis, fam, self.pvnaming_fam)
                _dict.update({ device_name:{fam:idx} })

            globs = self.glob_names.get(dis) or []
            for glob in globs:
                device_name = self.join_name(dis, glob, self.pvnaming_glob)
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
        for mag, power in zip(['ma','pm'],['ps','pu']):
            # create a mapping of index in the lattice and magnet name
            mag_ind_dict = dict()
            for mag_name, mag_prop in self.get_device_names(accelerator,mag).items():
                if self.pvnaming_fam in mag_name: continue
                idx = list(mag_prop.values())[0][0]
                if mag_ind_dict.get(idx) is None: # there could be more than one magnet per index
                    mag_ind_dict[idx]  = set()
                mag_ind_dict[idx] |= {mag_name}

            #Use this mapping to see if the power supply is attached to the same element
            for ps_name, ps_prop in self.get_device_names(accelerator,power).items():
                ps = self.split_name(ps_name)['device']
                idx = list(ps_prop.values())[0]
                idx = [idx[0]] if self.pvnaming_fam not in ps_name else [i[0] for i in idx] # if Fam then indices are list of lists
                for i in idx:
                    mag_names = mag_ind_dict[i]
                    for mag_name in mag_names:
                        m = self.split_name(mag_name)['device']
                        if (m not in ps) and (ps not in m):
                            continue  # WARNING: WILL FAIL IF THE POWER SUPPLY DOES NOT HAVE THE MAGNET NAME ON ITSELF OR VICE VERSA.
                        if mapping.get(mag_name) is None:
                            mapping[mag_name]  = set()
                        mapping[mag_name] |= {ps_name}

        # Finally find the inverse map
        inverse_mapping = dict()
        for key, value in mapping.items():
            for v in value:
                if inverse_mapping.get(v) is None:
                    inverse_mapping[v] = set()
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
        for pm in pms_dev:
            dev = split_name(pm)['device']
            mapping[pm] = self.pulse_curve_mapping[dev]

        return mapping


    ####### Excitation Curves #########
    def get_excitation_curve_mapping(self,accelerator):
        """Get mapping from magnet to excitation curve file names

        Returns dict.
        """
        magnets = self.get_magnet_names(accelerator)

        ec = dict()
        for fams, curve in self.excitation_curves_mapping.items():
            for name in magnets:
                device = self.split_name(name)['device']
                if device.startswith(fams): ec[name] = curve
        return ec
