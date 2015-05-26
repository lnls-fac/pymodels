#!/usr/bin/env python3

import math as _math
import numpy as _np
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M0 as _optics_mode_M0

_default_optics_mode = _optics_mode_M0
_energy = 0.15e9 #[eV]
_family_segmentation={ 'b'  : 14, 'qf' : 2, 'qd' : 1, 'sd' : 1,
                       'sf' : 1, 'bpm' : 1, 'ch' : 1, 'cv' : 1 }

def create_lattice(**kwargs):

    return []


def sirius_bo_family_data(lattice):
    latt_dict=_pyaccel.lattice.finddict(lattice,'fam_name')
    data={}

    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    for key in data.keys():
        if key == 'qf':
            idx=data[key]['index'].pop()
            data[key]['index'].insert(0,idx)

        if data[key]['nr_segs'] != 1:
            new_index = []
            j = 0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index'] = new_index

    return data

_the_ring = create_lattice()
_family_data = sirius_bo_family_data(_the_ring)
