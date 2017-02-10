
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

##### Pulsed Magnets #######
_pulse_curve_mapping= dict()

class LIDeviceNames(_naming_sys.DeviceNames):

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
        magnets = _device_names.get_magnet_names(accelerator)

        ec = dict()
        for name in magnets:
            dev = _naming_system.split_name(name)['device']
            if dev.startswith(('QD','QF3')):
                ec[name] = 'lima-q.txt'
            elif dev.startswith('QF'):
                ec[name] = 'lima-famqf.txt'
            elif dev.startswith('CH'):
                ec[name] = 'lima-ch.txt'
            elif dev.startswith('CV'):
                ec[name] = 'lima-cv.txt'
            elif dev.startswith('Spect'):
                ec[name] = 'lima-spect.txt'

            # elif dev.startswith('Slnd') and (int(dev[-2:]) >= 14):
            #     ec[name] = 'lima-famslnd.txt'
            # elif dev.startswith('Slnd') and (int(dev[-2:]) <= 13):
            #     ec[name] = 'lima-indslnd.txt'
            # elif dev.startswith('Lens'):
            #     ec[name] = 'lima-lens.txt'
        return ec
