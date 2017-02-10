
from . import families as _families
import sirius.naming_system as _naming_sys
import re as _re

_section = 'TS'
_el_names = { # All these Family names must be defined in family_data dictionary
    'DI': _families.families_di(),
    'PS': ['CH','CV','QF1A','QF1B','QD2','QF2','QF3',
           'QD4A','QF4','QD4B'],
    'MA': ['CH','CV','QF1A','QF1B','QD2','QF2','QF3',
           'QD4A','QF4','QD4B','B'],
    'TI': _families.families_pulsed_magnets(),
    'PU': _families.families_pulsed_magnets(),
    'PM': _families.families_pulsed_magnets()
}
_fam_names = { # All these Family names must be defined in family_data dictionary
    'DI': ['BPM'],
    'PS': ['B'],
    'MA': ['B']
}
_glob_names = dict() # These Family names can be any name
_disciplines = sorted( _el_names.keys() | _fam_names.keys() | _glob_names.keys())

##### Pulsed Magnets #######
_pulse_curve_mapping= {
    'InjSF':'tspm-injs-pulse.txt', # INJECTION SEPTUM
    'InjSG':'tspm-injs-pulse.txt', # INJECTION SEPTUM
    'EjeSF':'tspm-ejes-pulse.txt',
    'EjeSG':'tspm-ejes-pulse.txt',
}

class TSDeviceNames(_naming_sys.DeviceNames):

    def __init__(self):
        self.section = _section
        self.el_names = _el_names  # All these Family names must be defined in family_data dictionary
        self.fam_names = _fam_names  # All these Family names must be defined in family_data dictionary
        self.glob_names = _glob_names # These Family names can be any name
        self.disciplines = _disciplines

        ##### Pulsed Magnets #######
        self._pulse_curve_mapping = _pulse_curve_mapping

        ##### Family Data Function ######
        self.get_family_data = _families.get_family_data


    ####### Excitation Curves #########
    def get_excitation_curve_mapping(self,accelerator):
        """Get mapping from magnet to excitation curve file names

        Returns dict.
        """
        magnets = self.get_magnet_names(accelerator)

        ec = dict()
        for name in magnets:
            device = self.split_name(name)['device']
            if _re.search('B', device)       is not None: ec[name] = 'tsma-b.txt'
            elif _re.search('QF1', device)   is not None: ec[name] = 'tsma-q14.txt'
            elif _re.search('QD', device)    is not None: ec[name] = 'tsma-q14.txt'
            elif _re.search('QF', device)    is not None: ec[name] = 'tsma-q20.txt'
            elif _re.search('CH', device)    is not None: ec[name] = 'tsma-ch.txt'
            elif _re.search('CV', device)    is not None: ec[name] = 'tsma-cv.txt'
            elif _re.search('EjeSF', device) is not None: ec[name] = 'tspm-ejesf.txt'
            elif _re.search('EjeSG', device) is not None: ec[name] = 'tspm-ejesg.txt'
            elif _re.search('InjSG', device) is not None: ec[name] = 'tspm-injsg.txt'
            elif _re.search('InjSF', device) is not None: ec[name] = 'tspm-injsf.txt'

        return ec
