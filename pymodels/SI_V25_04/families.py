"""Element family definitions."""

import pyaccel as _pyaccel
from siriuspy.namesys import join_name as _join_name

_NR_B1 = 40
_NR_B2 = 40

_family_number_of_elements = {
    'B1': _NR_B1, 'B2': _NR_B2, 'BC': 20,
    'QFA': 10, 'QDA': 10,
    'QFB': 20, 'QDB1': 20, 'QDB2': 20,
    'QFP': 10, 'QDP1': 10, 'QDP2': 10,
    'Q1': 40, 'Q2': 40, 'Q3': 40, 'Q4': 40,
    'SDA0': 10, 'SDB0': 20, 'SDP0': 10,
    'SDA1': 10, 'SDB1': 20, 'SDP1': 10,
    'SDA2': 10, 'SDB2': 20, 'SDP2': 10,
    'SDA3': 10, 'SDB3': 20, 'SDP3': 10,
    'SFA0': 10, 'SFB0': 20, 'SFP0': 10,
    'SFA1': 10, 'SFB1': 20, 'SFP1': 10,
    'SFA2': 10, 'SFB2': 20, 'SFP2': 10,
    'DCCT': 2, 'ScrapH': 1, 'ScrapV': 1,
    'BPM': 160, 'GSL15': 1, 'GSL07': 1, 'GBPM': 1,
    'BbBPkup': 1, 'BbBKckrH': 1, 'BbBKckrV': 1, 'BbBKckrL': 1,
    'TuneShkrH': 1, 'TuneShkrV': 1, 'TunePkupH': 1, 'TunePkupV': 1,
    'FC1': 58, 'FC1FF': 2, 'FC2': 20, 'QS': 100, 'CH': 120, 'CV': 160,
    'SRFCav': 1, 'H3Cav': 1, 'start': 1,
    'InjDpKckr': 1, 'InjNLKckr': 1, 'PingH': 1, 'PingV': 1,
    'APU22': 3, 'APU58': 1, 'DELTA52': 1, 
    'IVU18': 2, 'VPU29': 2,
    'IDBPM': 2,
    'IDC1': 2, 'IDC4': 4, 'IDC5': 4,
    'IDQS': 2,
    }


_discipline_mapping = {
    'B1B2-1': 'PS',
    'B1B2-2': 'PS',
    'QFA': 'PS',
    'QDA': 'PS',
    'QDB2': 'PS',
    'QFB': 'PS',
    'QDB1': 'PS',
    'QDP2': 'PS',
    'QFP': 'PS',
    'QDP1': 'PS',
    'Q1': 'PS',
    'Q2': 'PS',
    'Q3': 'PS',
    'Q4': 'PS',
    'SDA0': 'PS',
    'SDB0': 'PS',
    'SDP0': 'PS',
    'SDA1': 'PS',
    'SDB1': 'PS',
    'SDP1': 'PS',
    'SDA2': 'PS',
    'SDB2': 'PS',
    'SDP2': 'PS',
    'SDA3': 'PS',
    'SDB3': 'PS',
    'SDP3': 'PS',
    'SFA0': 'PS',
    'SFB0': 'PS',
    'SFP0': 'PS',
    'SFA1': 'PS',
    'SFB1': 'PS',
    'SFP1': 'PS',
    'SFA2': 'PS',
    'SFB2': 'PS',
    'SFP2': 'PS',
    'InjNLKckr': 'PU',
    'InjDpKckr': 'PU',
    'PingH': 'PU',
    'PingV': 'PU',
    'BPM': 'DI',
    'IDBPM': 'DI',
    'DCCT': 'DI',
    'ScrapH': 'DI',
    'ScrapV': 'DI',
    'GSL15': 'DI',
    'GSL07': 'DI',
    'GBPM': 'DI',
    'BbBPkup': 'DI',
    'BbBKckrH': 'DI',
    'BbBKckrV': 'DI',
    'BbBKckrL': 'DI',
    'TuneShkrH': 'DI',
    'TuneShkrV': 'DI',
    'TunePkupH': 'DI',
    'TunePkupV': 'DI',
    'FC1': 'PS',
    'FC2': 'PS',
    'FCH': 'PS',
    'FCV': 'PS',
    'FFCH': 'PS',
    'FFCV': 'PS',
    'CH': 'PS',
    'CV': 'PS',
    'IDCH': 'PS',
    'IDCV': 'PS',
    'QS': 'PS',
    'IDQS': 'PS',
    'SRFCav': 'RF',
    'H3Cav': 'RF',
    'APU22': 'ID',
    'APU58': 'ID',
    'DELTA52': 'ID',
    'WIG180': 'ID',
    'PAPU50': 'ID',
    'IVU18': 'ID',
    'VPU29': 'ID',
    }


