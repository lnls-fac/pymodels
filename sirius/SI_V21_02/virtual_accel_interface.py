
from . import families as _families
import sirius.naming_system as _naming_sys

_section = 'SI'
_el_names = { # All these Family names must be defined in family_data dictionary
    'DI': _families.families_di(),
    'RF': _families.families_rf(),
    'MA': (_families.families_dipoles() +
           _families.families_quadrupoles() +
           _families.families_sextupoles() +
           _families.families_horizontal_correctors() +
           _families.families_vertical_correctors() +
           _families.families_skew_correctors()
           ),
    'PS': (_families.families_quadrupoles() +
           _families.families_horizontal_correctors() +
           _families.families_vertical_correctors() +
           _families.families_skew_correctors()
           ),
    'PM': _families.families_pulsed_magnets(),
    'PU': _families.families_pulsed_magnets(),
    'TI': _families.families_pulsed_magnets(),
}
_fam_names = { # All these Family names must be defined in family_data dictionary
    'PS': (['B1B2-1','B1B2-2']+
           _families.families_quadrupoles() +
           _families.families_sextupoles()
          ),
    'MA': (['B1B2-1','B1B2-2'] +
           _families.families_quadrupoles() +
           _families.families_sextupoles()
          ),
    'DI': ['BPM']
}
_glob_names = {# These Family names can be any name
    'AP': ['ChromX','ChromY','Lifetime','BLifetime','SigX','SigY','SigS','EmitX','EmitY'],
}
_disciplines = sorted( _el_names.keys() | _fam_names.keys() | _glob_names.keys())

##### Excitation Curves #######
_excitation_curves_mapping = {
    ('B1',)                     : 'sima-b1.txt',
    ('B2',)                     : 'sima-b2.txt',
    ('BC',)                     : 'sima-bc.txt',
    ('QD',)                     : 'sima-q14.txt',
    ('QFA','Q1','Q2','Q3','Q4') : 'sima-q20.txt',
    ('QFB','QFP')               : 'sima-q30.txt',
    ('QS',)                     : 'sima-qs.txt',
    ('SF',)                     : 'sima-sf.txt',
    ('SD',)                     : 'sima-sd.txt',
    ('CH',)                     : 'sima-ch.txt',
    ('CV',)                     : 'sima-cv.txt',
    ('FCH',)                    : 'sima-ch.txt',
    ('FCV',)                    : 'sima-cv.txt',
    ('InjDpK',)                 : 'sipm-injdpk.txt',
    ('InjNLK',)                 : 'sipm-injnlk.txt',
}

##### Pulsed Magnets #######
_pulse_curve_mapping= {
    'InjDpK':'sipm-injdpk-pulse.txt',
    'InjNLK':'sipm-injnlk-pulse.txt',
}

class SIDeviceNames(_naming_sys.DeviceNames):

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
