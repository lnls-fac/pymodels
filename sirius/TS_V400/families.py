"""Element family definitions"""

from . import lattice as _lattice
import pyaccel as _pyaccel


def families_dipoles():
    return ['bf', 'bd']


def families_septa():
    return ['seb', 'seg', 'sef']


def families_quadrupoles():
    return ['qf', 'qd']


def families_horizontal_correctors():
    return ['ch']


def families_vertical_correctors():
    return ['cv']


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
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    #bpm
    data['bpm']['index'].pop()

    # qf
    data['qf']={}
    data['qf']['index'] = []
    data['qf']['nr_segs'] = _family_segmentation['qf']
    data['qf']['families'] = ['qa1', 'qc1', 'qc2', 'qd2', 'qd3']
    for family in data['qf']['families']:
        data['qf']['index'] = data['qf']['index'] + latt_dict[family]
    data['qf']['index']=sorted(data['qf']['index'])

    # qd
    data['qd']={}
    data['qd']['index'] = []
    data['qd']['nr_segs'] = _family_segmentation['qd']
    data['qd']['families'] = ['qa2', 'qb1', 'qd1', 'qd4']
    for family in data['qd']['families']:
        data['qd']['index'] = data['qd']['index'] + latt_dict[family]
    data['qd']['index']=sorted(data['qd']['index'])

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index = []
            j = 0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index'] = new_index

    return data


_family_segmentation={ 'bf'  : 2, 'bd'  : 2, 'seb' : 2, 'seg' : 2, 'sef' : 2,
                       'qf'  : 1, 'qa1' : 1, 'qc1' : 1, 'qc2' : 1,  'qd2': 1, 'qd3' : 1,
                       'qd'  : 1, 'qa2' : 1, 'qb1' : 1, 'qd1' : 1, 'qd4' : 1,
                       'bpm' : 1, 'ch'  : 1, 'cv'  : 1,
                       }
_family_data = get_family_data(_lattice._the_line)
_family_mapping = {
    'bf': 'dipole',
    'bd': 'dipole',

    'seb': 'septum',
    'seg': 'septum',
    'sef': 'septum',

    'qf': 'quadrupole',
    'qa1': 'quadrupole',
    'qc1': 'quadrupole',
    'qc2': 'quadrupole',
    'qd2': 'quadrupole',
    'qd3': 'quadrupole',
    'qd': 'quadrupole',
    'qa2': 'quadrupole',
    'qb1': 'quadrupole',
    'qd1': 'quadrupole',
    'qd4': 'quadrupole',

    'bpm': 'bpm',

    'ch': 'horizontal_corrector',
    'cv': 'vertical_corrector',
}
