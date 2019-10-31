
from siriuspy.namesys import join_name as _join_name

from . import families as _fams


def get_control_system_data(lattice, fam_data=None):
    fam_data = fam_data or _fams.get_family_data(lattice)
    fam_map = _fams.family_mapping
    names = dict()

    # Individual elements
    mags = set(_fams.families_quadrupoles())
    mags.update(_fams.families_pulsed_magnets())
    mags.update(['CH', 'CV'])
    for mag in sorted(mags):
        dta = fam_data[mag]
        idxs = dta['index']
        subs = dta['subsection']
        insts = dta['instance']
        for idx, sub, inst in zip(idxs, subs, insts):
            dis = 'PM' if 'Sept' in mag else 'MA'
            name = _join_name(sec='TS', dis=dis, sub=sub, idx=inst, dev=mag)
            names[name] = {'index': idx, 'magnet_type': fam_map[mag]}
