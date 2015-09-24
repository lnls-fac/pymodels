"""Element family definitions"""

from . import lattice as _lattice
import pyaccel as _pyaccel
import numpy as _np


def families_dipoles():
    return ['bend']

def families_septa():
    return ['septex', 'septing', 'septinf']

def families_quadrupoles():
    return ['qd', 'qf']

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
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index=[]
            j=0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index']=new_index

    return data

_family_segmentation={ 'bend'    : 2, 'septex'  : 2, 'septing' : 2, 'septinf' : 2,
                       'qf1a'    : 1, 'qf1b'  : 1, 'qd2'  : 1, 'qf2'  : 1,
                       'qf3'     : 1, 'qd4a'  : 1, 'qf4'  : 1, 'qd4b' : 1,
                       'bpm'     : 1, 'hcm'   : 1, 'vcm'  : 1, 'qd'   : 1, 'qf' : 1
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
    'hcm'     : 'horizontal_corrector',
    'vcm'     : 'vertical_corrector',
    'qd'      : 'quadrupole',
    'qf'      : 'quadrupole',
}
