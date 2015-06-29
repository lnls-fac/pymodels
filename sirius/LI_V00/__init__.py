
from . import lattice as _lattice
from . import accelerator as _accelerator
from . import families as _families
from . import record_names

accelerator_data = _accelerator.accelerator_data
create_accelerator = accelerator.create_accelerator

# -- default accelerator values for LI_V00 --

energy = _lattice._energy
single_bunch_charge     = _lattice._single_bunch_charge
multi_bunch_charge      = _lattice._multi_bunch_charge
pulse_duration_interval = _lattice._pulse_duration_interval
default_optics_mode     = _lattice._default_optics_mode.label
lattice_version         = accelerator_data['lattice_version']
#emittance               = accelerator_data['emittance']
#energy_spread           = accelerator_data['energy_spread']
family_data             = _families._family_data
