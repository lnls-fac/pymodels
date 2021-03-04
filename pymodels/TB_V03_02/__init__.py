"""TB_V03_02 Model."""

from .lattice import default_optics_mode
from .lattice import energy

from .accelerator import default_vchamber_on
from .accelerator import default_radiation_on
from .accelerator import accelerator_data
from .accelerator import create_accelerator

from .families import get_family_data
from .families import family_mapping
from .families import get_section_name_mapping

lattice_version = accelerator_data['lattice_version']
