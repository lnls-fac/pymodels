from . import lattice as _lattice
from . import accelerator as _accelerator
from . import record_names

create_accelerator = accelerator.create_accelerator

# -- default accelerator values for LI_V00 --

energy = _lattice._energy
default_optics_mode  = _lattice._default_optics_mode.label
lattice_version      = 'LI_V00'
family_data          = _lattice._family_data
