"""Element family definitions"""

from . import lattice as _lattice
import pyaccel as _pyaccel


def families_dipoles():
    return ['bend']

def families_septa():
    return ['sep']

def families_quadrupoles():
    return ['qf','qd','triplet']

def families_horizontal_correctors():
    return ['ch']

def families_vertical_correctors():
    return ['cv']

def families_sextupoles():
    return []

def families_skew_correctors():
    return []

def families_rf():
    return []

def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict=_pyaccel.lattice.find_dict(lattice,'fam_name')
    data={}

    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key]={'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key]}

    if len(data['bpm']['index']) > 6:
        data['bpm']['index'].pop()

    if len(data['ch']['index']) > 5:
        # linac horizontal corrector
        data['lch']={'index':[data['ch']['index'][0]], 'nr_segs':_family_segmentation['ch']}
        # remove linac corrector from ch data
        data['ch']['index'] = data['ch']['index'][1:]

    if len(data['cv']['index']) > 6:
        # linac vertical corrector
        data['lcv']={'index':[data['cv']['index'][0]], 'nr_segs':_family_segmentation['cv']}
        # remove linac corrector from cv data
        data['cv']['index'] = data['cv']['index'][1:]

    # qd
    idx = []
    families = ['qd2','qd3a','qd3b','qd4','qd5']
    for family in families:
            idx.extend(data[family]['index'])
    data['qd']={'index':sorted(idx), 'nr_segs':_family_segmentation['quad']}

    # qf
    idx = []
    families = ['qf2','qf3a','qf3b','qf4','qf5']
    for family in families:
            idx.extend(data[family]['index'])
    data['qf']={'index':sorted(idx), 'nr_segs':_family_segmentation['quad']}

    # triplet
    idx = []
    families = ['q1a','q1b','q1c']
    for family in families:
            idx.extend(data[family]['index'])
    data['triplet']={'index':sorted(idx), 'nr_segs':_family_segmentation['triplet']}

    # septum
    data['sep']={'index':data['septin']['index'], 'nr_segs':_family_segmentation['sep']}

    # dipole
    idx = []
    families = ['bn', 'bp', 'spec']
    for family in families:
            idx.extend(data[family]['index'])
    data['bend']={'index':sorted(idx), 'nr_segs':_family_segmentation['bend']}

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index=[]
            j=0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index']=new_index

    return data

_family_segmentation = { 'bn':2, 'bp':2, 'bpm':1, 'ch': 1, 'cv': 1,
                         'q1a':1, 'q1b':1, 'q1c':1, 'qd2':1, 'qf2':1, 'qd3a':1, 'qf3a':1, 'qf3b':1, 'qd3b':1,
                         'qf4':1, 'qd4':1, 'qf5':1, 'qd5':1,
                         'septin':2, 'spec':2,
                         'quad':1, 'bend':2, 'sep':2, 'triplet':1,
                         'start':1,
                          }

_family_mapping = {
    'bn':      'dipole',
    'bp':      'dipole',
    'bpm':     'bpm',
    'spec':    'dipole',
    'ch':     'horizontal_corrector',
    'cv':     'vertical_corrector',
    'q1a':     'quadrupole',
    'q1b':     'quadrupole',
    'q1c':     'quadrupole',
    'qd2':     'quadrupole',
    'qf2':     'quadrupole',
    'qd3a':    'quadrupole',
    'qf3a':    'quadrupole',
    'qf3b':    'quadrupole',
    'qd3b':    'quadrupole',
    'qf4':     'quadrupole',
    'qd4':     'quadrupole',
    'qf5':     'quadrupole',
    'qd5':     'quadrupole',
    'septin':  'septum',
    'bend':    'dipole',
    'sep':     'septum',
    'qd':      'quadrupole',
    'qf':      'quadrupole',
    'triplet': 'quadrupole',
}
