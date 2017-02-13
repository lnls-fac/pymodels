
from . import families as _families
import sirius.naming_system as _naming_sys

_section = 'LI'
_el_names = { # All these Family names must be defined in family_data dictionary
    'DI': _families.families_di(),
    'RF': _families.families_rf(),
    'PS': ['Slnd01','Slnd02','Slnd03','Slnd04','Slnd05','Slnd06','Slnd07',
           'Slnd08','Slnd09','Slnd10','Slnd11','Slnd12','Slnd13',
           'QD1','QD2','QF3','CH','CV','Spect','Lens'],
    'MA': ['Slnd01','Slnd02','Slnd03','Slnd04','Slnd05','Slnd06','Slnd07',
           'Slnd08','Slnd09','Slnd10','Slnd11','Slnd12','Slnd13','Slnd14',
           'Slnd15','Slnd16','Slnd17','Slnd18','Slnd19','Slnd20','Slnd21',
           'QF1','QF2','QD1','QD2','QF3','CH','CV','Spect','Lens'],
    'TI': ['EGun'],
    'EG': ['EGun']
}
_fam_names = { # All these Family names must be defined in family_data dictionary
    'PS': ['Slnd14','Slnd15','Slnd16','Slnd17','Slnd18','Slnd19','Slnd20',
           'Slnd21','QF1','QF2'],
    'MA': ['Slnd14','Slnd15','Slnd16','Slnd17','Slnd18','Slnd19','Slnd20',
           'Slnd21','QF1','QF2'],
}
_glob_names = dict() # These Family names can be any name
_disciplines = sorted( _el_names.keys() | _fam_names.keys() | _glob_names.keys())

##### Excitation Curves #######
_excitation_curves_mapping = {
    ('QD','QF3'): 'lima-q.txt',
    ('QF',):      'lima-famqf.txt',
    ('CH',):      'lima-ch.txt',
    ('CV',):      'lima-cv.txt',
    ('Spect',):   'lima-spect.txt',
}

##### Pulsed Magnets #######
_pulse_curve_mapping= dict()

class LIDeviceNames(_naming_sys.DeviceNames):

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
