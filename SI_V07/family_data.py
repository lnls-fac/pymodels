# we have to decide what would go in here and what would go into database tables

import numpy as _np
import pyaccel as _pyaccel
from . import accelerator as _accelerator
from . import excitation_curves as _excs


class _Families(object):

    def __repr__(self):
        names = ', '.join(self._get_family_names())
        return "Families(" + names + ")"

    def __str__(self):
        names = '\n'.join(self._get_family_names())
        return names

    def _get_family_names(self):
        names = []
        for name in dir(self):
            if not name.startswith('_'):
                names.append("'" + name + "'")

        return names


class _Family(object):

    def __repr__(self):
        return "Family(fam_name='" + self.fam_name + "')"

    def __str__(self):
        width = 15
        fmt = "{0:>" + str(width) + "}: {1}"
        text = []
        for name in dir(self):
            if not name.startswith('_'):
                line = fmt.format(name, getattr(self, name).__str__())
                text.append(line)

        return '\n'.join(text)


_the_ring = _accelerator.create_accelerator()

b1 = _Family()
b1.fam_name = 'b1'
b1.pyaccel_indices = None
b1.hw_units  = 'ampere'
b1.ph_units  = 'GeV'
b1.hw_2_ph   = _excs.dipoles_b1
b1.ph_2_hw   = (0,0.1)
b1.hw_limits = (-10,10)

b2 = _Family()
b2.fam_name = 'b2'
b2.pyaccel_indices = None #_np.reshape(_pyaccel.lattice.findcells(_the_ring, 'fam_name', 'b2'), (3,-1))
b2.hw_units = 'ampere'
b2.ph_units = 'GeV'
b2.hw_2_ph  = (0,10)
b2.ph_2_hw  = (0,0.1)
b2.hw_limits = (-10,10)

bpmx = _Family()
bpmx.fam_name = 'bpmx'
bpmx.pyaccel_indices = None #_np.reshape(_pyaccel.lattice.findcells(_the_ring, 'fam_name', 'bpm'), (3,-1))
bpmx.hw_units = 'mm'
bpmx.ph_units = 'm'
bpmx.hw_2_ph  = (0,0.001)
bpmx.ph_2_hw  = (0,1000)

bpmy = _Family()
bpmy.fam_name = 'bpmy'
bpmy.pyaccel_indices = None #_np.reshape(_pyaccel.lattice.findcells(_the_ring, 'fam_name', 'bpm'), (3,-1))
bpmy.hw_units = 'mm'
bpmy.ph_units = 'm'
bpmy.hw_2_ph  = (0,0.001)
bpmy.ph_2_hw  = (0,1000)

families = _Families() #(b1, b2, bpmx, bpmy)
loc = locals()
for name in dir():
    if isinstance(loc[name], _Family):
        families.__dict__[name] = loc[name]

def get_family_data():
    return families
