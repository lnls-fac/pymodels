
from siriuspy.namesys import join_name as _join_name

from . import families as _fams


def get_control_system_data(lattice, fam_data=None):
    fam_data = fam_data or _fams.get_family_data(lattice)
    fam_map = _fams.family_mapping
    names = dict()

    # Individual elements
    mags = set(_fams.families_quadrupoles())
    mags.discard('QF2L')
    mags.update(['CH', 'CV'])
    mags.add('InjSept')
    for mag in sorted(mags):
        dta = fam_data[mag]
        idxs = dta['index']
        subs = dta['subsection']
        insts = dta['instance']
        for idx, sub, inst in zip(idxs, subs, insts):
            sec = 'LI' if mag.endswith('L') else 'TB'
            dev = mag[:-1] if mag.endswith('L') else mag
            dis = 'PM' if dev.startswith('InjSept') else 'MA'
            name = _join_name(sec=sec, dis=dis, sub=sub, idx=inst, dev=dev)
            names[name] = {'index': idx, 'magnet_type': fam_map[mag]}

    # Families elements
    mags = ['QF2L', ]
    for mag in mags:
        indv = list()
        dta = fam_data[mag]
        idxs = dta['index']
        subs = dta['subsection']
        insts = dta['instance']
        dev = mag[:-1]
        for sub, inst in zip(subs, insts):
            indv.append(
                _join_name(sec='LI', dis='MA', sub=sub, idx=inst, dev=dev))
        name = _join_name(sec='LI', dis='MA', sub='Fam', dev=dev)
        names[name] = {
            'magnets': indv, 'index': idxs, 'magnet_type': fam_map[mag]}
    return names
