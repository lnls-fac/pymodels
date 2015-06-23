
from . import lattice as _lattice
from . import accelerator as _accelerator
from . import record_names


create_accelerator = _accelerator.create_accelerator

# -- default accelerator values for SI_V07 --
energy               = _lattice._energy
harmonic_number      = _lattice._harmonic_number
default_cavity_on    = _accelerator._default_cavity_on
default_radiation_on = _accelerator._default_cavity_on
default_vchamber_on  = _accelerator._default_vchamber_on
default_optics_mode  = _lattice._default_optics_mode.label
lattice_version      = 'SI_V07'
lattice_symmetry     = _lattice._lattice_symmetry
family_data          = _lattice._family_data
family_mapping       = _lattice._family_mapping
global_coupling      = 0.01     # expected corrected value
average_pressure     = 1.333e-9 # average pressure [mbar]
