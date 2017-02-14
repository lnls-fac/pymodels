
from . import families as _families
import sirius.naming_system as _naming_sys

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
    'AP': ['Chrom','CurrLT','Size','Emitt'],
    'TI': ['STDMOE']
}
_disciplines = sorted( _el_names.keys() | _fam_names.keys() | _glob_names.keys())

##### Excitation Curves #######
_excitation_curves_mapping = {
    ('B',)    : 'boma-b.txt',
    ('QF',)   : 'boma-qf.txt',
    ('QD',)   : 'boma-qd.txt',
    ('QS',)   : 'boma-qs.txt',
    ('SF',)   : 'boma-sf.txt',
    ('SD',)   : 'boma-sd.txt',
    ('CH',)   : 'boma-ch.txt',
    ('CV',)   : 'boma-cv.txt',
    ('InjK',) : 'bopm-injk.txt',
    ('EjeK',) : 'bopm-ejek.txt',
}

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
        ##### Excitation Curves #######
        self.excitation_curves_mapping = _excitation_curves_mapping
        ##### Pulsed Magnets #######
        self.pulse_curve_mapping = _pulse_curve_mapping
        ##### Family Data Function ######
        self.get_family_data = _families.get_family_data
