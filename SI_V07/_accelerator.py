import pyaccel as _pyaccel
from . import _lattice

_default_cavity_on = False
_default_radiation_on = False
_default_vchamber_on = False

def create_accelerator():

    accelerator = _pyaccel.accelerator.Accelerator(
        elements=_lattice.create_lattice(),
        energy=_lattice._energy,
        harmonic_number=_lattice._harmonic_number,
        cavity_on=_default_cavity_on,
        radiation_on=_default_radiation_on,
        vchamber_on=_default_vchamber_on)

    return accelerator
