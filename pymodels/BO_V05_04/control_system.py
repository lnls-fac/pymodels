
from siriuspy.namesys import join_name as _join_name

from . import families as _fams


def get_control_system_data(lattice, fam_data=None):
    fam_data = fam_data or _fams.get_family_data(lattice)
    fam_map = _fams.family_mapping
    names = dict()

    # Individual elements
    mags = set(_fams.families_horizontal_correctors())
    mags |= set(_fams.families_vertical_correctors())
    mags |= set(_fams.families_skew_correctors())
    mags |= set(_fams.families_pulsed_magnets())
    for mag in sorted(mags):
        dta = fam_data[mag]
        idxs = dta['index']
        subs = dta['subsection']
        insts = dta['instance']
        for idx, sub, inst in zip(idxs, subs, insts):
            dis = 'PM' if mag.endswith('Kckr') else 'MA'
            name = _join_name(sec='BO', dis=dis, sub=sub, idx=inst, dev=mag)
            names[name] = {'index': idx, 'magnet_type': fam_map[mag]}

    # Families elements
    mags = set(_fams.families_quadrupoles())
    mags |= set(_fams.families_sextupoles())
    for mag in mags:
        indv = list()
        dta = fam_data[mag]
        idxs = dta['index']
        subs = dta['subsection']
        insts = dta['instance']
        for sub, inst in zip(subs, insts):
            indv.append(
                _join_name(sec='BO', dis='MA', sub=sub, idx=inst, dev=mag))
        name = _join_name(sec='BO', dis='MA', sub='Fam', dev=mag)
        names[name] = {
            'magnets': indv, 'index': idxs, 'magnet_type': fam_map[mag]}
    return names
