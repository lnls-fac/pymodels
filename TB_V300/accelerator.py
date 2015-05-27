import pyaccel as _pyaccel
from . import lattice as _lattice

_default_radiation_on = False
_default_vchamber_on = False

def create_accelerator():

    accelerator = _pyaccel.accelerator.Accelerator(
        lattice=_lattice.create_lattice(),
        energy=_lattice._energy,
        radiation_on=_default_radiation_on,
        vchamber_on=_default_vchamber_on )

    return accelerator
