
from . import lattice as _lattice
from . import accelerator as _accelerator
from . import families as _families
from . import record_names

accelerator_data = _accelerator.accelerator_data
create_accelerator = accelerator.create_accelerator

# -- default accelerator values for TS_V400 --

energy = _lattice._energy
default_radiation_on = _accelerator._default_radiation_on
default_vchamber_on  = _accelerator._default_vchamber_on
default_optics_mode  = _lattice._default_optics_mode.label
lattice_version      = 'TS_V400'
family_data          = _families._family_data
