from . import lattice as _lattice
from . import accelerator as _accelerator
from . import record_names

create_accelerator = accelerator.create_accelerator

# -- default accelerator values for BO_V901 --

energy = _lattice._energy
harmonic_number      = _lattice._harmonic_number
default_cavity_on    = _accelerator._default_cavity_on
default_radiation_on = _accelerator._default_cavity_on
default_vchamber_on  = _accelerator._default_vchamber_on
default_optics_mode  = _lattice._default_optics_mode.label
lattice_version      = 'BO_V901'
lattice_symmetry     = _lattice._lattice_symmetry
family_data          = _lattice._family_data
global_coupling      = 0.0002 # expected corrected value
average_pressure     = 1.5e-8 # average pressure [mbar]
