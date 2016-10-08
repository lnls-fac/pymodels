
from . import lattice as _lattice
from . import accelerator as _accelerator
from . import families as _families
from . import device_names as _device_names
from . import excitation_curves
from . import power_supplies
from . import pulsed_magnets


accelerator_data = _accelerator.accelerator_data
create_accelerator = _accelerator.create_accelerator

# -- default accelerator values for SI_V20_01 --
energy               = _lattice._energy
harmonic_number      = _lattice._harmonic_number
default_cavity_on    = _accelerator._default_cavity_on
default_radiation_on = _accelerator._default_radiation_on
default_vchamber_on  = _accelerator._default_vchamber_on
default_optics_mode  = _lattice._default_mode + '.' + _lattice._default_version
lattice_symmetry     = _lattice._lattice_symmetry
lattice_version      = accelerator_data['lattice_version']
get_family_data      = _families.get_family_data
get_device_names     = _device_names.get_device_names
family_mapping       = _families._family_mapping