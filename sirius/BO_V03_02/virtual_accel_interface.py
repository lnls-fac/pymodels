
from . import families as _families
import sirius.naming_system as _naming_sys
import re as _re

_section = 'BO'
_el_names = { # All these Family names must be defined in family_data dictionary
    'DI': _families.families_di(),
    'RF': _families.families_rf(),
    'MA': ['B','QD','QF','SD','SF','QS','CH','CV'],
    'PS': ['QS','CH','CV'],
    'PM': ['InjK','EjeK'],
    'PU': ['InjK','EjeK'],
    'TI': ['InjK','EjeK'],
}
_fam_names = { # All these Family names must be defined in family_data dictionary
    'PS': ['B-1','B-2','QD','QF','SD','SF'],
    'MA': ['B-1','B-2','QD','QF','SD','SF'],
    'DI': ['BPM']
}
_glob_names = {# These Family names can be any name
    'AP': ['ChromX','ChromY','Lifetime','BLifetime','SigX','SigY','SigS','EmitX','EmitY'],
    'TI': ['STDMOE']
}
_disciplines = sorted( _el_names.keys() | _fam_names.keys() | _glob_names.keys())

##### Pulsed Magnets #######
_pulse_curve_mapping= {
    'EjeK':'bopm-ejek-pulse.txt',
    'InjK':'bopm-injk-pulse.txt',
}

class BODeviceNames(_naming_sys.DeviceNames):

    def __init__(self):
        self.section = _section
        self.el_names = _el_names  # All these Family names must be defined in family_data dictionary
        self.fam_names = _fam_names  # All these Family names must be defined in family_data dictionary
        self.glob_names = _glob_names # These Family names can be any name
        self.disciplines = _disciplines

        ##### Pulsed Magnets #######
        self.pulse_curve_mapping = _pulse_curve_mapping

        ##### Family Data Function ######
        self.get_family_data = _families.get_family_data


    ####### Excitation Curves #########
    def get_excitation_curve_mapping(self,accelerator):
        """Get mapping from magnet to excitation curve file names

        Returns dict.
        """
        magnets = get_magnet_names(accelerator)

        ec = dict()
        for name in magnets:
            device = _naming_system.split_name(name)['device']
            if _re.search('B', device)    is not None: ec[name] = 'boma-b.txt'
            elif _re.search('QF', device) is not None: ec[name] = 'boma-qf.txt'
            elif _re.search('QD', device) is not None: ec[name] = 'boma-qd.txt'
            elif _re.search('QS', device) is not None: ec[name] = 'boma-qs.txt'
            elif _re.search('SF', device) is not None: ec[name] = 'boma-sf.txt'
            elif _re.search('SD', device) is not None: ec[name] = 'boma-sd.txt'
            elif _re.search('CH', device) is not None: ec[name] = 'boma-ch.txt'
            elif _re.search('CV', device) is not None: ec[name] = 'boma-cv.txt'
            elif _re.search('InjK', device) is not None: ec[name] = 'bopm-injk.txt'
            elif _re.search('EjeK', device)  is not None: ec[name] = 'bopm-ejek.txt'

        return ec
