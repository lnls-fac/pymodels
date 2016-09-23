
from . import lattice as _lattice
from . import accelerator as _accelerator
from . import families as _families
from . import device_names
from . import excitation_curves
from . import power_supplies
from . import pulsed_magnets


accelerator_data = _accelerator.accelerator_data
create_accelerator = _accelerator.create_accelerator

# -- default accelerator values for LI_V00 --
energy                      = _lattice._energy
single_bunch_charge         = _lattice._single_bunch_charge
multi_bunch_charge          = _lattice._multi_bunch_charge
single_bunch_pulse_duration = _lattice._single_bunch_pulse_duration
multi_bunch_pulse_duration  = _lattice._multi_bunch_pulse_duration
frequency                   = _lattice._frequency
default_optics_mode         = _lattice._default_optics_mode.label
lattice_version             = accelerator_data['lattice_version']
get_family_data             = _families.get_family_data
family_mapping              = _families._family_mapping
