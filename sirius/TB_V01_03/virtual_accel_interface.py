
from . import families as _families
import sirius.naming_system as _naming_sys
import re as _re

_section = 'TB'
_el_names = { # All these Family names must be defined in family_data dictionary
    'DI': _families.families_di(),
    'PS': ['CH','CV','QD1','QF1','QD2A','QF2A','QF2B',
           'QD2B','QF3','QD3','QF4','QD4'],
    'MA': ['CH','CV','QD1','QF1','QD2A','QF2A','QF2B',
           'QD2B','QF3','QD3','QF4','QD4','B'],
    'TI': ['InjS'],
    'PU': ['InjS'],
    'PM': ['InjS']
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
    'InjS':'tbpm-sep-pulse.txt' # INJECTION SEPTUM
}

class TBDeviceNames(_naming_sys.DeviceNames):

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
            if _re.search('B', device)     is not None: ec[name] = 'tbma-b.txt'
            elif _re.search('Q', device)   is not None: ec[name] = 'tbma-q.txt'
            elif _re.search('CH', device)   is not None: ec[name] = 'tbma-ch.txt'
            elif _re.search('CV', device)  is not None: ec[name] = 'tbma-cv.txt'
            elif _re.search('S', device) is not None: ec[name] = 'tbpm-injs.txt'

        return ec
