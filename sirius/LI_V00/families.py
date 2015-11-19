"""Element family definitions"""

from . import lattice as _lattice
import pyaccel as _pyaccel
import numpy as _np

def families_dipoles():
    return []

def families_septa():
    return []

def families_quadrupoles():
    return []

def families_horizontal_correctors():
    return []

def families_vertical_correctors():
    return []

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
    latt_dict=_pyaccel.lattice.find_dict(lattice, 'fam_name')
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


_family_segmentation = {}
_family_mapping = {}