family_mapping = {

    'B1': 'dipole',
    'B2': 'dipole',
    'BC': 'dipole',
    'B1B2-1': 'dipole',
    'B1B2-2': 'dipole',

    'QFA': 'quadrupole',
    'QDA': 'quadrupole',
    'QDB2': 'quadrupole',
    'QFB': 'quadrupole',
    'QDB1': 'quadrupole',
    'QDP2': 'quadrupole',
    'QFP': 'quadrupole',
    'QDP1': 'quadrupole',
    'Q1': 'quadrupole',
    'Q2': 'quadrupole',
    'Q3': 'quadrupole',
    'Q4': 'quadrupole',

    'SDA0': 'sextupole',
    'SDB0': 'sextupole',
    'SDP0': 'sextupole',
    'SDA1': 'sextupole',
    'SDB1': 'sextupole',
    'SDP1': 'sextupole',
    'SDA2': 'sextupole',
    'SDB2': 'sextupole',
    'SDP2': 'sextupole',
    'SDA3': 'sextupole',
    'SDB3': 'sextupole',
    'SDP3': 'sextupole',
    'SFA0': 'sextupole',
    'SFB0': 'sextupole',
    'SFP0': 'sextupole',
    'SFA1': 'sextupole',
    'SFB1': 'sextupole',
    'SFP1': 'sextupole',
    'SFA2': 'sextupole',
    'SFB2': 'sextupole',
    'SFP2': 'sextupole',

    'InjNLKckr': 'pulsed_magnet',
    'InjDpKckr': 'pulsed_magnet',
    'PingH': 'pulsed_magnet',
    'PingV': 'pulsed_magnet',

    'BPM': 'bpm',
    'IDBPM': 'bpm',
    'DCCT': 'dcct_to_measure_beam_current',
    'ScrapH': 'horizontal_scraper',
    'ScrapV': 'vertical_scraper',
    'GSL15': 'generic_stripline_(lambda/4)',
    'GSL07': 'generic_stripline_(lambda/8)',
    'GBPM': 'general_bpm',
    'BbBPkup': 'bunch-by-bunch_pickup',
    'BbBKckrH': 'horizontal_bunch-by-bunch_shaker',
    'BbBKckrV': 'vertical_bunch-by-bunch_shaker',
    'BbBKckrL': 'longitudinal_bunch-by-bunch_shaker',
    'TuneShkrH': 'horizontal_tune_shaker',
    'TuneShkrV': 'vertical_tune_shaker',
    'TunePkupH': 'horizontal_tune_pickup',
    'TunePkupV': 'vertical_tune_pickup',

    'FC1': 'fast_corrector',
    'FC2': 'fast_corrector',
    'FCH': 'fast_horizontal_corrector',
    'FCV': 'fast_vertical_corrector',
    'FFCH': 'feedforward_horizontal_corrector',
    'FFCV': 'feedforward_vertical_corrector',

    'CH': 'slow_horizontal_corrector',
    'CV': 'slow_vertical_corrector',
    'IDCH': 'id_horizontal_corrector',
    'IDCV': 'id_vertical_corrector',
    'IDQS': 'id_skew_quadrupole',

    'QS': 'skew_quadrupole',

    'SRFCav': 'superconducting_rf_cavity',
    'H3Cav': 'third_harmonic_rf_cavity',
    'APU22': 'insertion_device',
    'APU58': 'insertion_device',
    'DELTA52': 'insertion_device',
    'WIG180': 'insertion_device',
    'PAPU50': 'insertion_device',
    'IVU18': 'insertion_device',
    'VPU29': 'insertion_device',
    }


