
from .lattice import default_optics_mode
from .lattice import energy

from .accelerator import default_vchamber_on
from .accelerator import default_radiation_on
from .accelerator import accelerator_data
from .accelerator import create_accelerator

from .families import get_family_data
from .families import family_mapping
from .families import get_section_name_mapping

from . import virtual_accel_interface
device_names  = virtual_accel_interface.TBDeviceNames()
del virtual_accel_interface

# -- default accelerator values for TB_V01 --
lattice_version   = accelerator_data['lattice_version']
get_device_names  = device_names.get_device_names
get_magnet_names  = device_names.get_magnet_names