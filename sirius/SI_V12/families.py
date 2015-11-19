"""Element family definitions"""

import numpy as _numpy
import pyaccel as _pyaccel
from . import lattice as _lattice

def families_dipoles():
    return ['bend',]

def families_quadrupoles():
    return ['qfa', 'qda', 'qfb', 'qdb1', 'qdb2', 'qf1', 'qf2', 'qf3', 'qf4',]

def families_sextupoles():
    return ['sda', 'sfa', 'sdb', 'sfb',
            'sd1j', 'sf1j', 'sd2j', 'sd3j', 'sf2j',
            'sd1k', 'sf1k', 'sd2k', 'sd3k', 'sf2k', ]

def families_horizontal_correctors():
    return ['fch', 'ch',]

def families_vertical_correctors():
    return ['fcv', 'cv',]

def families_skew_correctors():
    return ['qs',]

def families_rf():
    return ['cav',]

def families_septa():
    return []


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice,'fam_name')
    data = {}
    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key]}

    # ch - slow horizontal correctors
    idx = []
    fams = ['sfa','sfb','sd1j','sf2j','sd1k','sf2k']
    for fam in fams:
        idx.extend(data[fam]['index'])
    data['ch']={'index':sorted(idx), 'nr_segs':_family_segmentation['ch']}

    # cv - slow vertical correctors
    idx = []
    fams = ['sfa','sd1j','sd3j','sfb','sd1k','sd3k','cv']
    for fam in fams:
            idx.extend(data[fam]['index'])
    #In this version of the lattice, there is a cv corrector in the sextupoles
    #sf2 of every sector C3 of the arc of the lattice. It means the corrector
    #alternates between a SF2J and SF2K. The logic bellow uses the dipoles B2
    #and BC_LF to determine where to put the corrector.
    indices = sorted(data['sf2k']['index'] + data['sf2j']['index'])
    dipoles = sorted(data['b2']['index'] + data['bc_lf']['index'])
    dipoles = _numpy.array(dipoles)
    for i in indices:
        el, *_ = _numpy.nonzero(dipoles > i)
        if len(el) != 0:
            if lattice[dipoles[el[0]]].fam_name == 'b2':
                idx += [i]
        else:
            el, *_ = _numpy.nonzero(dipoles < i)
            if len(el) != 0:
                if lattice[dipoles[el[-1]]].fam_name == 'bc_lf':
                    idx += [i]
            else:
                raise Exception('Problem with vertical corrector index definition.')
    data['cv']={'index':sorted(idx), 'nr_segs':_family_segmentation['cv']}

    # fch - fast horizontal correctors
    data['fch']={'index':data['cf']['index'], 'nr_segs':_family_segmentation['fch']}

    # fcv - fast vertical correctors
    data['fcv']={'index':data['cf']['index'], 'nr_segs':_family_segmentation['fcv']}

    # bc
    data['bc']={'index':sorted(data['bc_hf']['index']+data['bc_lf']['index']), 'nr_segs':_family_segmentation['bc']}

    # qs - skew quad correctors
    idx = []
    fams = ['sfa','sda','sf1j','sf1k']
    for fam in fams:
            idx.extend(data[fam]['index'])
    data['qs']={'index':sorted(idx), 'nr_segs':_family_segmentation['qs']}

    # qn - quadrupoles knobs for optics correction
    idx = []
    fams = ['qfa','qda','qf1','qf2','qf3','qf4','qdb1','qfb','qdb2']
    for fam in fams:
            idx.extend(data[fam]['index'])
    data['qn']={'index':sorted(idx), 'nr_segs':_family_segmentation['qn']}

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index = []
            j = 0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index'] = new_index

    #girders
    girder =  get_girder_data(lattice)
    if girder is not None: data['girder'] = girder

    return data

def get_girder_data(lattice):
    data = []
    gir = _pyaccel.lattice.find_indices(lattice,'fam_name','girder')
    if len(gir) == 0: return None

    gir_ini = gir[0::2]
    gir_end = gir[1::2]
    for i in range(len(gir_ini)):
        idx = list(range(gir_ini[i],gir_end[i]+1))
        data.append(dict({'index':idx}))

    return data


_family_segmentation={
    'b1'  : 2, 'b2' : 3, 'bc_hf' : 14, 'bc_lf' : 14, 'bc': 28,
    'qfa' : 1, 'qda': 1, 'qdb2': 1, 'qfb': 1,
    'qdb1': 1, 'qf1': 1, 'qf2' : 1, 'qf3': 1, 'qf4': 1,
    'sda' : 1, 'sfa': 1, 'sdb' : 1, 'sfb': 1,
    'sd1j': 1, 'sf1j': 1, 'sd2j': 1, 'sd3j' : 1, 'sf2j': 1,
    'sd1k': 1, 'sf1k': 1, 'sd2k': 1, 'sd3k' : 1, 'sf2k': 1,
    'bpm' : 1, 'cf' : 1,
    'fch' : 1, 'fcv': 1, 'qs'  : 1, 'ch': 1, 'cv': 1, 'qn' : 1,
    'cav' : 1,
    'start': 1,
}

_family_mapping = {

    'b1': 'dipole',
    'b2': 'dipole',
    'bc': 'dipole',

    'qfa' : 'quadrupole',
    'qda' : 'quadrupole',
    'qdb2': 'quadrupole',
    'qfb' : 'quadrupole',
    'qdb1': 'quadrupole',
    'qf1' : 'quadrupole',
    'qf2' : 'quadrupole',
    'qf3' : 'quadrupole',
    'qf4' : 'quadrupole',

    'sda' : 'sextupole',
    'sfa' : 'sextupole',
    'sdb' : 'sextupole',
    'sfb' : 'sextupole',
    'sd1j': 'sextupole',
    'sf1j': 'sextupole',
    'sd2j': 'sextupole',
    'sd3j': 'sextupole',
    'sf2j': 'sextupole',
    'sd1k': 'sextupole',
    'sf1k': 'sextupole',
    'sd2k': 'sextupole',
    'sd3k': 'sextupole',
    'sf2k': 'sextupole',

    'bpm': 'bpm',

    'cf' : 'fast_corrector',
    'fch': 'fast_horizontal_corrector',
    'fcv': 'fast_vertical_corrector',

    'ch': 'slow_horizontal_corrector',
    'cv': 'slow_vertical_corrector',

    'qs' : 'skew_quadrupole',
}