def families_dipoles():
    """Return dipole families."""
    return ['B1', 'B2', 'BC', ]


def families_quadrupoles():
    """Return quadrupole families."""
    return ['QFA', 'QDA', 'QFB', 'QDB1', 'QDB2', 'QFP',
            'QDP1', 'QDP2', 'Q1', 'Q2', 'Q3', 'Q4', ]


def families_sextupoles():
    """Return sextupole families."""
    return [
        'SDA0', 'SDB0', 'SDP0',
        'SDA1', 'SDB1', 'SDP1',
        'SDA2', 'SDB2', 'SDP2',
        'SDA3', 'SDB3', 'SDP3',
        'SFA0', 'SFB0', 'SFP0',
        'SFA1', 'SFB1', 'SFP1',
        'SFA2', 'SFB2', 'SFP2', ]


def families_horizontal_correctors():
    """Return horizontal corrector families."""
    return ['FCH', 'FFCH', 'CH', 'IDCH']


def families_vertical_correctors():
    """Return vertical corrector families."""
    return ['FCV', 'FFCV', 'CV', 'IDCV']


def families_skew_correctors():
    """Return skew corrector families."""
    return ['QS', 'IDQS']


def families_rf():
    """Return RF families."""
    return ['SRFCav', ]


def families_pulsed_magnets():
    """Return pulsed magnet families."""
    return ['InjDpKckr', 'InjNLKckr', 'PingH', 'PingV', ]


def families_di():
    """Return diagnostics families."""
    return [
        'BPM', 'IDBPM', 'DCCT', 'ScrapH', 'ScrapV', 'GSL15', 'GSL07',
        'GBPM', 'BbBPkup', 'BbBKckrH', 'BbBKckrV', 'BbBKckrL',
        'TuneShkrH', 'TuneShkrV', 'TunePkupH', 'TunePkupV']


def families_ids():
    """Return insertion devices families."""
    return ['APU22', 'APU58', 'DELTA52', 'IVU18', 'VPU29']


def families_id_correctors():
    """Return insertion device correctors families."""
    return ['IDC1', 'IDC4', 'IDC5']


def families_id_skew_correctors():
    """Return insertion device skew correctors families."""
    return ['IDQS', ]


