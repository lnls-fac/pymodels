
from siriuspy.namesys import join_name as _join_name
import pyaccel as _pyaccel


_family_segmentation = {
    'B-1': 20, 'B-2': 20, 'B': 20, 'QF': 2, 'QD': 1, 'SD': 1, 'QS': 1,
    'SF': 1, 'CH': 1, 'CV': 1,
    'BPM': 1, 'Scrn': 1, 'DCCT': 1, 'TunePkup': 1, 'TuneShkr': 1, 'GSL': 1,
    'P5Cav': 1, 'start': 1, 'BEND': 14,
    'InjKckr': 1, 'EjeKckr': 1
    }

_discipline_mapping = {
    'B-1': 'PS',
    'B-2': 'PS',
    'QF': 'PS',
    'QD': 'PS',
    'QS': 'PS',
    'SD': 'PS',
    'SF': 'PS',
    'CH': 'PS',
    'CV': 'PS',
    'InjKckr': 'PU',
    'EjeKckr': 'PU',
    'BPM': 'DI',
    'DCCT': 'DI',
    'Scrn': 'DI',
    'TunePkup': 'DI',
    'TuneShkr': 'DI',
    'P5Cav': 'RF',
    }

family_mapping = {
    'B': 'dipole',
    'B-1': 'dipole',
    'B-2': 'dipole',

    'QF': 'quadrupole',
    'QD': 'quadrupole',
    'QS': 'skew_quadrupole',

    'SD': 'sextupole',
    'SF': 'sextupole',

    'InjKckr': 'pulsed_magnet',
    'EjeKckr': 'pulsed_magnet',

    'BPM': 'bpm',
    'DCCT':    'beam_current_monitor',
    'Scrn':    'beam_profile_monitor',
    'TunePkup':   'tune_pickup',
    'TuneShkr':   'tune_shaker',

    'CH': 'horizontal_corrector',
    'CV': 'vertical_corrector',

    'P5Cav': 'rf_cavity',
    }


def families_dipoles():
    """."""
    return ['B']


def families_quadrupoles():
    """."""
    return ['QF', 'QD']


def families_sextupoles():
    """."""
    return ['SF', 'SD']


def families_horizontal_correctors():
    """."""
    return ['CH']


def families_vertical_correctors():
    """."""
    return ['CV']


def families_skew_correctors():
    """."""
    return ['QS']


def families_rf():
    """."""
    return ['P5Cav']


def families_pulsed_magnets():
    """."""
    return ['InjKckr', 'EjeKckr']


def families_di():
    """."""
    return ['DCCT', 'BPM', 'Scrn', 'TunePkup', 'TuneShkr', 'GSL']


def get_section_name_mapping(lattice):
    """."""
    lat = lattice[:]
    section_map = ['' for i in range(len(lat))]

    # find where the nomenclature starts counting and shift the lattice:
    start = _pyaccel.lattice.find_indices(lat, 'fam_name', 'start')[0]
    b1 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B')
    if b1[0] > start:
        ind_shift = (b1[-1] + 1)  # Next element of last b1
    else:
        for i in b1[::-1]:  # except there is a b1 before start
            if i < start:
                ind_shift = i + 1
                break
    lat = _pyaccel.lattice.shift(lat, ind_shift)

    # Find indices important to define the change of the names of
    # the subsections
    b = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B')
    qf = _pyaccel.lattice.find_indices(lat, 'fam_name', 'QF')
    b_nrsegs = len(b)//50

    # divide the ring in 50 sectors defined by the b1 dipoles:
    Sects = []
    ini = 0
    for i in range(len(b)//b_nrsegs):
        fim = b[(i+1)*b_nrsegs-1] + 1
        Sects.append(list(range(ini, fim)))
        ini = fim

    # Names of the subsections:
    sub_secs = ['U', 'D']

    for i, sec in enumerate(Sects, 1):
        # conditions that define change in subsection name:
        # define changes to ''
        sec_b = [x for x in b if sec[0] <= x <= sec[-1]]
        relev_inds = [sec_b[-1]]
        # define changes to '' and D
        sec_qf = [x for x in qf if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_qf[-1]]
        relev_inds.sort()
        # fill the section_map variable
        ref = 0
        for j in sec:
            section_map[(ind_shift+j) % len(lat)] = "{0:02d}".format(i)
            section_map[(ind_shift+j) % len(lat)] += sub_secs[ref]
            if j >= relev_inds[ref]:
                ref += 1

    return section_map


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name.

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice, 'fam_name')
    section_map = get_section_name_mapping(lattice)

    # Fill the data dictionary with index info
    data = {}
    for key, idx in latt_dict.items():
        nr = _family_segmentation.get(key)
        if nr is None:
            continue
        # Create a list of lists for the indexes
        data[key] = [idx[i*nr:(i+1)*nr] for i in range(len(idx)//nr)]

    # quadrupoles knobs for optics correction
    idx = []
    fams = ['QF', 'QD']
    for fam in fams:
        idx.extend(data[fam])
    data['QN'] = sorted(idx, key=lambda x: x[0])

    # sbs - sextupoles knobs for optics correction
    idx = []
    fams = ['SD', 'SF']
    for fam in fams:
        idx.extend(data[fam])
    data['SN'] = sorted(idx, key=lambda x: x[0])

    # Dipole Families for power supplies
    idx = []
    fams = ['B']
    for fam in fams:
        idx.extend(data[fam])
    data['B-1'] = sorted(idx, key=lambda x: x[0])
    data['B-2'] = sorted(idx, key=lambda x: x[0])

    # ## Now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [section_map[i[0]] for i in idx]

        # find out if there are more than one element per section and
        # attribute a number to it
        num = len(secs)*['']
        if len(secs) > 1:
            j = 1
            if secs[0] == secs[1]:
                num[0] = '{0:d}'.format(j)
                j += 1
            for i in range(1, len(secs)-1):
                if secs[i] == secs[i+1] or secs[i] == secs[i-1]:
                    num[i] = '{0:d}'.format(j)

                if secs[i] == secs[i+1]:
                    j += 1
                else:
                    j = 1

            if secs[-1] == secs[-2]:
                num[-1] = '{0:d}'.format(j)

        new_data[key] = {'index': idx, 'subsection': secs, 'instance': num}

    # get control system devname
    for key in new_data:
        if key not in _discipline_mapping:
            continue
        dis = _discipline_mapping[key]
        dta = new_data[key]
        devnames = []
        subs = dta['subsection']
        insts = dta['instance']
        for sub, inst in zip(subs, insts):
            devnames.append(
                _join_name(sec='BO', dis=dis, sub=sub, idx=inst, dev=key))
        new_data[key]['devnames'] = devnames

    # girders
    girder = get_girder_data(lattice)
    if girder is not None:
        new_data['girder'] = girder

    return new_data


def get_girder_data(lattice):
    """."""
    data = []
    girders = _pyaccel.lattice.find_indices(lattice, 'fam_name', 'girder')
    if not girders:
        return None

    idx = list(range(girders[-1], len(lattice))) + list(range(girders[0]))
    data.append(dict({'index': idx}))

    gir = girders[1:-1]
    gir_ini = gir[0::2]
    gir_end = gir[1::2]
    for ini, end in zip(gir_ini, gir_end):
        idx = list(range(ini, end+1))
        data.append(dict({'index': idx}))

    return data
