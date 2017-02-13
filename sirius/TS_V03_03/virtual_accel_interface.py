
from . import families as _families
import sirius.naming_system as _naming_sys

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

##### Excitation Curves #######
_excitation_curves_mapping = {
    ('B',)    : 'tsma-b.txt',
    ('QF1',)  : 'tsma-q14.txt',
    ('QD',)   : 'tsma-q14.txt',
    ('QF',)   : 'tsma-q20.txt',
    ('CH',)   : 'tsma-ch.txt',
    ('CV',)   : 'tsma-cv.txt',
    ('EjeSF',): 'tspm-ejesf.txt',
    ('EjeSG',): 'tspm-ejesg.txt',
    ('InjSG',): 'tspm-injsg.txt',
    ('InjSF',): 'tspm-injsf.txt',
}

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
        ##### Excitation Curves #######
        self.excitation_curves_mapping = _excitation_curves_mapping
        ##### Pulsed Magnets #######
        self._pulse_curve_mapping = _pulse_curve_mapping
        ##### Family Data Function ######
        self.get_family_data = _families.get_family_data
