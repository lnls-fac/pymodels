"""Element family definitions"""

from . import lattice as _lattice
import pyaccel as _pyaccel
import numpy as _np


def families_dipoles():
    return ['bend']

def families_septa():
    return ['septex', 'septing', 'septinf']

def families_quadrupoles():
    return ['quad']

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
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key]}

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index=[]
            j=0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index']=new_index

    return data

_family_segmentation={ 'bend' : 2, 'septex' : 2, 'septing' : 2, 'septinf' : 2,
                       'qf1a' : 1, 'qf1b'   : 1, 'qd2'     : 1, 'qf2'     : 1,
                       'qf3'  : 1, 'qd4a'   : 1, 'qf4'     : 1, 'qd4b'    : 1,
                       'bpm'  : 1, 'ch'     : 1, 'cv'      : 1, 'start'   : 1,
                       }

_family_mapping = {
    'bend'    : 'dipole',
    'septex'  : 'septum',
    'septing' : 'septum',
    'septinf' : 'septum',
    'qf1a'    : 'quadrupole',
    'qf1b'    : 'quadrupole',
    'qd2'     : 'quadrupole',
    'qf2'     : 'quadrupole',
    'qf3'     : 'quadrupole',
    'qd4a'    : 'quadrupole',
    'qf4'     : 'quadrupole',
    'qd4b'    : 'quadrupole',
    'bpm'     : 'bpm',
    'ch'     : 'horizontal_corrector',
    'cv'     : 'vertical_corrector',
    'qd'      : 'quadrupole',
    'qf'      : 'quadrupole',
}
