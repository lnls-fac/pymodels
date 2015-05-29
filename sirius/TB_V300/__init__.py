from . import lattice as _lattice
from . import accelerator as _accelerator
from . import record_names

create_accelerator = accelerator.create_accelerator

# -- default accelerator values for TB_V300 --

energy = _lattice._energy
default_radiation_on = _accelerator._default_radiation_on
default_vchamber_on  = _accelerator._default_vchamber_on
default_optics_mode  = _lattice._default_optics_mode.label
lattice_version      = 'TB_V300'
family_data = _lattice._family_data
