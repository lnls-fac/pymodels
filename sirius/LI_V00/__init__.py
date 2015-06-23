from . import lattice as _lattice
from . import accelerator as _accelerator
from . import record_names

create_accelerator = accelerator.create_accelerator

# -- default accelerator values for LI_V00 --

energy = _lattice._energy
single_bunch_charge     = _lattice._single_bunch_charge
multi_bunch_charge      = _lattice._multi_bunch_charge
pulse_duration_interval = _lattice._pulse_duration_interval
default_optics_mode  = _lattice._default_optics_mode.label
lattice_version      = 'LI_V00'
family_data          = _lattice._family_data
emittance            = _lattice._emittance
global_coupling      = 1.0 # "round" beam