def get_section_name_mapping(lattice):
    """Return list with section name of each lattice element."""
    lat = lattice[:]
    section_map = ['' for i in range(len(lat))]

    # find where the nomenclature starts counting and shift the lattice:
    start = _pyaccel.lattice.find_indices(lat, 'fam_name', 'start')[0]
    b1 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B1')
    if b1[0] > start:
        ind_shift = (b1[-1] + 1)  # Next element of last b1
    else:
        for i in b1[::-1]:  # except there is a b1 before start
            if i < start:
                ind_shift = i + 1
                break
    lat = _pyaccel.lattice.shift(lat, ind_shift)

    # find indices important to define the change of the names of
    # the subsections.
    b1 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B1')
    b1_nrsegs = len(b1)//_NR_B1
    b2 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B2')
    # b2_nrsegs = len(b2)//_NR_B2
    bc = _pyaccel.lattice.find_indices(lat, 'fam_name', 'BC')
    bpm = _pyaccel.lattice.find_indices(lat, 'fam_name', 'BPM')

    # divide the ring in 20 sectors defined by the b1 dipoles:
    Sects = []
    ini = 0
    for i in range(len(b1)//(2*b1_nrsegs)):
        end = b1[(i+1)*2*b1_nrsegs-1] + 1
        Sects.append(list(range(ini, end)))
        ini = end

    # Names of the subsections:
    sub_secs = ['M1', 'SX', 'M2', 'C1', 'C2', 'BC', 'C3', 'C4']
    symm = ['SA', 'SB', 'SP', 'SB']

    for i, sec in enumerate(Sects, 1):
        # conditions that define change in subsection name:
        # define changes to C1
        sec_b1 = [x for x in b1 if sec[0] <= x <= sec[-1]]
        relev_inds = [sec_b1[0]-1, sec_b1[-1]]
        # define changes to C2 and C4:
        sec_b2 = [x for x in b2 if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_b2[0]-1, sec_b2[-1]]
        # define changes to BC and C3
        sec_bc = [x for x in bc if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_bc[0]-1, sec_bc[-1]]
        # define changes to SX and M2
        sec_bpm = [x for x in bpm if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_bpm[0], sec_bpm[1]-1]
        relev_inds.sort()
        # fill the section_map variable
        ref = 0
        for j in sec:
            section_map[(ind_shift+j) % len(lat)] = "{0:02d}".format(i)
            section_map[(ind_shift+j) % len(lat)] += \
                symm[(i-1) % len(symm)] if sub_secs[ref] == 'SX' else \
                sub_secs[ref]
            if j >= relev_inds[ref]:
                ref += 1

    return section_map


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for family names.

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice, 'fam_name')
    section_map = get_section_name_mapping(lattice)

    def get_idx(x):
        return x[len(x)//2]
    # get_idx = lambda x: x[0]

    # fill the data dictionary with index info ######
    data = {}
    for key, idx in latt_dict.items():
        nr_el = _family_number_of_elements.get(key)
        if nr_el is None:
            continue
        nr_seg = len(idx)//nr_el
        if not nr_seg:
            nr_seg = 1
            nr_el = len(idx)
        # Create a list of lists for the indexes
        data[key] = [idx[i*nr_seg:(i+1)*nr_seg] for i in range(nr_el)]

    # ch - slow horizontal correctors
    idx = []
    fams = ['SDA0', 'SFB0', 'SFP0', 'SDA1', 'SDB1', 'SDP1',
            'SFA2', 'SFB2', 'SFP2']
    for fam in fams:
        idx.extend(data[fam])
    data['CH'] = sorted(idx, key=get_idx)

    # cv - slow vertical correctors
    idx = []
    fams = ['SDA0', 'SFB0', 'SFP0', 'SDA1', 'SDB1', 'SDP1',
            'SDA3', 'SDB3', 'SDP3', 'SFA2', 'SFB2', 'SFP2', 'CV']
    for fam in fams:
        if fam in {'SFA2', 'SFB2', 'SFP2'}:
            # for these families there are skew only in C3 sections
            idx.extend([i for i in data[fam] if 'C3' in section_map[i[0]]])
        else:
            idx.extend(data[fam])
    data['CV'] = sorted(idx, key=get_idx)

    # idch - id horizontal correctors
    idx = []
    fams = ['IDC1', 'IDC2', 'IDC3']
    for fam in fams:
        if fam in data:
            idx.extend(data[fam])
    data['IDCH'] = sorted(idx, key=get_idx)

    # idcv - id vertical correctors
    idx = []
    fams = ['IDC1', 'IDC2']
    for fam in fams:
        if fam in data:
            idx.extend(data[fam])
    data['IDCV'] = sorted(idx, key=get_idx)

    # fch - fast horizontal correctors
    idx = []
    fams = ['FC1', 'FC1FF', 'FC2', ]
    for fam in fams:
        if fam in data:
            idx.extend(data[fam])
    data['FCH'] = sorted(idx, key=get_idx)

    # fcv - fast vertical correctors
    data['FCV'] = sorted(idx, key=get_idx)

    # ffch - feedforward horizontal correctors
    idx = []
    fams = ['FC1FF', ]
    for fam in fams:
        if fam in data:
            idx.extend(data[fam])
    data['FFCH'] = sorted(idx, key=get_idx)

    # ffcv - feedforward vertical correctors
    data['FFCV'] = sorted(idx, key=get_idx)

    # qs - skew quad correctors
    idx = []
    fams = ['SFA0', 'SDB0', 'SDP0', 'SDA2', 'SDB2',
            'SDP2', 'SDA3', 'SDB3', 'SDP3', 'FC2']
    for fam in fams:
        if fam in {'SDA2', 'SDB2', 'SDP2'}:
            # for these families there are skew only in C1 sections
            idx.extend([i for i in data[fam] if 'C1' in section_map[i[0]]])
        elif fam in {'SDA3', 'SDB3', 'SDP3'}:
            # for these families there are skew only in C3 sections
            idx.extend([i for i in data[fam] if 'C3' in section_map[i[0]]])
        elif fam == 'FC2':
            idx.extend([i for i in data[fam] if 'C2' in section_map[i[0]]])
        else:
            idx.extend(data[fam])
    data['QS'] = sorted(idx, key=get_idx)

    # quadrupoles knobs for optics correction
    idx = []
    fams = ['QFA', 'QDA', 'QDB2', 'QFB', 'QDB1', 'QDP2', 'QFP', 'QDP1',
            'Q1', 'Q2', 'Q3', 'Q4']
    for fam in fams:
        idx.extend(data[fam])
    data['QN'] = sorted(idx, key=get_idx)

    # sbs - sextupoles knobs for optics correction
    idx = []
    fams = ['SDA0', 'SDB0', 'SDP0', 'SDA1', 'SDB1', 'SDP1', 'SDA2', 'SDB2',
            'SDP2', 'SDA3', 'SDB3', 'SDP3', 'SFA0', 'SFB0', 'SFP0', 'SFA1',
            'SFB1', 'SFP1', 'SFA2', 'SFB2', 'SFP2']
    for fam in fams:
        idx.extend(data[fam])
    data['SN'] = sorted(idx, key=get_idx)

    # Power Supply for B1 and B2 families
    data['B1B2-1'] = sorted(data['B1']+data['B2'], key=get_idx)
    data['B1B2-2'] = sorted(data['B1']+data['B2'], key=get_idx)

    # all dipoles indices
    data['BN'] = sorted(data['B1']+data['B2']+data['BC'], key=get_idx)

    # PingH (in the model the same as InjDpKckr)
    data['PingH'] = sorted(data['InjDpKckr'], key=get_idx)

    # IDs
    idx = []
    fams = families_ids()
    for fam in fams:
        if fam in data:
            idx.extend(data[fam])
    data['ID'] = sorted(idx, key=get_idx)

    # ID skew correctors
    idx = []
    fams = families_id_skew_correctors()
    for fam in fams:
        if fam in data:
            idx.extend(data[fam])
    data['IDQS'] = sorted(idx, key=get_idx)

    # Girders
    girder = get_girder_data(lattice)
    if girder is not None:
        data['girder'] = girder

    def f(x):
        return '{0:d}'.format(x)

    # now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [section_map[get_idx(i)] for i in idx]

        # find out if there are more than one element per section and
        # attribute a number to it
        num = len(secs)*['']
        if len(secs) > 1:
            j = 1
            num[0] = f(j) if secs[0] == secs[1] else ''
            j = j+1 if secs[0] == secs[1] else 1
            for i in range(1, len(secs)-1):
                num[i] = f(j) if secs[i] == secs[i+1] or secs[i] == secs[i-1] \
                    else ''
                j = j+1 if secs[i] == secs[i+1] else 1
            num[-1] = f(j) if (secs[-1] == secs[-2]) else ''

        new_data[key] = {'index': idx, 'subsection': secs, 'instance': num}

    # get control system devname
    for key in new_data:
        if key not in _discipline_mapping:
            continue
        if key in ('IDC1', 'IDC2', 'IDC3'):
            continue
        dis = _discipline_mapping[key]
        dta = new_data[key]
        devnames = []
        subs = dta['subsection']
        insts = dta['instance']
        dev = key
        if dev in ('IDCH', 'IDCV', 'IDQS', 'IDBPM'):
            dev = dev[2:]
        for sub, inst in zip(subs, insts):
            devnames.append(
                _join_name(sec='SI', dis=dis, sub=sub, idx=inst, dev=dev))
        new_data[key]['devnames'] = devnames

    return new_data


def get_girder_data(lattice):
    """Return girder data.

    List of dicts, one for each girder, containing index of elements in that
    girder.
    """
    gir = _pyaccel.lattice.find_indices(lattice, 'fam_name', 'girder')
    if not gir:
        return None
    gir_ini = gir[0::2]
    gir_end = gir[1::2]

    data = []
    for ini, end in zip(gir_ini, gir_end):
        data.append(list(range(ini, end+1)))
    return data
