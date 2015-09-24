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
    return ['hcm']

def families_vertical_correctors():
    return ['vcm']

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
            data[key]={'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    if len(data['bpm']['index']) == 7:
        # bpm
        data['bpm']['index'].pop()

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index=[]
            j=0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index']=new_index

    # qd
    data['qd']={}
    data['qd']['index'] = []
    data['qd']['nr_segs'] = _family_segmentation['quad']
    data['qd']['families'] = ['qd2','qd3a','qd3b','qd4','qd5']
    for family in data['qd']['families']:
        data['qd']['index'] = data['qd']['index'] + latt_dict[family]
    data['qd']['index']=sorted(data['qd']['index'])

    # qf
    data['qf']={}
    data['qf']['index'] = []
    data['qf']['nr_segs'] = _family_segmentation['quad']
    data['qf']['families'] = ['qf2','qf3a','qf3b','qf4','qf5']
    for family in data['qf']['families']:
        data['qf']['index'] = data['qf']['index'] + latt_dict[family]
    data['qf']['index']=sorted(data['qf']['index'])

    # triplet
    data['triplet']={}
    data['triplet']['index'] = []
    data['triplet']['nr_segs'] = _family_segmentation['triplet']
    data['triplet']['families'] = ['q1a','q1b','q1c']
    for family in data['triplet']['families']:
        data['triplet']['index'] = data['triplet']['index'] + latt_dict[family]
    data['triplet']['index']=sorted(data['triplet']['index'])

    # quadrupole
    data['quad']={}
    data['quad']['index'] = []
    data['quad']['nr_segs'] = _family_segmentation['quad']
    data['quad']['families'] = ['q1a','q1b','q1c','qd2','qf2','qd3a','qf3a','qf3b','qd3b','qf4','qd4','qf5','qd5']
    for family in data['quad']['families']:
        data['quad']['index'] = data['quad']['index'] + latt_dict[family]
    data['quad']['index']=sorted(data['quad']['index'])

    # septum
    data['sep']={}
    data['sep']['index'] = []
    data['sep']['nr_segs'] = _family_segmentation['sep']
    data['sep']['families'] = ['septin']
    for family in data['sep']['families']:
        data['sep']['index'] = data['sep']['index'] + latt_dict[family]
    data['sep']['index']=sorted(data['sep']['index'])

    return data

_family_segmentation = { 'bn':2, 'bp':2, 'bpm':1, 'hcm': 1, 'vcm': 1,
                         'q1a':1, 'q1b':1, 'q1c':1, 'qd2':1, 'qf2':1, 'qd3a':1, 'qf3a':1, 'qf3b':1, 'qd3b':1,
                         'qf4':1, 'qd4':1, 'qf5':1, 'qd5':1,
                         'septin':2, 'spec':2,
                         'quad':1, 'bend':2, 'sep':2, 'triplet':1
                          }

_family_mapping = {
    'bn':      'dipole',
    'bp':      'dipole',
    'bpm':     'bpm',
    'spec':    'dipole',
    'hcm':     'horizontal_corrector',
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
    'vcm':     'vertical_corrector',
    'bend':    'dipole',
    'sep':     'septum',
    'quad':    'quadrupole',
    'qd':      'quadrupole',
    'qf':      'quadrupole',
    'triplet': 'quadrupole',
}
