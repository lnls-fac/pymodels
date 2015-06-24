
import pyaccel as _pyaccel
from . import lattice as _lattice


def sirius_bo_family_data(lattice):
    latt_dict=_pyaccel.lattice.find_dict(lattice,'fam_name')
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


_family_segmentation={ 'b'  : 14, 'qf' : 2, 'qd' : 1, 'sd' : 1,
                       'sf' : 1, 'bpm' : 1, 'ch' : 1, 'cv' : 1 }
_family_data = sirius_bo_family_data(_lattice._the_ring)
