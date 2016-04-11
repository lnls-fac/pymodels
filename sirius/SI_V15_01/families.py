"""Element family definitions"""

import numpy as _numpy
import pyaccel as _pyaccel
from . import lattice as _lattice

def families_dipoles():
    return ['bend',]

def families_quadrupoles():
    return ['qfa', 'qda', 'qfb', 'qdb1', 'qdb2', 'qfp', 'qdp1', 'qdp2', 'q1', 'q2', 'q3', 'q4',]

def families_sextupoles():
    return ['sda0', 'sdba0', 'sdbp0', 'sdp0',
            'sda1', 'sdba1', 'sdbp1', 'sdp1',
            'sda2', 'sdba2', 'sdbp2', 'sdp2',
            'sda3', 'sdba3', 'sdbp3', 'sdp3',
            'sfa0', 'sfba0', 'sfbp0', 'sfp0',
            'sfa1', 'sfba1', 'sfbp1', 'sfp1',
            'sfa2', 'sfba2', 'sfbp2', 'sfp2']

def families_horizontal_correctors():
    return ['fch', 'ch',]

def families_vertical_correctors():
    return ['fcv', 'cv',]

def families_skew_correctors():
    return ['qs',]

def families_rf():
    return ['cav',]

def families_pulsed_magnets():
    return ['kick_in', 'pmm']


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
    fams = ['sfa0','sfba0','sfbp0','sfp0','sda1','sdba1','sdbp1','sdp1','sfa2','sfba2','sfbp2','sfp2']
    for fam in fams:
        idx.extend(data[fam]['index'])
    data['ch']={'index':sorted(idx), 'nr_segs':_family_segmentation['ch']}

    # cv - slow vertical correctors
    idx = []
    fams = ['sfa0','sfba0','sfbp0','sfp0','sda1','sdba1','sdbp1','sdp1','sda3','sdba3','sdbp3','sdp3','cv']
    for fam in fams:
            idx.extend(data[fam]['index'])
    # In this version of the lattice, there is a cv corrector in the sextupoles
    # sf2 of every sector C3 of the arc the lattice. It means the corrector
    # alternates between all SF2's. The logic bellow uses the
    # dipoles B2 and BC_LF to determine where to put the corrector.
    indices = sorted(data['sfa2']['index'] + data['sfba2']['index'] + data['sfbp2']['index'] + data['sfp2']['index'])
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
    data['fch']={'index':data['fc']['index'], 'nr_segs':_family_segmentation['fch']}

    # fcv - fast vertical correctors
    data['fcv']={'index':data['fc']['index'], 'nr_segs':_family_segmentation['fcv']}

    # bc
    data['bc']={'index':sorted(data['bc_hf']['index']+data['bc_lf']['index']), 'nr_segs':_family_segmentation['bc']}

    # qs - skew quad correctors
    idx = []
    fams = ['sda0','sdba0','sdbp0','sdp0','sfa1','sfba1','sfbp1','sfp1']
    for fam in fams:
            idx.extend(data[fam]['index'])
    data['qs']={'index':sorted(idx), 'nr_segs':_family_segmentation['qs']}

    # qn - quadrupoles knobs for optics correction
    idx = []
    fams = ['qfa','qda','q1','q2','q3','q4','qdb1','qfb','qdb2','qdp1','qfp','qdp2']
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
    'b1'    : 30, 'b2'    : 36,
    'bc'    : 30, 'bc_hf' : 16, 'bc_lf' : 14,
    'qfa'   : 1,  'qda'   : 1,
    'qfb'   : 1,  'qdb1'  : 1,  'qdb2'  : 1,
    'qfp'   : 1,  'qdp1'  : 1,  'qdp2'  : 1,
    'q1'    : 1,  'q2'    : 1,  'q3'    : 1,  'q4'   : 1,
    'sda0'  : 1, 'sdba0'  : 1, 'sdbp0'  : 1, 'sdp0'  : 1,
    'sda1'  : 1, 'sdba1'  : 1, 'sdbp1'  : 1, 'sdp1'  : 1,
    'sda2'  : 1, 'sdba2'  : 1, 'sdbp2'  : 1, 'sdp2'  : 1,
    'sda3'  : 1, 'sdba3'  : 1, 'sdbp3'  : 1, 'sdp3'  : 1,
    'sfa0'  : 1, 'sfba0'  : 1, 'sfbp0'  : 1, 'sfp0'  : 1,
    'sfa1'  : 1, 'sfba1'  : 1, 'sfbp1'  : 1, 'sfp1'  : 1,
    'sfa2'  : 1, 'sfba2'  : 1, 'sfbp2'  : 1, 'sfp2'  : 1,
    'bpm'   : 1,  'fc'    : 1,  'fch'   : 1,  'fcv'  : 1,
    'qs'    : 1,  'ch'    : 1,  'cv'    : 1,  'qn'   : 1,
    'cav'   : 1,  'start' : 1,
    'kick_in' : 1, 'pmm' : 1,
}

_family_mapping = {

    'b1'  : 'dipole',
    'b2'  : 'dipole',
    'bc'  : 'dipole',

    'qfa' : 'quadrupole',
    'qda' : 'quadrupole',
    'qdb2': 'quadrupole',
    'qfb' : 'quadrupole',
    'qdb1': 'quadrupole',
    'qdp2': 'quadrupole',
    'qfp' : 'quadrupole',
    'qdp1': 'quadrupole',
    'q1'  : 'quadrupole',
    'q2'  : 'quadrupole',
    'q3'  : 'quadrupole',
    'q4'  : 'quadrupole',

    'sda0' : 'sextupole',
    'sdba0': 'sextupole',
    'sdbp0': 'sextupole',
    'sdp0' : 'sextupole',
    'sda1' : 'sextupole',
    'sdba1': 'sextupole',
    'sdbp1': 'sextupole',
    'sdp1' : 'sextupole',
    'sda2' : 'sextupole',
    'sdba2': 'sextupole',
    'sdbp2': 'sextupole',
    'sdp2' : 'sextupole',
    'sda3' : 'sextupole',
    'sdba3': 'sextupole',
    'sdbp3': 'sextupole',
    'sdp3' : 'sextupole',
    'sfa0' : 'sextupole',
    'sfba0': 'sextupole',
    'sfbp0': 'sextupole',
    'sfp0' : 'sextupole',
    'sfa1' : 'sextupole',
    'sfba1': 'sextupole',
    'sfbp1': 'sextupole',
    'sfp1' : 'sextupole',
    'sfa2' : 'sextupole',
    'sfba2': 'sextupole',
    'sfbp2': 'sextupole',
    'sfp2' : 'sextupole',

    'pmm'    : 'pulsed_magnet',
    'kick_in': 'pulsed_magnet',

    'bpm' : 'bpm',

    'cf'  : 'fast_corrector',
    'fch' : 'fast_horizontal_corrector',
    'fcv' : 'fast_vertical_corrector',

    'ch'  : 'slow_horizontal_corrector',
    'cv'  : 'slow_vertical_corrector',

    'qs'  : 'skew_quadrupole',
}
